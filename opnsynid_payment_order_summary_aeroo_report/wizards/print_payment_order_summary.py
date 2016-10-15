# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models, fields


class PrintPaymentOrderSummary(models.TransientModel):
    _name = "account.print_payment_order_summary"
    _description = "Print Payment Order Summary"

    date_start = fields.Date(
        string="Date Start",
        )
    date_end = fields.Date(
        string="Date End",
        )
    mode_ids = fields.Many2many(
        string="Payment Mode",
        comodel_name="payment.mode",
        )
    output_format = fields.Selection(
        string='Output Format',
        required=True,
        selection=[
            ('pdf', 'PDF'),
            ('xls', 'XLS'),
            ('ods', 'ODS')
        ],
        default='ods',
        )

    @api.multi
    def action_print(self):
        self.ensure_one()
        self.do_something_useful()
