# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from report import report_sxw
from decimal import Decimal


class Parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.lines = []
        self.total_debit = 0.0
        self.total_credit = 0.0
        self.total_beginning_debit = 0.0
        self.total_beginning_credit = 0.0
        self.total_ending_debit = 0.0
        self.total_ending_credit = 0.0
        self.localcontext.update({
            'time': time,
            'get_period': self.get_period,
            'get_company': self.get_company,
            'total_debit': self.get_total_debit,
            'total_credit': self.get_total_credit,
            'total_beginning_debit': self.get_total_beginning_debit,
            'total_beginning_credit': self.get_total_beginning_credit,
            'total_ending_debit': self.get_total_ending_debit,
            'total_ending_credit': self.get_total_ending_credit,
            'lines': self.get_trial_balance_line,
        })

    def get_company(self):
        data = self.localcontext['data']['form']
        company_name = data['company_id'] and data['company_id'][1] or False

        return company_name

    def get_period(self):
        data = self.localcontext['data']['form']
        period_name = data['period_id'] and data['period_id'][1] or False

        return period_name

    def get_balance(self, type_balance, account_id):
        res = {}
        obj_period = self.pool.get('account.period')
        obj_account = self.pool.get('account.account')

        data = self.localcontext['data']['form']
        data_period = data['period_id']
        data_fiscalyear = data['fiscalyear_id']

        period_id = data_period and data_period[0] or False
        fiscalyear_id = data_fiscalyear and data_fiscalyear[0] or False
        state = data['state']

        period_from = False
        period_to = False

        if period_id:
            kriteria_opening_balance = [('fiscalyear_id', '=', fiscalyear_id)]
            period_ids = obj_period.search(
                self.cr, self.uid, kriteria_opening_balance)

            for list_index, opening_period_id in enumerate(period_ids):
                if opening_period_id == period_id:
                    previous_period_id = period_ids[list_index-1]

            first_period_id = period_ids[0]

            beginning_period_from = first_period_id
            beginning_period_to = previous_period_id

            period_from = period_id
            period_to = period_id

            ending_period_from = first_period_id
            ending_period_to = period_id

        res = {
            'beginning_debit': 0.0,
            'beginning_credit': 0.0,
            'debit': 0.0,
            'credit': 0.0,
            'ending_debit': 0.0,
            'ending_credit': 0.0,
        }

        if period_id:
            context_beginning = {
                'period_from': beginning_period_from,
                'period_to': beginning_period_to,
            }

            context_ending = {
                'period_from': ending_period_from,
                'period_to': ending_period_to,
            }

            context_now = {
                'period_from': period_from,
                'period_to': period_to,
            }

            if state != 'all':
                context_beginning.update({'state': state})
                context_ending.update({'state': state})
                context_now.update({'state': state})

            account_beginning = obj_account.browse(
                self.cr, self.uid, [account_id], context=context_beginning)[0]
            account_ending = obj_account.browse(
                self.cr, self.uid, [account_id], context=context_ending)[0]
            account_now = obj_account.browse(
                self.cr, self.uid, [account_id], context=context_now)[0]

            if type_balance == 'beginning':
                res = {
                    'beginning_debit': account_beginning.debit,
                    'beginning_credit': account_beginning.credit
                }
            if type_balance == 'now':
                res = {
                    'debit': account_now.debit,
                    'credit': account_now.credit
                }
            if type_balance == 'ending':
                res = {
                    'ending_debit': account_ending.debit,
                    'ending_credit': account_ending.credit
                }

        return res

    def get_total_debit(self):
        return self.total_debit

    def get_total_credit(self):
        return self.total_credit

    def get_total_beginning_debit(self):
        return self.total_beginning_debit

    def get_total_beginning_credit(self):
        return self.total_beginning_credit

    def get_total_ending_debit(self):
        return self.total_ending_debit

    def get_total_ending_credit(self):
        return self.total_ending_credit

    def get_trial_balance_line(self):
        def _process_child(accounts, parent, level):
            account_rec = [
                acct for acct in accounts if acct['id'] == parent
            ][0]

            if account_rec['type'] != 'view':

                beginning = self.get_balance('beginning', account_rec['id'])
                now = self.get_balance('now', account_rec['id'])
                ending_debit = self.get_balance('ending', account_rec['id'])

                self.total_beginning_debit += beginning['beginning_debit']
                self.total_beginning_credit += \
                    abs(beginning['beginning_credit'])

                self.total_debit += now['debit']
                self.total_credit += abs(now['credit'])

                self.total_ending_debit += ending_debit['ending_debit']
                self.total_ending_credit += abs(ending_debit['ending_credit'])

                res = {
                    'id': account_rec['id'],
                    'code': account_rec['code'],
                    'name': account_rec['name'],
                    'beginning_debit': Decimal(
                        abs(beginning['beginning_debit'])
                    ),
                    'beginning_credit': Decimal(
                        abs(beginning['beginning_credit'])
                    ),
                    'debit': Decimal(abs(now['debit'])),
                    'credit': Decimal(abs(now['credit'])),
                    'ending_debit': Decimal(
                        abs(ending_debit['ending_debit'])
                    ),
                    'ending_credit': Decimal(
                        abs(ending_debit['ending_credit'])
                    ),
                    'balance': Decimal(abs(account_rec['balance'])),
                    'parent_id': account_rec['parent_id'],
                }

                self.lines.append(res)

            if account_rec['child_id']:
                level += 1
                for child in account_rec['child_id']:
                    _process_child(accounts, child, level)

        obj_account_account = self.pool.get('account.account')

        kriteria = [('type', '<>', 'view')]

        account_ids = obj_account_account.search(self.cr, self.uid, kriteria)

        self.lines = []
        ids = {}
        level = 1

        ctx = {}

        ids = account_ids

        parents = ids

        child_ids = obj_account_account._get_children_and_consol(
            self.cr, self.uid, ids, ctx)

        if child_ids:
            ids = child_ids

        account_fields = [
            'type',
            'code',
            'name',
            'debit',
            'credit',
            'balance',
            'parent_id',
            'child_id'
        ]
        accounts = obj_account_account.read(
            self.cr, self.uid, ids, account_fields, ctx)

        for parent in parents:
            level = 1
            _process_child(accounts, parent, level)

        return self.lines
