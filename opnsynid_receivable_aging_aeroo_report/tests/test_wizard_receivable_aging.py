# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime

from openerp.tests.common import TransactionCase


class TestWizardReceivableAging(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestWizardReceivableAging, self).setUp(*args, **kwargs)

        self.obj_wiz = self.env["account.wizard_report_receivable_aging"]

        self.company = self.env.user.company_id
        self.fiscal = self.env.ref("account.data_fiscalyear")
        self.journal_1 = self.env.ref("account.sales_journal")

    def _prepare_wizard(self):
        data = {
            "company_id": self.company.id,
            "fiscalyear_id": self.fiscal.id,
            "date_as_of": datetime.now().strftime("%Y-%m-%d"),
            "journal_ids": [(6, 0, [self.journal_1.id])],
        }
        return data

    def test_wizard_ods(self):
        data = self._prepare_wizard()
        data.update(
            {
                "output_format": "ods",
            }
        )

        wiz = self.obj_wiz.create(data)
        result = wiz.button_print_report()
        self.assertEqual(
            result.get("type"),
            "ir.actions.report.xml",
        )

    def test_wizard_xls(self):
        data = self._prepare_wizard()
        data.update(
            {
                "output_format": "xls",
            }
        )

        wiz = self.obj_wiz.create(data)
        result = wiz.button_print_report()
        self.assertEqual(
            result.get("type"),
            "ir.actions.report.xml",
        )
