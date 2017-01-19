# -*- coding: utf-8 -*-
# © 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from openerp.tools import drop_view_if_exists
from datetime import datetime


class AccountPaymentInstructionLines(models.Model):

    _name = 'account.payment_instruction_lines'
    _description = 'Payment Instruction Lines'
    _auto = False

    date = fields.Date(
        string="Date"
    )

    mode_id = fields.Many2one(
        string='Payment Mode',
        comodel_name='payment.mode'
    )

    partner_id = fields.Many2one(
        string='Partner',
        comodel_name='res.partner'
    )
    currency_id = fields.Many2one(
        string='Currency',
        comodel_name='res.currency'
    )

    amount_currency = fields.Float(
        string="Amount in Partner Currency",
        digits=(16, 2)
    )

    def init(self, cr):
        drop_view_if_exists(cr, 'account_payment_instruction_lines')
        strSQL = """
            CREATE OR REPLACE VIEW account_payment_instruction_lines AS (
                SELECT
                    row_number() OVER() as id,
                    A.date AS date,
                    C.mode AS mode_id,
                    B.partner_id AS partner_id,
                    B.currency AS currency_id,
                    SUM(B.amount_currency) AS amount_currency
                    FROM account_payment_instruction_helper AS A
                    JOIN payment_line AS B ON A.line_id = B.id
                    JOIN payment_order AS C ON B.order_id = C.id
                    WHERE C.state = 'open'
                    GROUP BY A.date, C.mode, B.partner_id, B.currency
            )
        """
        cr.execute(strSQL)
