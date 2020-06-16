# -*- coding: utf-8 -*-
# Copyright 2015 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp.osv import osv, fields
from openerp.tools.translate import _


class WizardReportTrialBalance(osv.osv_memory):
    _name = "account.wizard_report_trial_balance"
    _description = "Wizard Report Trial Balance"

    def default_company_id(self, cr, uid, context=None):
        obj_user = self.pool.get("res.users")

        user = obj_user.browse(cr, uid, [uid])[0]

        return user.company_id and user.company_id.id or False

    def default_fiscalyear_id(self, cr, uid, context=None):
        obj_fiscalyear = self.pool.get("account.fiscalyear")

        fiscalyear_id = obj_fiscalyear.find(cr, uid)

        return fiscalyear_id or False

    def default_period_id(self, cr, uid, context=None):
        obj_period = self.pool.get("account.period")

        period_ids = obj_period.find(cr, uid)

        return period_ids and period_ids[0] or False

    def default_state(self, cr, uid, context=None):
        return "posted"

    def default_output(self, cr, uid, context=None):
        return "ods"

    _columns = {
        "company_id": fields.many2one(
            string="Company",
            obj="res.company",
            required=True),
        "fiscalyear_id": fields.many2one(
            string="Fiscal Year",
            obj="account.fiscalyear",
            required=True),
        "period_id": fields.many2one(
            string="Period",
            obj="account.period",
            required=True),
        "output_format": fields.selection(
            string="Output Format",
            required=True,
            selection=[
                ("pdf", "PDF"),
                ("xls", "XLS"),
                ("ods", "ODS")
            ]),
        "state": fields.selection(
            string="State",
            selection=[
                ("all", "All"),
                ("draft", "Draft"),
                ("posted", "Posted")
            ],
            required=True),
    }

    _defaults = {
        "company_id": default_company_id,
        "fiscalyear_id": default_fiscalyear_id,
        "period_id": default_period_id,
        "output_format": default_output,
        "state": default_state
    }

    def button_print_report(self, cr, uid, ids, data, context=None):
        datas = {}
        output_format = ""

        if context is None:
            context = {}

        datas["form"] = self.read(cr, uid, ids)[0]

        if datas["form"]["output_format"] == "xls":
            output_format = "report_trial_balance_xls"
        elif datas["form"]["output_format"] == "ods":
            output_format = "report_trial_balance_ods"
        elif datas["form"]["output_format"] == "pdf":
            output_format = "report_trial_balance_pdf"
        else:
            err = "Output Format cannot be empty"
            raise osv.except_osv(_("Warning"), _(err))

        return {
            "type": "ir.actions.report.xml",
            "report_name": output_format,
            "datas": datas,
        }
