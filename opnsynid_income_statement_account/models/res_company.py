# -*- coding: utf-8 -*-
# © 2015 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResCompany(models.Model):
    """override company to add income statement account"""
    _inherit = "res.company"
    _name = "res.company"

    income_statement_ids = fields.Many2many(
        string="Income Statement",
        comodel_name="account.account",
        relation="rel_company_2_is_acc",
        column1="company_id",
        column2="account_id",
        )
