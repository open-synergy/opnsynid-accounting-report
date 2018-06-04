# -*- coding: utf-8 -*-
# © 2015 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time
from datetime import date
from openerp.report import report_sxw
from decimal import Decimal


class Parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.lines = []
        self.total_debit = 0.0
        self.total_credit = 0.0
        self.localcontext.update({
            "time": time,
            "get_account": self.get_account,
            "line": self.get_general_ledger_line,
            "get_period": self.get_period,
            "get_company": self.get_company,
            "total_debit": self.get_total_debit,
            "total_credit": self.get_total_credit,
            "beginning_balance": self.get_beginning_balance,
        })

    def get_opening_balance(self, account_id, state, date_start_period):
        opening_balance = 0.00
        obj_account_period = self.pool.get("account.period")
        obj_account_move_line = self.pool.get("account.move.line")

        kriteria_opening_balance = [
            ("date_start", "=", date_start_period),
            ("special", "=", 1)
        ]

        period_ids = obj_account_period.search(
            self.cr, self.uid, kriteria_opening_balance)

        period = obj_account_period.browse(
            self.cr, self.uid, period_ids)[0]

        kriteria = [
            ("account_id", "=", account_id),
            ("period_id", "=", period.id)
        ]
        if state != "all":
            kriteria.append(("move_id.state", "=", state))

        account_move_line_ids = obj_account_move_line.search(
            self.cr, self.uid, kriteria)

        if account_move_line_ids:
            account_move_line_id = obj_account_move_line.browse(
                self.cr, self.uid, account_move_line_ids)

            for account_move_line in account_move_line_id:
                debit = account_move_line.debit
                credit = account_move_line.credit
                opening_balance += (debit - credit)

        return opening_balance

    def beginning_balance(self, account_id):
        beginning_balance = 0.00
        obj_account_move_line = self.pool.get("account.move.line")
        obj_account_period = self.pool.get("account.period")
        obj_account_fiscalyear = self.pool.get("account.fiscalyear")

        data = self.localcontext["data"]["form"]

        start_period_id = data["start_period_id"]\
            and data["start_period_id"][0] or False
        end_period_id = data["end_period_id"]\
            and data["end_period_id"][0] or False

        fiscalyear_id = data["fiscalyear_id"]\
            and data["fiscalyear_id"][0] or False

        state = data["state"]

        if start_period_id:
            period_id = start_period_id
        else:
            period_id = end_period_id

        period = obj_account_period.browse(
            self.cr, self.uid, period_id)

        fiscalyear = obj_account_fiscalyear.browse(
            self.cr, self.uid, fiscalyear_id)

        beginning_balance = 0.0

        if period.date_start == fiscalyear.date_start or not start_period_id:
            opening_balance = self.get_opening_balance(
                account_id, state, fiscalyear.date_start)
            return opening_balance
        else:
            tahun = int(period.date_start[0:4])
            bulan = int(period.date_start[5:7])
            hari = int(period.date_start[8:10])

            tanggal = date(tahun, bulan, hari)

            ord_tanggal_awal = tanggal.toordinal() - 1
            tanggal_awal = date.fromordinal(ord_tanggal_awal)

            kriteria = [
                ("account_id", "=", account_id),
                ("date", ">=", fiscalyear.date_start),
                ("date", "<=", str(tanggal_awal))
            ]
            if state != "all":
                kriteria.append(("move_id.state", "=", state))

        account_move_line_ids = obj_account_move_line.search(
            self.cr, self.uid, kriteria)

        if account_move_line_ids:
            account_move_line_id = obj_account_move_line.browse(
                self.cr, self.uid, account_move_line_ids)

            for account_move_line in account_move_line_id:
                debit = account_move_line.debit
                credit = account_move_line.credit
                beginning_balance += (debit - credit)

        return beginning_balance

    def get_beginning_balance(self, account_id):
        beginning_balance = self.beginning_balance(account_id)
        return Decimal(beginning_balance)

    def get_account(self, account_id):
        obj_account = self.pool.get("account.account")

        account = obj_account.browse(
            self.cr, self.uid, account_id)

        return account

    def get_general_ledger_line(self, account_id):
        running_balance = 0.00
        running_balance = self.beginning_balance(account_id)
        obj_account_move_line = self.pool.get("account.move.line")
        obj_account_period = self.pool.get("account.period")
        obj_account_fiscalyear = self.pool.get("account.fiscalyear")
        self.lines = []

        data = self.localcontext["data"]["form"]

        start_period_id = data["start_period_id"]\
            and data["start_period_id"][0] or False
        end_period_id = data["end_period_id"][0]\
            and data["end_period_id"][0] or False
        state = data["state"]

        debit = 0.0
        credit = 0.0
        self.total_debit = 0.0
        self.total_credit = 0.0

        if start_period_id and end_period_id:
            if start_period_id == end_period_id:
                kriteria = [
                    ("account_id", "=", account_id),
                    ("period_id", "=", start_period_id),
                ]
            else:
                kriteria = [
                    ("account_id", "=", account_id),
                    ("period_id", ">=", start_period_id),
                    ("period_id", "<=", end_period_id),
                ]
        if state != "all":
            kriteria.append(("move_id.state", "=", state))

        if not start_period_id and end_period_id:
            period = obj_account_period.browse(
                self.cr, self.uid, end_period_id)
            fiscalyear = obj_account_fiscalyear.browse(
                self.cr, self.uid, period.fiscalyear_id.id)

            period_kriteria = obj_account_period.find(
                self.cr, self.uid, fiscalyear.date_start, {
                    "account_period_prefer_normal": True
                })

            kriteria = [
                ("account_id", "=", account_id),
                ("period_id", ">=", int(period_kriteria[0])),
                ("period_id", "<=", end_period_id),
            ]
        if state != "all":
            kriteria.append(("move_id.state", "=", state))

        account_move_line_ids = obj_account_move_line.search(
            self.cr, self.uid, kriteria, order="date")

        if account_move_line_ids:
            account_move_line_id = obj_account_move_line.browse(
                self.cr, self.uid, account_move_line_ids)
            for account_move_line in account_move_line_id:
                debit = account_move_line.debit
                credit = account_move_line.credit

                self.total_debit += debit
                self.total_credit += credit
                running_balance += debit - credit

                tahun = account_move_line.date[8:]
                bulan = account_move_line.date[5:7]
                tanggal = account_move_line.date[2:4]

                val = {
                    "date": tahun + "-" + bulan + "-" + tanggal,
                    "ref": account_move_line.ref,
                    "doc": account_move_line.move_id.name,
                    "description": account_move_line.name,
                    "debit": debit,
                    "credit": credit,
                    "running_balance": Decimal(running_balance)
                }
                self.lines.append(val)

        return self.lines

    def get_total_debit(self):
        return self.total_debit

    def get_total_credit(self):
        return self.total_credit

    def get_period(self):
        data = self.localcontext["data"]["form"]
        start_period_name = data["start_period_id"]\
            and data["start_period_id"][1] or False
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
