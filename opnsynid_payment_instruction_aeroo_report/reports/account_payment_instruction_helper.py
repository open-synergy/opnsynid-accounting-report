# -*- coding: utf-8 -*-
# © 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from openerp.tools import drop_view_if_exists


class AccountPaymentInstructionHelper(models.Model):

    _name = 'account.payment_instruction_helper'
    _description = 'Payment Instruction Helper'
    _auto = False

    @api.multi
    def _get_date(self):
        for record in self:
            payment_line = record.line_id

            order = payment_line.order_id
            if order.date_prefered == 'fixed':
                record.date = payment_line.date
            elif order.date_prefered == 'now':
                record.date = order.date_created
            else:
                if payment_line.ml_maturity_date:
                    record.date = payment_line.ml_maturity_date
                elif payment_line.ml_date_created:
                    record.date = payment_line.ml_date_created
                else:
                    record.date = order.date_created

    line_id = fields.Many2one(
        string='Payment Lines',
        comodel_name='payment.line'
    )

    date = fields.Date(
        string="Date"
    )

    def init(self, cr):
        drop_view_if_exists(cr, 'account_payment_instruction_helper')
        strSQL = """
            CREATE OR REPLACE VIEW account_payment_instruction_helper AS (
                SELECT
                    row_number() OVER() as id,
                    A.id AS line_id,
                    CASE
                        WHEN B.date_prefered = 'fixed'
                            THEN B.date_scheduled
                        WHEN B.date_prefered = 'now'
                            THEN B.date_created
                        ELSE
                            CASE
                            WHEN C.date_maturity IS NOT NULL
                                THEN C.date_maturity
                            WHEN C.date IS NOT NULL
                                THEN C.date
                            ELSE
                                B.date_created
                            END
                    END AS date
                    FROM payment_line AS A
                    JOIN payment_order AS B ON A.order_id = B.id
                    LEFT JOIN account_move_line AS C
                        ON A.move_line_id = C.id
            )
        """
        cr.execute(strSQL)
