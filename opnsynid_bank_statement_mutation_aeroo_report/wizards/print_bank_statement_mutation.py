# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from openerp import api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class PrintBankStatementMutation(models.TransientModel):
    _name = "account.print_bank_statement_mutation"
    _description = "Print Bank Statement Mutation"

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.user.company_id.id,
    )
    date_start = fields.Date(
        string="Date Start",
        default=datetime.now().strftime("%Y-%m-%d"),
    )
    date_end = fields.Date(
        string="Date End",
    )
    journal_ids = fields.Many2many(
        string="Bank",
        comodel_name="account.journal",
        domain=[("type", "=", "bank")],
        required=True,
        rel="rel_bank_statement_mutation_2_journal",
        column1="wizard_id",
        column2="journal_id",
    )
    state_draft = fields.Boolean(
        string="New",
    )
    state_open = fields.Boolean(
        string="Open",
    )
    state_confirm = fields.Boolean(
        string="Closed",
    )
    output_format = fields.Selection(
        string="Output Format",
        required=True,
        selection=[("xls", "XLS"), ("ods", "ODS")],
        default="ods",
    )

    @api.constrains("date_start", "date_end")
    def _check_date(self):
        strWarning = _("Date start must be greater than date end")
        if self.date_start and self.date_end:
            if self.date_start > self.date_end:
                raise UserError(strWarning)

    @api.multi
    def action_print(self):
        self.ensure_one()

        datas = {}
        output_format = ""

        datas["form"] = self.read()[0]

        if self.output_format == "xls":
            output_format = "bank_statement_mutation_xls"
        elif self.output_format == "ods":
            output_format = "bank_statement_mutation_ods"

        return {
            "type": "ir.actions.report.xml",
            "report_name": output_format,
            "datas": datas,
        }
