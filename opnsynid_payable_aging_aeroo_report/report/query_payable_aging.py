# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime

from openerp import api, fields, models
from openerp.tools import drop_view_if_exists


class QueryPayableAging(models.Model):

    _name = "account.query_payable_aging"
    _description = "Query Payable Aging"
    _auto = False

    @api.multi
    def function_aging(self):
        for record in self:
            res = {}
            residual = 0.0
            obj_move_line = reconcile_lines = self.env["account.move.line"]
            period_length = self._context.get("period_length", False)
            date_as_of = self._context.get("date_as_of", False)

            if date_as_of:
                ord_date_as_of = datetime.strptime(date_as_of, "%Y-%m-%d").toordinal()

            res = {
                "aging1": 0.0,
                "aging2": 0.0,
                "aging3": 0.0,
                "aging4": 0.0,
                "aging5": 0.0,
                "amount_residual": 0.0,
                "amount_residual_currency": 0.0,
            }

            if record.date_due:
                ord_date_due = datetime.strptime(record.date_due, "%Y-%m-%d").toordinal()

                direction = ord_date_due - ord_date_as_of
                move_line = obj_move_line.browse(record.id)

                if move_line.reconcile_id:
                    reconcile_lines = move_line.reconcile_id.line_id
                elif move_line.reconcile_partial_id:
                    reconcile_lines = move_line.reconcile_partial_id.line_partial_ids
                else:
                    reconcile_lines += move_line

                for reconcile_line in reconcile_lines:
                    if reconcile_line.date <= date_as_of:
                        residual += reconcile_line.credit - reconcile_line.debit

                res["amount_residual"] = residual

                for interval in range(1, 6):
                    st_if_1 = period_length * (interval - 1)
                    st_if_2 = period_length * (interval)
                    if (st_if_1) <= abs(direction) < (st_if_2):
                        res["aging%s" % (interval)] = residual

                    if interval == 5:
                        if abs(direction) >= (period_length * 4):
                            res["aging5"] = residual

                if move_line.amount_residual_currency:
                    residual_currency = move_line.amount_residual_currency
                    record.amount_residual_currency = residual_currency

            record.aging1 = res["aging1"]
            record.aging2 = res["aging2"]
            record.aging3 = res["aging3"]
            record.aging4 = res["aging4"]
            record.aging5 = res["aging5"]

            if direction < 0:
                record.direction = "past"
            else:
                record.direction = "future"

    name = fields.Char(string="Description", size=64)

    move_id = fields.Many2one(string="# Move", comodel_name="account.move")

    account_id = fields.Many2one(string="Account", comodel_name="account.account")

    company_id = fields.Many2one(string="Company", comodel_name="res.company")

    date = fields.Date(string="Date")
    date_due = fields.Date(string="Date Due")

    journal_id = fields.Many2one(string="Journal", comodel_name="account.journal")

    partner_id = fields.Many2one(string="Partner", comodel_name="res.partner")

    period_id = fields.Many2one(string="Period", comodel_name="account.period")

    respective_currency_id = fields.Many2one(
        string="Respective Currency", comodel_name="res.currency"
    )

    base_currency_id = fields.Many2one(
        string="Base Currency", comodel_name="res.currency"
    )

    reconcile_id = fields.Many2one(
        string="Reconcile", comodel_name="account.move.reconcile"
    )

    reconcile_partial_id = fields.Many2one(
        string="Partial Reconcile", comodel_name="account.move.reconcile"
    )

    debit = fields.Float(string="Debit")
    credit = fields.Float(string="Credit")
    amount_currency = fields.Float(string="Amount Currency")

    amount_residual = fields.Float(string="Amount Residual", compute=function_aging)

    amount_residual_currency = fields.Float(
        string="Amount Residual Currency", compute=function_aging
    )

    aging1 = fields.Float(string="Aging1", compute=function_aging)

    aging2 = fields.Float(string="Aging2", compute=function_aging)

    aging3 = fields.Float(string="Aging3", compute=function_aging)

    aging4 = fields.Float(string="Aging4", compute=function_aging)

    aging5 = fields.Float(string="Aging5", compute=function_aging)

    direction = fields.Selection(
        string="Direction",
        selection=[("past", "Past"), ("future", "Future")],
        compute=function_aging,
    )

    state = fields.Selection(
        string="State", selection=[("draft", "Unposted"), ("posted", "Posted")]
    )

    def init(self, cr):
        drop_view_if_exists(cr, "account_query_payable_aging")
        strSQL = """
                    CREATE OR REPLACE VIEW account_query_payable_aging AS (
                        SELECT
                                a.id AS id,
                                a.name AS name,
                                a.move_id AS move_id,
                                a.account_id AS account_id,
                                b.company_id AS company_id,
                                b.date as date,
                                a.date_maturity as date_due,
                                b.journal_id AS journal_id,
                                a.partner_id AS partner_id,
                                b.period_id AS period_id,
                                CASE
                                    WHEN a.currency_id IS NULL
                                    THEN e.currency_id
                                    ELSE a.currency_id
                                END AS respective_currency_id,
                                e.currency_id AS base_currency_id,
                                a.reconcile_id AS reconcile_id,
                                a.reconcile_partial_id AS reconcile_partial_id,
                                a.debit AS debit,
                                a.credit AS credit,
                                a.amount_currency AS amount_currency,
                                b.state AS state
                        FROM account_move_line AS a
                        JOIN account_move AS b ON a.move_id = b.id
                        JOIN account_journal AS c ON b.journal_id = c.id
                        JOIN account_account AS d ON a.account_id = d.id
                        JOIN res_company AS e ON b.company_id = e.id
                        WHERE   (d.type = 'payable') AND
                                (b.state = 'posted') AND
                                (a.credit > 0)
                    )
                    """
        cr.execute(strSQL)
