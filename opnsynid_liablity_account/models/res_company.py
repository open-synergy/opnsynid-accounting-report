# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2015 Andhitia Rama. All rights reserved.
#    @author Andhitia Rama
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

from openerp import models, fields


class res_company(models.Model):
    """override company to add liablity account"""
    _inherit = 'res.company'
    _name = 'res.company'

    liablity_ids = fields.Many2many(
        string='Liabilities',
        comodel_name='account.account',
        relation='rel_company_2_liablity_acc',
        column1='company_id',
        column2='account_id',
        )
