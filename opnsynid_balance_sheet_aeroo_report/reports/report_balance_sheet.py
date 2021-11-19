# -*- coding: utf-8 -*-
# © 2015 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import time
from decimal import Decimal

from openerp.report import report_sxw


class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):  # pylint: disable=R8110
        super(Parser, self).__init__(cr, uid, name, context)
        self.lines = []
        self.sub_total_account_current = Decimal(0.0)
        self.sub_total_second_current = Decimal(0.0)
        self.total_account_current = Decimal(0.0)
        self.sub_total_account_previous = Decimal(0.0)
        self.sub_total_second_previous = Decimal(0.0)
        self.total_account_previous = Decimal(0.0)
        self.localcontext.update(
            {
                "time": time,
                "get_asset": self.get_asset,
                "get_liability": self.get_liability,
                "get_period": self.get_period,
                "get_company": self.get_company,
                "line": self.get_balance_sheet_line,
                "total_previous": self.get_total_previous,
                "total_second_previous": self.get_total_second_previous,
                "total_current": self.get_total_current,
                "total_second_current": self.get_total_second_current,
                "sub_total_account_current": self.get_sub_total_account_current,
                "sub_total_second_current": self.get_sub_total_second_current,
                "total_account_current": self.get_total_account_current,
                "total_acc_second_current": self.get_total_acc_second_current,
                "sub_total_account_previous": self.get_sub_total_account_previous,
                "sub_total_second_previous": self.get_sub_total_second_previous,
                "total_account_previous": self.get_total_account_previous,
                "total_acc_second_previous": self.get_total_acc_second_previous,
            }
        )

    def get_asset(self):
        obj_user = self.pool.get("res.users")
        user = obj_user.browse(self.cr, self.uid, [self.uid])[0]

        return user.company_id.asset_ids

    def get_liability(self):
        obj_user = self.pool.get("res.users")
        user = obj_user.browse(self.cr, self.uid, [self.uid])[0]

        return user.company_id.liability_ids

    def get_period(self):
        period_name = (
            self.localcontext["data"]["form"]["period_id"]
            and self.localcontext["data"]["form"]["period_id"][1]
            or False
        )

        return period_name

    def get_company(self):
        company_name = (
            self.localcontext["data"]["form"]["company_id"]
            and self.localcontext["data"]["form"]["company_id"][1]
            or False
        )

        return company_name

    def get_previous_period(self, account_id, currency_id, user_type):
        previous_period = 0.0
        second_previous_period = 0.0

        obj_account_account = self.pool.get("account.account")
        obj_account_period = self.pool.get("account.period")
        obj_account_type = self.pool.get("account.account.type")

        criteria_type = [("id", "=", user_type[0])]

        account_type_ids = obj_account_type.search(self.cr, self.uid, criteria_type)
        account_type = obj_account_type.browse(self.cr, self.uid, account_type_ids)

        report_type = account_type.report_type
        if report_type in ["income", "liability"]:
            factor = -1
        else:
            factor = 1

        current_period_id = self.localcontext["data"]["form"]["period_id"][0]
        fiscalyear_id = self.localcontext["data"]["form"]["fiscalyear_id"][0]
        state = self.localcontext["data"]["form"]["state"]

        criteria = [
            ("fiscalyear_id", "=", fiscalyear_id),
        ]

        period_ids = obj_account_period.search(self.cr, self.uid, criteria)

        for list_index, period_id in enumerate(period_ids):
            if period_id == current_period_id:
                previous_period_id = period_ids[list_index - 1]

        criteria = [("fiscalyear_id", "=", fiscalyear_id), ("special", "=", True)]

        first_period_ids = obj_account_period.search(
            self.cr,
            self.uid,
            criteria,
        )
        first_period_id = first_period_ids[0]

        ctx = {}
        ctx["period_to"] = previous_period_id
        ctx["period_from"] = first_period_id
        if state != "all":
            ctx["state"] = state

        account = obj_account_account.browse(self.cr, self.uid, account_id, ctx)

        if account:
            previous_period = account.balance * factor
            if currency_id:
                second_previous_period = account.foreign_balance * factor
            else:
                second_previous_period = False

        return previous_period, second_previous_period

    def get_current_period(self, account_id, currency_id, user_type):
        current_period = 0.0
        second_current_period = 0.0
        obj_account_account = self.pool.get("account.account")
        obj_account_period = self.pool.get("account.period")
        obj_account_type = self.pool.get("account.account.type")

        criteria_type = [("id", "=", user_type[0])]

        account_type_ids = obj_account_type.search(self.cr, self.uid, criteria_type)
        account_type = obj_account_type.browse(self.cr, self.uid, account_type_ids)

        report_type = account_type.report_type
        if report_type in ["income", "liability"]:
            factor = -1
        else:
            factor = 1

        period_id = self.localcontext["data"]["form"]["period_id"][0]
        fiscalyear_id = self.localcontext["data"]["form"]["fiscalyear_id"][0]
        state = self.localcontext["data"]["form"]["state"]

        criteria = [
            ("fiscalyear_id", "=", fiscalyear_id),
            ("special", "=", True),
        ]

        period_ids = obj_account_period.search(
            self.cr,
            self.uid,
            criteria,
        )

        first_period_id = period_ids[0]

        ctx = {}
        ctx["period_to"] = period_id
        ctx["period_from"] = first_period_id
        if state != "all":
            ctx["state"] = state

        account = obj_account_account.browse(self.cr, self.uid, account_id, ctx)

        if account:
            current_period = account.balance * factor
            if currency_id:
                second_current_period = account.foreign_balance * factor
            else:
                second_current_period = False

        return current_period, second_current_period

    def get_balance_sheet_line(self, account_id):
        def _process_child(accounts, parent, level):
            account_rec = [acct for acct in accounts if acct["id"] == parent][0]

            if account_rec["id"] != account_id:

                if account_rec["type"] == "view":
                    res = {
                        "name": ("  " * level) + account_rec["name"],
                        "code": account_rec["code"],
                        "previous_period": False,
                        "second_previous_period": False,
                        "current_period": False,
                        "second_current_period": False,
                        "second_curr": False,
                    }

                    self.lines.append(res)

                else:

                    currency_id = account_rec["currency_id"]
                    currency = currency_id and currency_id[1] or False
                    previous_period, second_previous_period = self.get_previous_period(
                        account_rec["id"],
                        currency_id,
                        account_rec["user_type"],
                    )
                    current_period, second_current_period = self.get_current_period(
                        account_rec["id"],
                        currency_id,
                        account_rec["user_type"],
                    )

                    self.total_previous += Decimal(previous_period)
                    self.total_second_previous_period += Decimal(second_previous_period)
                    self.total_current += Decimal(current_period)
                    self.total_second_current_period += Decimal(second_current_period)

                    show_zero = self.localcontext["data"]["form"]["show_zero"]

                    if show_zero:
                        res = {
                            "name": ("  " * level) + account_rec["name"],
                            "code": account_rec["code"],
                            "previous_period": Decimal(previous_period),
                            "second_previous_period": Decimal(second_previous_period),
                            "current_period": Decimal(current_period),
                            "second_current_period": Decimal(second_current_period),
                            "second_curr": currency,
                        }
                        self.lines.append(res)
                    else:
                        if previous_period != 0.0 and current_period != 0.0:
                            res = {
                                "name": ("  " * level) + account_rec["name"],
                                "code": account_rec["code"],
                                "previous_period": Decimal(previous_period),
                                "second_previous_period": Decimal(
                                    second_previous_period
                                ),
                                "current_period": Decimal(current_period),
                                "second_current_period": Decimal(second_current_period),
                                "second_curr": currency,
                            }
                            self.lines.append(res)

            if account_rec["child_id"] and account_rec["type"] != "consolidation":

                level += 1
                for child in account_rec["child_id"]:
                    _process_child(accounts, child, level)

        self.total_previous = Decimal(0.0)
        self.total_second_previous_period = Decimal(0.0)
        self.total_current = Decimal(0.0)
        self.total_second_current_period = Decimal(0.0)

        obj_account_account = self.pool.get("account.account")

        self.lines = []
        ids = {}
        level = 1

        ctx = {}

        ids = [account_id]

        parents = ids

        child_ids = obj_account_account._get_children_and_consol(
            self.cr, self.uid, ids, ctx
        )

        if child_ids:
            ids = child_ids

        account_fields = [
            "type",
            "user_type",
            "code",
            "name",
            "debit",
            "currency_id",
            "credit",
            "balance",
            "parent_id",
            "child_id",
        ]

        accounts = obj_account_account.read(self.cr, self.uid, ids, account_fields, ctx)

        for parent in parents:
            level = 1
            _process_child(accounts, parent, level)

        return self.lines

    def get_total_previous(self):
        return self.total_previous

    def get_total_second_previous(self):
        return self.total_second_previous_period

    def get_total_current(self):
        return self.total_current

    def get_total_second_current(self):
        return self.total_second_current_period

    def get_sub_total_account_current(self, amount):
        self.sub_total_account_current += amount
        return True

    def get_sub_total_second_current(self, amount):
        self.sub_total_second_current += amount
        return True

    def get_total_account_current(self):

        self.total_account_current = Decimal(self.sub_total_account_current)
        self.sub_total_account_current = Decimal(0.0)

        return self.total_account_current

    def get_total_acc_second_current(self):

        self.total_acc_second_current = Decimal(self.sub_total_second_current)
        self.sub_total_second_current = Decimal(0.0)

        return self.total_acc_second_current

    def get_sub_total_account_previous(self, amount):
        self.sub_total_account_previous += amount
        return True

    def get_sub_total_second_previous(self, amount):
        self.sub_total_second_previous += amount
        return True

    def get_total_account_previous(self):

        self.total_account_previous = Decimal(self.sub_total_account_previous)
        self.sub_total_account_previous = Decimal(0.0)

        return self.total_account_previous

    def get_total_acc_second_previous(self):

        self.total_acc_second_previous = Decimal(self.sub_total_second_previous)
        self.sub_total_second_previous = Decimal(0.0)

        return self.total_acc_second_previous
