# -*- coding: utf-8 -*-
# Copyright 2015 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import time
from datetime import date
from decimal import Decimal

from openerp.report import report_sxw


class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):  # pylint: disable=R8110
        super(Parser, self).__init__(cr, uid, name, context)
        self.lines = []
        self.total_debit = 0.0
        self.total_credit = 0.0
        self.total_debit_currency = 0.0
        self.total_credit_currency = 0.0
        self.localcontext.update(
            {
                "time": time,
                "get_account": self.get_account,
                "line": self.get_general_ledger_line,
                "get_period": self.get_period,
                "get_company": self.get_company,
                "total_debit": self.get_total_debit,
                "total_credit": self.get_total_credit,
                "total_debit_currency": self.get_total_debit_currency,
                "total_credit_currency": self.get_total_credit_currency,
                "beginning_balance": self.get_beginning_balance,
            }
        )

    def _prepare_opening_balance(self, account_id, state, date_start_period):
        obj_account_period = self.pool.get("account.period")

        kriteria_opening_balance = [
            ("date_start", "=", date_start_period),
            ("special", "=", 1),
        ]

        period_ids = obj_account_period.search(
            self.cr, self.uid, kriteria_opening_balance
        )

        period = obj_account_period.browse(self.cr, self.uid, period_ids)[0]

        kriteria = [("account_id", "=", account_id), ("period_id", "=", period.id)]
        if state != "all":
            kriteria.append(("move_id.state", "=", state))

        return kriteria

    def _prepare_beginning_balance(
        self,
        account_id,
        state,
        period,
        date_start_period,
    ):
        tahun = int(period.date_start[0:4])
        bulan = int(period.date_start[5:7])
        hari = int(period.date_start[8:10])

        tanggal = date(tahun, bulan, hari)

        ord_tanggal_awal = tanggal.toordinal() - 1
        tanggal_awal = date.fromordinal(ord_tanggal_awal)

        kriteria = [
            ("account_id", "=", account_id),
            ("date", ">=", date_start_period),
            ("date", "<=", str(tanggal_awal)),
        ]
        if state != "all":
            kriteria.append(("move_id.state", "=", state))

        return kriteria

    def _prepare_line(
        self,
        account_id,
    ):
        data = self.localcontext["data"]["form"]
        obj_account_period = self.pool.get("account.period")
        start_period_id = (
            data["start_period_id"] and data["start_period_id"][0] or False
        )
        start_period = obj_account_period.browse(self.cr, self.uid, start_period_id)

        end_period_id = data["end_period_id"][0] and data["end_period_id"][0] or False
        end_period = obj_account_period.browse(self.cr, self.uid, end_period_id)
        state = data["state"]

        if start_period_id == end_period_id:
            kriteria = [
                ("account_id", "=", account_id),
                ("date", ">=", start_period.date_start),
                ("date", "<=", start_period.date_stop),
                ("period_id.special", "=", False),
            ]
        else:
            kriteria = [
                ("account_id", "=", account_id),
                ("date", ">=", start_period.date_start),
                ("date", "<=", end_period.date_stop),
                ("period_id.special", "=", False),
            ]

        if state != "all":
            kriteria.append(("move_id.state", "=", state))

        return kriteria

    def get_opening_balance(self, kriteria):
        opening_balance = 0.00
        opening_balance_curr = 0.00
        obj_account_move_line = self.pool.get("account.move.line")

        account_move_line_ids = obj_account_move_line.search(
            self.cr, self.uid, kriteria
        )

        if account_move_line_ids:
            account_move_line_id = obj_account_move_line.browse(
                self.cr, self.uid, account_move_line_ids
            )

            for account_move_line in account_move_line_id:
                debit = account_move_line.debit
                credit = account_move_line.credit
                opening_balance += debit - credit
                opening_balance_curr += account_move_line.amount_currency

        return opening_balance, opening_balance_curr

    def beginning_balance(self, account_id):
        beginning_balance = 0.00
        beginning_balance_curr = 0.00
        obj_account_move_line = self.pool.get("account.move.line")
        obj_account_period = self.pool.get("account.period")
        obj_account_fiscalyear = self.pool.get("account.fiscalyear")

        data = self.localcontext["data"]["form"]

        start_period_id = (
            data["start_period_id"] and data["start_period_id"][0] or False
        )
        end_period_id = data["end_period_id"] and data["end_period_id"][0] or False

        fiscalyear_id = data["fiscalyear_id"] and data["fiscalyear_id"][0] or False

        state = data["state"]

        if start_period_id:
            period_id = start_period_id
        else:
            period_id = end_period_id

        period = obj_account_period.browse(self.cr, self.uid, period_id)

        fiscalyear = obj_account_fiscalyear.browse(self.cr, self.uid, fiscalyear_id)

        if period.date_start == fiscalyear.date_start or not start_period_id:
            kriteria = self._prepare_opening_balance(
                account_id, state, fiscalyear.date_start
            )
            opening_balance, opening_balance_curr = self.get_opening_balance(kriteria)
            return opening_balance, opening_balance_curr
        else:
            kriteria = self._prepare_beginning_balance(
                account_id, state, period, fiscalyear.date_start
            )

        account_move_line_ids = obj_account_move_line.search(
            self.cr, self.uid, kriteria
        )

        if account_move_line_ids:
            account_move_line_id = obj_account_move_line.browse(
                self.cr, self.uid, account_move_line_ids
            )

            for account_move_line in account_move_line_id:
                debit = account_move_line.debit
                credit = account_move_line.credit
                beginning_balance += debit - credit
                beginning_balance_curr += account_move_line.amount_currency

        return beginning_balance, beginning_balance_curr

    def get_beginning_balance(self, account_id):
        balance = self.beginning_balance(account_id)
        return Decimal(balance[0]), Decimal(balance[1])

    def get_account(self, account_id):
        obj_account = self.pool.get("account.account")

        account = obj_account.browse(self.cr, self.uid, account_id)

        return account

    def get_general_ledger_line(self, account_id):
        running_balance = 0.00
        running_balance_curr = 0.00
        running_balance, running_balance_curr = self.beginning_balance(account_id)
        obj_account_move_line = self.pool.get("account.move.line")
        self.lines = []

        debit = 0.0
        credit = 0.0
        self.total_debit = 0.0
        self.total_credit = 0.0

        self.total_debit_currency = 0.0
        self.total_credit_currency = 0.0

        kriteria = self._prepare_line(account_id)

        account_move_line_ids = obj_account_move_line.search(
            self.cr, self.uid, kriteria, order="date"
        )

        if account_move_line_ids:
            account_move_line_id = obj_account_move_line.browse(
                self.cr, self.uid, account_move_line_ids
            )
            for account_move_line in account_move_line_id:
                debit_currency = 0.0
                credit_currency = 0.0
                debit = account_move_line.debit
                credit = account_move_line.credit

                if account_move_line.amount_currency > 0:
                    debit_currency = abs(account_move_line.amount_currency)
                else:
                    credit_currency = abs(account_move_line.amount_currency)

                self.total_debit += debit
                self.total_credit += credit
                self.total_debit_currency += debit_currency
                self.total_credit_currency += credit_currency
                running_balance += debit - credit
                running_balance_curr += debit_currency - credit_currency

                tahun = account_move_line.date[8:]
                bulan = account_move_line.date[5:7]
                tanggal = account_move_line.date[2:4]

                val = {
                    "date": tahun + "-" + bulan + "-" + tanggal,
                    "ref": account_move_line.ref,
                    "doc": account_move_line.move_id.name,
                    "description": account_move_line.name,
                    "partner": account_move_line.partner_id.name,
                    "debit": debit,
                    "credit": credit,
                    "debit_currency": debit_currency,
                    "credit_currency": credit_currency,
                    "running_balance": Decimal(running_balance),
                    "running_balance_curr": Decimal(running_balance_curr),
                }
                self.lines.append(val)

        return self.lines

    def get_total_debit(self):
        return self.total_debit

    def get_total_credit(self):
        return self.total_credit

    def get_total_debit_currency(self):
        return self.total_debit_currency

    def get_total_credit_currency(self):
        return self.total_credit_currency

    def get_period(self):
        data = self.localcontext["data"]["form"]
        start_period_name = (
            data["start_period_id"] and data["start_period_id"][1] or False
        )
        end_period_name = data["end_period_id"][1]
        nama_bulan = "-"

        if start_period_name and end_period_name:

            nama_bulan = start_period_name + " - " + end_period_name

        if not start_period_name and end_period_name:
            nama_bulan = "S/D " + end_period_name

        if start_period_name == end_period_name:
            nama_bulan = start_period_name

        return nama_bulan

    def get_company(self):
        data = self.localcontext["data"]["form"]
        company_name = data["company_id"] and data["company_id"][1] or False

        return company_name
