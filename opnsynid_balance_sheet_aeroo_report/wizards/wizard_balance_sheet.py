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
from openerp import models, fields, api


class WizardBalanceSheet(models.Model):
    _name = 'account.wizard_balance_sheet'
    _description = 'Print Balance Sheet'

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def _default_fiscalyear_id(self, cr, uid, context={}):
        fiscalyear_id = self.env['account.fiscalyear'].find(
            self.env.cr,
            self.env.uid
            )

        return fiscalyear_id or False

    @api.model
    def _default_period_id(self):
        period_ids = self.env['account.period'].find(
            self.env.cr,
            self.env.uid)

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
