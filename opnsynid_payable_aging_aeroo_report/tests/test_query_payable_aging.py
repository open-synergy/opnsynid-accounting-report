# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from datetime import datetime, date


class TestQueryPayableAging(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestQueryPayableAging, self).setUp(*args, **kwargs)

        self.obj_query = self.env['account.query_payable_aging']
        self.obj_invoice = self.env['account.invoice']
        self.obj_move = self.env['account.move']
        self.obj_move_line = self.env['account.move.line']
        self.obj_bank_stmt = self.env['account.bank.statement']
        self.obj_bank_stmt_line = self.registry('account.bank.statement.line')

        self.journal_1 = self.env.ref('account.sales_journal')
        self.bank_journal_1 = self.env.ref('account.bank_journal')
        self.partner_1 = self.env.ref('base.res_partner_2')
        self.currency_1 = self.env.ref('base.EUR')
        self.company = self.env.user.company_id.id
        self.account = self.env.ref('account.a_pay')
        self.product_1 = self.env.ref('product.product_product_3')
        self.product_2 = self.env.ref('product.product_product_5')

        self.period = self.env.ref('account.period_2')
        self.date_now = self.period.date_start

        self.date_payment = date.fromordinal(
            datetime.strptime(
                self.date_now, '%Y-%m-%d').toordinal() + 3)

        self.date_payment_2 = date.fromordinal(
            datetime.strptime(
                self.date_now, '%Y-%m-%d').toordinal() + 40)

        self.date_due = date.fromordinal(
            datetime.strptime(
                self.date_now, '%Y-%m-%d').toordinal() + 7)

    def _prepare_invoice(self):
        data = {
            'name': 'Supplier Invoice - A',
            'journal_id': self.journal_1.id,
            'partner_id': self.partner_1.id,
            'currency_id': self.currency_1.id,
            'company_id': self.company,
            'account_id': self.account.id,
            'date_invoice': self.date_now,
            'date_due': self.date_due,
            'type': 'in_invoice',
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

    def _prepare_bank_statement(self):
        data = {
            'journal_id': self.bank_journal_1.id,
            'date': self.date_payment
        }
        return data

    def _prepare_bank_statement_line(self, bank_stmt_id):
        data = {
            'name': 'First Payment',
            'statement_id': bank_stmt_id,
            'partner_id': self.partner_1.id,
            'amount': -150,
            'currency_id': self.currency_1.id,
            'date': self.date_payment
        }
        return data

    def _prepare_bank_statement_2(self):
        data = {
            'journal_id': self.bank_journal_1.id,
            'date': self.date_payment_2
        }
        return data

    def _prepare_bank_statement_line_2(self, bank_stmt_id):
        data = {
            'name': 'Second Payment',
            'statement_id': bank_stmt_id,
            'partner_id': self.partner_1.id,
            'amount': -70,
            'currency_id': self.currency_1.id,
            'date': self.date_payment_2
        }
        return data

    def test_query_payable_aging_1(self):
        # Condition : No Payment

        # Create Invoice
        data = self._prepare_invoice()
        inv = self.obj_invoice.create(data)
        inv.signal_workflow('invoice_open')

        # Search Move
        move_id = self.obj_move.search(
            [('ref', '=', 'Supplier Invoice - A')]
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
        self.assertEqual(query.aging1, 510.0)
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
        self.assertEqual(query.aging2, 510.0)
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
        self.assertEqual(query.aging3, 510.0)
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
        self.assertEqual(query.aging4, 510.0)
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
        self.assertEqual(query.aging5, 510.0)

    def test_query_payable_aging_2(self):
        cr, uid = self.cr, self.uid
        # Condition : Half Payment

        # Create Invoice
        data_invoice = self._prepare_invoice()
        inv = self.obj_invoice.create(data_invoice)

        inv.signal_workflow('invoice_open')

        # Search Move
        move_id = self.obj_move.search(
            [('ref', '=', 'Supplier Invoice - A')]
        )
        # Check Move
        self.assertIsNotNone(move_id)

        # Search Query

        query_id = self.obj_query.search(
            [('move_id', '=', move_id.id)]
        )
        # Check Query
        self.assertEqual(query_id.move_id.name, move_id.name)

        # Create Payment
        data_bank_stmt = self._prepare_bank_statement()
        bank_stmt_id = self.obj_bank_stmt.create(data_bank_stmt).id

        # Check Payment
        self.assertIsNotNone(bank_stmt_id)

        # Create Payment Line
        data_bank_stmt_line = self._prepare_bank_statement_line(bank_stmt_id)
        bank_stmt_line_id = self.obj_bank_stmt_line.create(
            cr, uid, data_bank_stmt_line)

        # Check Payment Line
        self.assertIsNotNone(bank_stmt_line_id)

        # Create reconcile the payment with the invoice
        for l in inv.move_id.line_id:
            if l.account_id.id == self.account.id:
                line_id = l
                break

        self.obj_bank_stmt_line.process_reconciliation(
            cr, uid, bank_stmt_line_id, [{
                'counterpart_move_line_id': line_id.id,
                'credit': 0,
                'debit': 150,
                'name': line_id.name, }])

        # Create Payment 2
        data_bank_stmt_2 = self._prepare_bank_statement_2()
        bank_stmt_id_2 = self.obj_bank_stmt.create(data_bank_stmt_2).id

        # Check Payment 2
        self.assertIsNotNone(bank_stmt_id_2)

        # Create Payment Line 2
        data_bank_stmt_line_2 = self._prepare_bank_statement_line_2(
            bank_stmt_id_2)
        bank_stmt_line_id_2 = self.obj_bank_stmt_line.create(
            cr, uid, data_bank_stmt_line_2)

        # Check Payment Line
        self.assertIsNotNone(bank_stmt_line_id_2)

        # Create reconcile the payment with the invoice
        for l in inv.move_id.line_id:
            if l.account_id.id == self.account.id:
                line_id = l
                break

        self.obj_bank_stmt_line.process_reconciliation(
            cr, uid, bank_stmt_line_id_2, [{
                'counterpart_move_line_id': line_id.id,
                'credit': 0,
                'debit': 70,
                'name': line_id.name, }])

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
        self.assertEqual(query.aging1, 360.0)
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
        self.assertEqual(query.aging2, 360.0)
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
        self.assertEqual(query.aging3, 290.0)
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
        self.assertEqual(query.aging4, 290.0)
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
        self.assertEqual(query.aging5, 290.0)
