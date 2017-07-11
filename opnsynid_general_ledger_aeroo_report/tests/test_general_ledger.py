# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class GeneralLedgerTest(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(GeneralLedgerTest, self).setUp(*args, **kwargs)

        self.obj_wiz = self.env['account.wizard_report_general_ledger']
        self.company = self.env.user.company_id

        self.fiscal = self.env.ref('account.data_fiscalyear')
        self.start_period = self.env.ref('account.period_1')
        self.end_period = self.env.ref('account.period_2')
        self.account_1 = self.env.ref('account.a_recv')

    def _prepare_wizard(self):
        data = {
            'company_id': self.company.id,
            'fiscalyear_id': self.fiscal.id,
            'start_period_id': self.start_period.id,
            'end_period_id': self.end_period.id,
            'account_ids': [(6, 0, [self.account_1.id])],
            'state': 'posted',
        }
        return data

    def test_wizard_ods(self):
        data = self._prepare_wizard()
        data.update({
            'output_format': 'ods',
        })

        wiz = self.obj_wiz.create(data)
        result = wiz.button_print_report()
        self.assertEqual(result.get('type'), 'ir.actions.report.xml',)

    def test_wizard_xls(self):
        data = self._prepare_wizard()
        data.update({
            'output_format': 'xls',
        })

        wiz = self.obj_wiz.create(data)
        result = wiz.button_print_report()
        self.assertEqual(result.get('type'), 'ir.actions.report.xml',)

    def test_wizard_pdf(self):
        data = self._prepare_wizard()
        data.update({
            'output_format': 'pdf',
        })

        wiz = self.obj_wiz.create(data)
        result = wiz.button_print_report()
        self.assertEqual(result.get('type'), 'ir.actions.report.xml',)
