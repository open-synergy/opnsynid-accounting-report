# -*- coding: utf-8 -*-
# Copyright 2015 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, fields, models


class WizardReportGeneralLedger(models.TransientModel):
    _name = "account.wizard_report_general_ledger"
    _description = "Wizard Report General Ledger"

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def _default_fiscalyear_id(self):
        obj_fiscalyear = self.env["account.fiscalyear"]

        fiscalyear_id = obj_fiscalyear.find()

        return fiscalyear_id or False

    @api.model
    def _default_end_period_id(self):
        obj_period = self.env["account.period"]

        period_ids = obj_period.find()

        return period_ids and period_ids[0] or False

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=_default_company_id,
    )

    fiscalyear_id = fields.Many2one(
        string="Fiscal Year",
        comodel_name="account.fiscalyear",
        required=True,
        default=_default_fiscalyear_id,
    )

    start_period_id = fields.Many2one(
        string="Start Period",
        comodel_name="account.period",
        required=True,
    )

    end_period_id = fields.Many2one(
        string="End Period",
        comodel_name="account.period",
        required=True,
        default=_default_end_period_id,
    )

    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        required=False,
        domain=[
            ("type", "!=", "view"),
            ("type", "!=", "consollidation"),
            ("type", "!=", "closed"),
        ],
    )

    account_ids = fields.Many2many(
        string="Accounts",
        comodel_name="account.account",
        rel="rel_wzd_general_ledger_2_acc",
        column1="wizard_id",
        column2="account_id",
        domain=[
            ("type", "!=", "view"),
            ("type", "!=", "consollidation"),
            ("type", "!=", "closed"),
        ],
    )

    in_foreign = fields.Boolean(string="In Foreign")

    output_format = fields.Selection(
        string="Output Format",
        required=True,
        selection=[("pdf", "PDF"), ("xls", "XLS"), ("ods", "ODS")],
        default="ods",
    )

    state = fields.Selection(
        string="State",
        selection=[("all", "All"), ("draft", "Draft"), ("posted", "Posted")],
        required=True,
        default="posted",
    )

    def button_print_report(self, cr, uid, ids, context=None):  # pylint: disable=R8110
        if context is None:
            context = {}

        datas = {}
        output_format = ""

        datas["form"] = self.read(cr, uid, ids)[0]

        if datas["form"]["output_format"] == "xls":
            output_format = "report_general_ledger_xls"
        elif datas["form"]["output_format"] == "ods":
            output_format = "report_general_ledger_ods"
        elif datas["form"]["output_format"] == "pdf":
            output_format = "report_general_ledger_pdf"

        return {
            "type": "ir.actions.report.xml",
            "report_name": output_format,
            "datas": datas,
        }
