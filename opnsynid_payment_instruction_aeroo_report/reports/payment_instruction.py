# -*- coding: utf-8 -*-
# © 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time
from datetime import datetime
from openerp.report import report_sxw


class Parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.data_list = []
        self.localcontext.update({
            "time": time,
            "get_company": self._get_company,
            "get_mode": self._get_mode,
            "get_date": self._get_date,
            "get_line": self._get_line,
        })

    def _get_company(self):
        data = self.localcontext["data"]["form"]
        company_name = data["company_id"] and data["company_id"][1] or False

        return company_name

    def _get_date(self):
        data = self.localcontext["data"]["form"]
        date = data["date"] or False

        conv_date = datetime.strptime(
            date, '%Y-%m-%d').strftime('%d/%m/%Y')

        return conv_date

    def _get_mode(self):
        data = self.localcontext["data"]["form"]
        mode = data["mode_id"] and data["mode_id"][1] or False

        return mode

    def _get_line(self):
        res = {}
        obj_line = self.pool.get("account.payment_instruction_lines")

        date = self.localcontext["data"]["form"]["date"]
        mode_id = self.localcontext["data"]["form"]["mode_id"][0]

        criteria = [
            ("date", "=", date),
            ("mode_id", "=", mode_id)
        ]

        line_ids = obj_line.search(self.cr, self.uid, criteria)

        no = 1
        for line in obj_line.browse(
            self.cr, self.uid, line_ids):
            res = {
                "no": no,
                "date": line.date,
                "mode": line.mode_id.name,
                "partner": line.partner_id.name,
                "currency": line.currency_id.name,
                "amount_currency": line.amount_currency
            }
            self.data_list.append(res)
            no += 1

        return self.data_list
