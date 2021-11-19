# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time

from openerp.report import report_sxw


class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):  # pylint: disable=R8110
        super(Parser, self).__init__(cr, uid, name, context)
        self.list_mode = []
        self.list_payment = []
        self.dict_total = {}
        self.localcontext.update(
            {
                "time": time,
                "get_company": self._get_company,
                "get_mode": self._get_mode,
                "get_line": self._get_line,
                "get_total": self._get_total,
            }
        )

    def _get_company(self):
        data = self.localcontext["data"]["form"]
        company_name = data["company_id"] and data["company_id"][1] or False

        return company_name

    def _get_mode(self):
        data = self.localcontext["data"]["form"]
        mode_ids = data["mode_ids"]

        obj_mode = self.pool.get("payment.mode")

        for mode in obj_mode.browse(self.cr, self.uid, mode_ids):
            journal = mode.journal
            if mode.journal.type == "bank":
                source_type = "Bank"
            else:
                source_type = "Cash"
            if not journal.currency:
                currency = journal.company_id.currency_id.name
            else:
                currency = journal.currency.name

            res = {
                "id": mode.id,
                "name": mode.name,
                "source_type": source_type,
                "bank": mode.bank_id.bank_name or "-",
                "owner_name": mode.bank_id.owner_name or "-",
                "acc_number": mode.bank_id.acc_number or "-",
                "currency": currency,
            }
            self.list_mode.append(res)

        return self.list_mode

    def _get_line(self, mode_id):
        self.list_payment = []
        data = self.localcontext["data"]["form"]
        obj_line = self.pool.get("payment.line")
        date_start = data["date_start"]
        date_end = data["date_end"]
        state = []
        criteria = [
            ("order_id.mode", "=", mode_id),
        ]

        if data["state_draft"]:
            state.append("draft")
        if data["state_open"]:
            state.append("open")
        if data["state_done"]:
            state.append("done")
        if data["state_cancel"]:
            state.append("cancel")

        if len(state) > 0:
            criteria = [
                ("order_id.state", "in", state),
            ] + criteria

        if date_start:
            criteria = [
                ("date", ">=", date_start),
            ] + criteria

        if date_end:
            criteria = [
                ("date", "<=", date_end),
            ] + criteria

        line_ids = obj_line.search(self.cr, self.uid, criteria, order="date asc, id")

        no = 1
        for line in obj_line.browse(self.cr, self.uid, line_ids):
            res = {
                "no": no,
                "date": line.date,
                "order_ref": line.order_id.reference,
                "amount": line.amount_currency,
                "partner": line.partner_id.name,
                "acc_number": line.bank_id and line.bank_id.acc_number or "-",
                "bank": line.bank_id and line.bank_id.bank_name or "-",
                "owner_name": line.bank_id and line.bank_id.owner_name or "-",
                "communication": line.communication or "-",
            }
            self.list_payment.append(res)
            if not self.dict_total.get(mode_id, False):
                self.dict_total.update({mode_id: line.amount_currency})
            else:
                self.dict_total[mode_id] += line.amount_currency
            no += 1
        return self.list_payment

    def _get_total(self, mode_id):
        return self.dict_total.get(mode_id, 0.0)
