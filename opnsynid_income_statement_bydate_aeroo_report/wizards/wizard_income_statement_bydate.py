# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, osv
from openerp.tools.translate import _


class WizardIncomeStatementBydate(models.TransientModel):
    _name = 'account.wizard_income_statement_bydate'
    _description = 'Print Income Statement Based on Date Range'

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        required=True,
        default=_default_company_id,
    )
    date_start = fields.Date(
        string='Date Start',
        required=True,
    )
    date_end = fields.Date(
        string='Date End',
        required=True,
    )
    output_format = fields.Selection(
        string='Output Format',
        required=True,
        default='ods',
        selection=[
            ('xls', 'XLS'),
            ('ods', 'ODS')
        ])
    state = fields.Selection(
        string='State',
        selection=[
            ('all', 'All'),
            ('draft', 'Draft'),
            ('posted', 'Posted')
        ],
        required=True,
        default='posted',
    )

    def button_print_report(self, cr, uid, ids, data, context=None):
        datas = {}
        output_format = ''

        if context is None:
            context = {}

        datas['form'] = self.read(cr, uid, ids)[0]

        if datas['form']['output_format'] == 'xls':
            output_format = 'report_income_statement_bydate_xls'
        elif datas['form']['output_format'] == 'ods':
            output_format = 'report_income_statement_bydate_ods'
        else:
            err = 'Output Format cannot be empty'
            raise osv.except_osv(_('Warning'), _(err))

        return {
            'type': 'ir.actions.report.xml',
            'report_name': output_format,
            'datas': datas,
        }
