# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import time
from openerp.report import report_sxw


class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.lines = []
        self.sub_total_account_current = 0.0
        self.total_account_current = 0.0
        self.localcontext.update({
            'time': time,
            'get_company': self.get_company,
            'get_income_statement': self.get_income_statement,
            'line': self.get_income_statement_line,
            'total_current': self.get_total_current,
            'sub_total_account_current': self.get_sub_total_account_current,
            'total_account_current': self.get_total_account_current,
            })

    def get_company(self):
        company_name = self.localcontext['data']['form']['company_id'] \
            and self.localcontext['data']['form']['company_id'][1] or False

        return company_name

    def get_income_statement(self):
        obj_user = self.pool.get('res.users')
        user = obj_user.browse(self.cr, self.uid, [self.uid])[0]

        return user.company_id.income_statement_ids


    def get_current_period(self, account_id):
        current_period = 0.0
        obj_account_account = self.pool.get('account.account')

        form = self.localcontext['data']['form']

        state = form['state']
        date_start = form['date_start']
        date_end = form['date_end']

        ctx = {}
        ctx['date_from'] = date_start
        ctx['date_to'] = date_end
        ctx['state'] = state

        account = obj_account_account.browse(
            self.cr, self.uid, account_id, ctx)

        if account:
            current_period = account.balance

        return current_period


    def get_income_statement_line(self, account_id):
        def _process_child(accounts, parent, level):
            account_rec = \
                [acct for acct in accounts if acct['id'] == parent][0]

            current_period = self.get_current_period(account_rec['id'])

            if account_rec['id'] != account_id:
                if account_rec['type'] == 'view':
                    res = {
                        'name': ('  '*level) + account_rec['name'],
                        'current_period': False,
                        }

                    self.lines.append(res)

                else:
                    self.total_current += current_period
                    res = {
                        'name': ('  '*level) + account_rec['name'],
                        'current_period': current_period,
                        }

                    self.lines.append(res)

            if account_rec['child_id'] \
                    and account_rec['type'] != 'consolidation':
                level += 1
                for child in account_rec['child_id']:
                    _process_child(accounts, child, level)

        self.total_previous = 0.0
        self.total_current = 0.0
        self.total_ytd = 0.0

        obj_account_account = self.pool.get('account.account')

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
            'type', 'code', 'name', 'debit', 'credit',
            'balance', 'parent_id', 'child_id',
            ]
        accounts = obj_account_account.read(
            self.cr, self.uid, ids, account_fields, ctx)

        for parent in parents:
            level = 1
            _process_child(accounts, parent, level)

        return self.lines

    def get_total_current(self):
        return self.total_current

    def get_sub_total_account_current(self, amount):
        self.sub_total_account_current += amount
        return True

    def get_total_account_current(self):

        self.total_account_current = self.sub_total_account_current
        self.sub_total_account_current = 0.0

        return self.total_account_current
