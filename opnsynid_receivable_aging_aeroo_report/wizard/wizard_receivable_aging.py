# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from openerp import api, models, fields, _
from openerp.exceptions import except_orm
from datetime import datetime


class WizardReportReceivableAging(models.TransientModel):
    _name = "account.wizard_report_receivable_aging"
    _description = "Wizard Report Receivable Aging"

    @api.model
    def _default_fiscalyear_id(self):
        obj_fiscalyear = self.env["account.fiscalyear"]

        fiscalyear_id = obj_fiscalyear.find()

        return fiscalyear_id or False

    @api.model
    def _default_date_as_of(self):
        return datetime.now()

    @api.model
    def _default_journal(self):
        company_id = self._context.get(
            "company_id", self.env.user.company_id.id)
        domain = [
            ("type", "=", "sale"),
            ("company_id", "=", company_id),
        ]
        return self.env["account.journal"].search(domain, limit=1)

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.user.company_id.id,
    )

    fiscalyear_id = fields.Many2one(
        string="Fiscal Year",
        comodel_name="account.fiscalyear",
        required=True,
        default=_default_fiscalyear_id,
    )

    journal_ids = fields.Many2many(
        string="Journals",
        comodel_name="account.journal",
        relation="wizard_receivable_aging_rel",
        column1="wizard_id",
        column2="journal_id",
        default=_default_journal,
    )

    date_from = fields.Date(
        string="Date From",
        required=False,
    )

    date_to = fields.Date(
        string="Date To",
        required=False,
    )

    date_as_of = fields.Date(
        string="Date As Of",
        required=True,
        default=datetime.now(),
    )

    period_length = fields.Integer(
        string="Period Legth(days)",
        required=True,
        default=30,
    )

    output_format = fields.Selection(
        string="Output Format",
        required=True,
        selection=[
            ("xls", "XLS"),
            ("ods", "ODS")
        ],
        default="ods",
    )

    @api.multi
    def button_print_report(self):
        self.ensure_one()
        context = self._context

        if context is None:
            context = {}

        datas = {}
        output_format = ""

        datas["form"] = self.read()[0]

        date_from = datas["form"]["date_from"]
        date_to = datas["form"]["date_to"]

        if date_from and date_to:
            if date_from > date_to:
                err = "Date From cannot be greater than Date To"
                raise except_orm(_("Warning"), _(err))

        if datas["form"]["output_format"] == "xls":
            output_format = "report_receivable_aging_xls"
        elif datas["form"]["output_format"] == "ods":
            output_format = "report_receivable_aging_ods"

        return {
            "type": "ir.actions.report.xml",
            "report_name": output_format,
            "datas": datas,
        }
