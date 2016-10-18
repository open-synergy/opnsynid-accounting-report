# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time
from openerp.report import report_sxw


class Parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.list_journal = []
        self.list_line = []
        self.dict_total = {}
        self.localcontext.update({
            "time": time,
            "get_company": self._get_company,
            "get_journal": self._get_journal,
            "get_line": self._get_line,
            "get_total": self._get_total,
            "get_beginning_balance": self._get_beginning_balance,
        })

    def _get_company(self):
        data = self.localcontext['data']['form']
        company_name = data['company_id'] and data['company_id'][1] or False

        return company_name

    def _get_journal(self):
        data = self.localcontext["data"]["form"]
        journal_ids = data["journal_ids"]

        obj_journal = self.pool.get("account.journal")
        obj_bank = self.pool.get("res.partner.bank")

        for journal in obj_journal.browse(
                self.cr, self.uid, journal_ids):
            if not journal.currency:
                currency = journal.company_id.currency_id.name
            else:
                currency = journal.currency.name

            bank = False
            criteria = [
                ("journal_id", "=", journal.id),
            ]
            bank_ids = obj_bank.search(
                self.cr, self.uid, criteria)

            if bank_ids:
                bank = obj_bank.browse(
                    self.cr, self.uid, bank_ids)[0]

            res = {
                "id": journal.id,
                "name": journal.name,
                "bank": bank and bank.bank_name or "-",
                "owner_name": bank and bank.owner_name or "-",
                "acc_number": bank and bank.acc_number or "-",
                "currency": currency,
            }
            self.list_journal.append(res)

        return self.list_journal

    def _prepare_domain(
            self, journal_id,
            date_start=False, date_end=False):
        data = self.localcontext["data"]["form"]
        date_start = data["date_start"]
        date_end = data["date_end"]
        criteria = [
            ("journal_id", "=", journal_id)
        ]
        if date_start:
            criteria = [
                ("date", ">=", date_start),
            ] + criteria

        if date_end:
            criteria = [
                ("date", ">=", date_end),
            ] + criteria
        state = []

        if data["state_draft"]:
            state.append("draft")
        if data["state_open"]:
            state.append("open")
        if data["state_confirm"]:
            state.append("confirm")

        if len(state) > 0:
            criteria = [
                ("state", "in", state),
            ] + criteria

        return criteria

    def _get_statement(
            self, journal_id,
            date_start=False, date_end=False,
            sort="asc"):
        statement = False
        sort = "date " + sort
        obj_statement = self.pool.get("account.bank.statement")
        criteria = self._prepare_domain(
            journal_id, date_start, date_end)
        statement_ids = obj_statement.search(
            self.cr, self.uid, criteria, limit=1,
            order=sort)
        if statement_ids:
            statement = obj_statement.browse(
                self.cr, self.uid, statement_ids)[0]
        return statement

    def _get_beginning_balance(
            self, journal_id):
        data = self.localcontext["data"]["form"]
        date_start = data["date_start"]
        date_end = data["date_end"]
        result = 0.0
        statement = self._get_statement(
            journal_id, date_start, date_end)
        if statement:
            result = statement.balance_start
        self.dict_total.update({journal_id: result})
        return result

    def _get_line(self, journal_id):
        self.list_line = []
        data = self.localcontext["data"]["form"]
        obj_line = self.pool.get("account.bank.statement.line")
        date_start = data["date_start"]
        date_end = data["date_end"]
        state = []
        criteria = [
            ("statement_id.journal_id", "=", journal_id),
        ]

        if data["state_draft"]:
            state.append("draft")
        if data["state_open"]:
            state.append("open")
        if data["state_confirm"]:
            state.append("confirm")

        if len(state) > 0:
            criteria = [
                ("statement_id.state", "in", state),
            ] + criteria

        if date_start:
            criteria = [
                ("date", ">=", date_start),
            ] + criteria

        if date_end:
            criteria = [
                ("date", "<=", date_end),
            ] + criteria

        line_ids = obj_line.search(
            self.cr, self.uid, criteria, order="date asc, id")

        no = 1
        for line in obj_line.browse(
                self.cr, self.uid, line_ids):
            if not self.dict_total.get(journal_id, False):
                self.dict_total.update({journal_id: line.amount})
            else:
                self.dict_total[journal_id] += line.amount
            res = {
                "no": no,
                "date": line.date,
                "statement_ref": line.statement_id.name,
                "amount": line.amount,
                "partner": line.partner_id and line.partner_id.name or "-",
                "name": line.name,
                "running_balance": self._get_total(journal_id),
            }
            self.list_line.append(res)
            no += 1
        return self.list_line

    def _get_total(self, journal_id):
        return self.dict_total.get(journal_id, 0.0)
