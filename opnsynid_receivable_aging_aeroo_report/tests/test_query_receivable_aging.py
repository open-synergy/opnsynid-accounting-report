# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from datetime import datetime, date


class TestQueryReceivableAging(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestQueryReceivableAging, self).setUp(*args, **kwargs)

        self.obj_query = self.env['account.query_receivable_aging']
        self.obj_invoice = self.env['account.invoice']
        self.obj_move = self.env['account.move']

        self.journal_1 = self.env.ref('account.sales_journal')
        self.partner_1 = self.env.ref('base.res_partner_2')
        self.currency_1 = self.env.ref('base.IDR')
        self.company = self.env.user.company_id.id
        self.account = self.env.ref('account.a_recv')
        self.product_1 = self.env.ref('product.product_product_3')
        self.product_2 = self.env.ref('product.product_product_5')

        self.date_now = datetime.now().strftime('%Y-%m-%d')
        self.date_due = date.fromordinal(
            datetime.strptime(
                self.date_now, '%Y-%m-%d').toordinal() + 7)

    def _prepare_invoice(self):
        data = {
            'name': 'Customer Invoice - A',
            'journal_id': self.journal_1.id,
            'partner_id': self.partner_1.id,
            'currency_id': self.currency_1.id,
            'company_id': self.company,
            'account_id': self.account.id,
            'date_invoice': self.date_now,
            'date_due': self.date_due,
            'type': 'out_invoice',
            'invoice_line': [
                (0, 0, {'product_id': self.product_1.id,
                        'uos_id': 1,
                        'quantity': 1.0,
                        'price_unit': 10.0,
                        'name': 'Basic PC',
                        'account_id': self.account.id}),
                (0, 0, {'product_id': self.product_2.id,
                        'uos_id': 1,
                        'quantity': 5.0,
                        'price_unit': 100.0,
                        'name': 'PC On Demand',
                        'account_id': self.account.id})
            ]
        }
        return data

    def test_query_receivable_aging(self):
        data = self._prepare_invoice()
        inv = self.obj_invoice.create(data)
        inv.signal_workflow('invoice_open')

        # Search Move
        move_id = self.obj_move.search(
            [('ref', '=', 'Customer Invoice - A')]
        )
        # Check Move
        self.assertIsNotNone(move_id)

        # Search Query

        query_id = self.obj_query.search(
            [('move_id', '=', move_id.id)]
        )
        # Check Query
        self.assertEqual(query_id.move_id.name, move_id.name)

        # Check Aging
        # Condition : Period Length = 30

        # Aging1 0-30
        date_as_of_1 = date.fromordinal(
            self.date_due.toordinal() + 1)

        query = self.obj_query.with_context(
            period_length=30, date_as_of=str(date_as_of_1)
        ).browse(query_id.id)[0]
        self.assertNotEqual(query.aging1, 0.0)
        self.assertEqual(query.aging2, 0.0)
        self.assertEqual(query.aging3, 0.0)
        self.assertEqual(query.aging4, 0.0)
        self.assertEqual(query.aging5, 0.0)

        # Aging2 31-60
        date_as_of_2 = date.fromordinal(
            self.date_due.toordinal() + 31)

        query = self.obj_query.with_context(
            period_length=30, date_as_of=str(date_as_of_2)
        ).browse(query_id.id)[0]
        self.assertEqual(query.aging1, 0.0)
        self.assertNotEqual(query.aging2, 0.0)
        self.assertEqual(query.aging3, 0.0)
        self.assertEqual(query.aging4, 0.0)
        self.assertEqual(query.aging5, 0.0)

        # Aging3 61-90
        date_as_of_3 = date.fromordinal(
            self.date_due.toordinal() + 61)

        query = self.obj_query.with_context(
            period_length=30, date_as_of=str(date_as_of_3)
        ).browse(query_id.id)[0]
        self.assertEqual(query.aging1, 0.0)
        self.assertEqual(query.aging2, 0.0)
        self.assertNotEqual(query.aging3, 0.0)
        self.assertEqual(query.aging4, 0.0)
        self.assertEqual(query.aging5, 0.0)

        # Aging4 91-120
        date_as_of_4 = date.fromordinal(
            self.date_due.toordinal() + 91)

        query = self.obj_query.with_context(
            period_length=30, date_as_of=str(date_as_of_4)
        ).browse(query_id.id)[0]
        self.assertEqual(query.aging1, 0.0)
        self.assertEqual(query.aging2, 0.0)
        self.assertEqual(query.aging3, 0.0)
        self.assertNotEqual(query.aging4, 0.0)
        self.assertEqual(query.aging5, 0.0)

        # Aging5 +120
        date_as_of_5 = date.fromordinal(
            self.date_due.toordinal() + 121)

        query = self.obj_query.with_context(
            period_length=30, date_as_of=str(date_as_of_5)
        ).browse(query_id.id)[0]
        self.assertEqual(query.aging1, 0.0)
        self.assertEqual(query.aging2, 0.0)
        self.assertEqual(query.aging3, 0.0)
        self.assertEqual(query.aging4, 0.0)
        self.assertNotEqual(query.aging5, 0.0)
