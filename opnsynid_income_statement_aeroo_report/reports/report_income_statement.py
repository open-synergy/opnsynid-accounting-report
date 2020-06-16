# -*- coding: utf-8 -*-
# Copyright 2015 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import time
from openerp.report import report_sxw


class Parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.lines = []
        self.sub_total_account_current = 0.0
        self.total_account_current = 0.0
        self.sub_total_account_previous = 0.0
        self.total_account_previous = 0.0
        self.sub_total_account_ytd = 0.0
        self.total_account_ytd = 0.0
        self.localcontext.update({
            "time": time,
            "get_period": self.get_period,
            "get_company": self.get_company,
            "get_income_statement": self.get_income_statement,
            "line": self.get_income_statement_line,
            "total_previous": self.get_total_previous,
            "total_current": self.get_total_current,
            "total_ytd": self.get_total_ytd,
            "sub_total_account_current": self.get_sub_total_account_current,
            "total_account_current": self.get_total_account_current,
            "sub_total_account_previous": self.get_sub_total_account_previous,
            "total_account_previous": self.get_total_account_previous,
            "sub_total_account_ytd": self.get_sub_total_account_ytd,
            "total_account_ytd": self.get_total_account_ytd,
        })

    def get_company(self):
        company_name = self.localcontext["data"]["form"]["company_id"] \
            and self.localcontext["data"]["form"]["company_id"][1] or False

        return company_name

    def get_period(self):
        period_name = self.localcontext["data"]["form"]["period_id"] \
            and self.localcontext["data"]["form"]["period_id"][1] or False

        return period_name

    def get_income_statement(self):
        obj_user = self.pool.get("res.users")
        user = obj_user.browse(self.cr, self.uid, [self.uid])[0]

        return user.company_id.income_statement_ids

    def get_previous_period(self, account_id):
        previous_period = 0.0
        obj_account_account = self.pool.get("account.account")
        obj_account_period = self.pool.get("account.period")
        form = self.localcontext["data"]["form"]

        current_period_id = form["period_id"][0]
        fiscalyear_id = form["fiscalyear_id"][0]
        state = form["state"]

        criteria = [
            ("fiscalyear_id", "=", fiscalyear_id)
        ]

        period_ids = obj_account_period.search(
            self.cr, self.uid, criteria, order="date_start")

        for list_index, period_id in enumerate(period_ids):
            if period_id == current_period_id:
                previous_period_id = period_ids[list_index - 1]

        ctx = {}
        ctx["period_to"] = previous_period_id
        ctx["period_from"] = previous_period_id
        if state != "all":
            ctx["state"] = state

        account = obj_account_account.browse(
            self.cr, self.uid, account_id, ctx)

        report_type = account.user_type.report_type
        if report_type in ["income"]:
            factor = -1
        else:
            factor = 1

        if account:
            previous_period = (account.balance * factor)

        return previous_period

    def get_current_period(self, account_id):
        current_period = 0.0
        obj_account_account = self.pool.get("account.account")

        form = self.localcontext["data"]["form"]

        period_id = form["period_id"][0]
        state = form["state"]

        ctx = {}
        ctx["period_to"] = period_id
        ctx["period_from"] = period_id
        if state != "all":
            ctx["state"] = state

        account = obj_account_account.browse(
            self.cr, self.uid, account_id, ctx)

        report_type = account.user_type.report_type
        if report_type in ["income"]:
            factor = -1
        else:
            factor = 1

        if account:
            current_period = (account.balance * factor)

        return current_period

    def get_ytd(self, account_id):
        year_to_date = 0.0
        obj_account_account = self.pool.get("account.account")
        obj_account_period = self.pool.get("account.period")

        form = self.localcontext["data"]["form"]
        fiscalyear_id = form["fiscalyear_id"][0]
        state = form["state"]

        criteria = [
            ("fiscalyear_id", "=", fiscalyear_id)
        ]

        period_ids = obj_account_period.search(
            self.cr, self.uid, criteria, order="date_start")

        period_id = form["period_id"][0]
        first_period_id = period_ids[0]

        ctx = {}
        ctx["period_to"] = period_id
        ctx["period_from"] = first_period_id
        if state != "all":
            ctx["state"] = state

        account = obj_account_account.browse(
            self.cr, self.uid, account_id, ctx)

        report_type = account.user_type.report_type
        if report_type in ["income"]:
            factor = -1
        else:
            factor = 1

        if account:
            year_to_date = (account.balance * factor)

        return year_to_date

    def get_income_statement_line(self, account_id):
        def _process_child(accounts, parent, level):
            account_rec = \
                [acct for acct in accounts if acct["id"] == parent][0]

            previous_period = self.get_previous_period(account_rec["id"])
            current_period = self.get_current_period(account_rec["id"])
            ytd_period = self.get_ytd(account_rec["id"])

            if account_rec["id"] != account_id:
                if account_rec["type"] == "view":
                    res = {
                        "name": ("  " * level) + account_rec["name"],
                        "previous_period": False,
                        "current_period": False,
                        "ytd_period": False,
                    }

                    self.lines.append(res)

                else:
                    self.total_previous += previous_period
                    self.total_current += current_period
                    self.total_ytd += ytd_period
                    res = {
                        "name": ("  " * level) + account_rec["name"],
                        "previous_period": previous_period,
                        "current_period": current_period,
                        "ytd_period": ytd_period,
                    }

                    self.lines.append(res)

            if account_rec["child_id"] \
                    and account_rec["type"] != "consolidation":
                level += 1
                for child in account_rec["child_id"]:
                    _process_child(accounts, child, level)

        self.total_previous = 0.0
        self.total_current = 0.0
        self.total_ytd = 0.0

        obj_account_account = self.pool.get("account.account")

        self.lines = []
        ids = {}
        level = 1

        ctx = {}

        ids = [account_id]

        parents = ids

        child_ids = obj_account_account._get_children_and_consol(
            self.cr, self.uid, ids, ctx)

        if child_ids:
            ids = child_ids

        account_fields = [
            "type", "code", "name", "debit", "credit",
            "balance", "parent_id", "child_id", "user_type",
        ]
        accounts = obj_account_account.read(
            self.cr, self.uid, ids, account_fields, ctx)

        for parent in parents:
            level = 1
            _process_child(accounts, parent, level)

        return self.lines

    def get_total_previous(self):
        return self.total_previous

    def get_total_current(self):
        return self.total_current

    def get_total_ytd(self):
        return self.total_ytd

    def get_sub_total_account_current(self, amount):
        self.sub_total_account_current += amount
        return True

    def get_total_account_current(self):

        self.total_account_current = self.sub_total_account_current
        self.sub_total_account_current = 0.0

        return self.total_account_current

    def get_sub_total_account_previous(self, amount):
        self.sub_total_account_previous += amount
        return True

    def get_total_account_previous(self):
        self.total_account_previous = self.sub_total_account_previous
        self.sub_total_account_previous = 0.0

        return self.total_account_previous

    def get_sub_total_account_ytd(self, amount):
        self.sub_total_account_ytd += amount
        return True

    def get_total_account_ytd(self):
        self.total_account_ytd = self.sub_total_account_ytd
        self.sub_total_account_ytd = 0.0

        return self.total_account_ytd
