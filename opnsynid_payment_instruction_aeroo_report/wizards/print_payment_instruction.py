# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from openerp import api, models, fields


class PrintPaymentInstruction(models.TransientModel):
    _name = "account.print_payment_instruction"
    _description = "Print Payment Instruction"

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.user.company_id.id,
    )
    date = fields.Date(
        string="Date",
        default=datetime.now().strftime("%Y-%m-%d"),
    )
    mode_id = fields.Many2one(
        string="Payment Mode",
        comodel_name="payment.mode",
        required=True,
    )
    output_format = fields.Selection(
        string='Output Format',
        required=True,
        selection=[
            ('xls', 'XLS'),
            ('ods', 'ODS')
        ],
        default='ods',
    )

    @api.multi
    def action_print(self):
        self.ensure_one()

        datas = {}
        output_format = ''

        datas['form'] = self.read()[0]

        if self.output_format == 'xls':
            output_format = 'payment_instruction_xls'
        elif self.output_format == 'ods':
            output_format = 'payment_instruction_ods'

        return {
            'type': 'ir.actions.report.xml',
            'report_name': output_format,
            'datas': datas,
        }
