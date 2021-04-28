# -*- coding: utf-8 -*-
# © 2015 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, osv
from openerp.tools.translate import _


class WizardBalanceSheet(models.TransientModel):
    _name = 'account.wizard_balance_sheet'
    _description = 'Print Balance Sheet'

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def _default_fiscalyear_id(self):
        fiscalyear_id = self.env['account.fiscalyear'].find()
        return fiscalyear_id or False

    @api.model
    def _default_period_id(self):
        period_ids = self.env['account.period'].find()
        return period_ids and period_ids[0] or False

    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        required=True,
        default=_default_company_id,
    )
    fiscalyear_id = fields.Many2one(
        string='Fiscal Year',
        comodel_name='account.fiscalyear',
        required=True,
        default=_default_fiscalyear_id,
    )
    period_id = fields.Many2one(
        string='Period',
        comodel_name='account.period',
        required=True,
        default=_default_period_id,
    )
    output_format = fields.Selection(
        string='Output Format',
        required=True,
        default='ods',
        selection=[
            ('xls', 'XLS'),
            ('ods', 'ODS')
        ])
    show_zero = fields.Boolean(
        string="Show Zero Balance",
        default=True,
    )
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
            output_format = 'report_balance_sheet_xls'
        elif datas['form']['output_format'] == 'ods':
            output_format = 'report_balance_sheet_ods'
        else:
            err = 'Output Format cannot be empty'
            raise osv.except_osv(_('Warning'), _(err))

        return {
            'type': 'ir.actions.report.xml',
            'report_name': output_format,
            'datas': datas,
        }
