# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class WizardReportGeneralLedger(models.TransientModel):
    _inherit = "account.wizard_report_general_ledger"

    operating_unit_ids = fields.Many2many(
        string="Operating Unit(s)",
        comodel_name="operating.unit",
        rel="rel_wzd_general_ledger_2_ou",
        column1="wizard_id",
        column2="operating_unit_id",
    )
