# -*- coding: utf-8 -*-
# © 2015 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.addons.opnsynid_general_ledger_aeroo_report.report \
    import report_general_ledger


class Parser(report_general_ledger.Parser):

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)

    def _prepare_opening_balance(
        self,
        account_id,
        state,
        date_start_period
    ):
        _super = super(Parser, self)
        res = _super._prepare_opening_balance(
            account_id, state, date_start_period)

        data = self.localcontext["data"]["form"]
        operating_unit_ids = data["operating_unit_ids"]

        if operating_unit_ids:
            res.append(("operating_unit_id", "in", operating_unit_ids))

        return res

    def _prepare_beginning_balance(
        self,
        account_id,
        state,
        period,
        date_start_period,
    ):
        _super = super(Parser, self)
        res = _super._prepare_beginning_balance(
            account_id, state, period, date_start_period)

        data = self.localcontext["data"]["form"]
        operating_unit_ids = data["operating_unit_ids"]

        if operating_unit_ids:
            res.append(("operating_unit_id", "in", operating_unit_ids))

        return res

    def _prepare_line(
        self,
        account_id,
    ):
        _super = super(Parser, self)
        res = _super._prepare_line(account_id)

        data = self.localcontext["data"]["form"]
        operating_unit_ids = data["operating_unit_ids"]

        if operating_unit_ids:
            res.append(("operating_unit_id", "in", operating_unit_ids))

        return res
