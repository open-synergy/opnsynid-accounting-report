# -*- coding: utf-8 -*-
# © 2015 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ResCompany(models.Model):
    """override company to add asset account"""

    _inherit = "res.company"
    _name = "res.company"

    asset_ids = fields.Many2many(
        string="Assets",
        comodel_name="account.account",
        relation="rel_company_2_asset_acc",
        column1="company_id",
        column2="account_id",
    )
