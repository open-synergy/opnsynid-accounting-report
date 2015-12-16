# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api, osv
from openerp.tools.translate import _


class WizardIncomeStatement(models.Model):
    _name = 'account.wizard_income_statement'
    _description = 'Print Income Statement'

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
            output_format = 'report_income_statement_xls'
        elif datas['form']['output_format'] == 'ods':
            output_format = 'report_income_statement_ods'
        else:
            err = 'Output Format cannot be empty'
            raise osv.except_osv(_('Warning'), _(err))

        return {
            'type': 'ir.actions.report.xml',
            'report_name': output_format,
            'datas': datas,
        }
