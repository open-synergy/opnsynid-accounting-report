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


from openerp.osv import osv, fields
from openerp.tools.translate import _


class wizard_report_general_ledger(osv.osv_memory):
    _name = 'account.wizard_report_general_ledger'
    _description = 'Wizard Report General Ledger'

    def default_company_id(self, cr, uid, context=None):
        obj_user = self.pool.get('res.users')

        user = obj_user.browse(cr, uid, [uid])[0]

        return user.company_id and user.company_id.id or False

    def default_fiscalyear_id(self, cr, uid, context=None):
        obj_fiscalyear = self.pool.get('account.fiscalyear')

        fiscalyear_id = obj_fiscalyear.find(cr, uid)

        return fiscalyear_id or False

    def default_end_period_id(self, cr, uid, context=None):
        obj_period = self.pool.get('account.period')

        period_ids = obj_period.find(cr, uid)

        return period_ids and period_ids[0] or False

    def default_state(self, cr, uid, context=None):
        return 'posted'
        
    def default_output(self, cr, uid, context=None):
        return 'ods'

    _columns = {
        'company_id': fields.many2one(
            string='Company',
            obj='res.company',
            required=True),
        'fiscalyear_id': fields.many2one(
            string='Fiscal Year',
            obj='account.fiscalyear',
            required=True),
        'start_period_id': fields.many2one(
            string='Start Period',
            obj='account.period',
            required=True),
        'end_period_id': fields.many2one(
            string='Start Period',
            obj='account.period',
            required=True),
        'account_id': fields.many2one(
            string='Account',
            obj='account.account',
            required=True,
            domain=[
                ('type', '!=', 'view'),
                ('type', '!=', 'consollidation'),
                ('type', '!=', 'closed')
            ]),
        'in_foreign': fields.boolean(string='In Foreign'),
        'output_format': fields.selection(
            string='Output Format',
            required=True,
            selection=[
                ('pdf', 'PDF'),
                ('xls', 'XLS'),
                ('ods', 'ODS')
            ]),
        'state': fields.selection(
            string='State',
            selection=[
                ('all', 'All'),
                ('draft', 'Draft'),
                ('posted', 'Posted')
            ],
            required=True),
    }

    _defaults = {
        'company_id': default_company_id,
        'fiscalyear_id': default_fiscalyear_id,
        'end_period_id': default_end_period_id,
        'state': default_state,
        'output_format': default_output
    }

    def button_print_report(self, cr, uid, ids, data, context=None):
        datas = {}
        output_format = ''

        if context is None:
            context = {}

        datas['form'] = self.read(cr, uid, ids)[0]

        if datas['form']['output_format'] == 'xls':
            output_format = 'report_general_ledger_xls'
        elif datas['form']['output_format'] == 'ods':
            output_format = 'report_general_ledger_ods'
        elif datas['form']['output_format'] == 'pdf':
            output_format = 'report_general_ledger_pdf'
        else:
            err = 'Output Format cannot be empty'
            raise osv.except_osv(_('Warning'), _(err))

        return {
            'type': 'ir.actions.report.xml',
            'report_name': output_format,
            'datas': datas,
        }
