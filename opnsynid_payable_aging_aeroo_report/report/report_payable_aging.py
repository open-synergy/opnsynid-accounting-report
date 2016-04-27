# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time
from datetime import datetime
from openerp.report import report_sxw


class Parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.journal_list = []
        self.total_amount = 0.0
        self.localcontext.update({
            'time': time,
            'get_company': self.get_company,
            'get_date': self.get_date,
            'get_date_as_of': self.get_date_as_of,
            'get_period_length': self.get_period_length,
            'get_journals': self.get_journals,
        })

    def get_company(self):
        data = self.localcontext['data']['form']
        company_name = data['company_id'] and data['company_id'][1] or False

        return company_name

    def get_date_from(self):
        data = self.localcontext['data']['form']
        date_from = data['date_from'] or False
        if date_from:
            conv_date_from = datetime.strptime(
                date_from, '%Y-%m-%d').strftime('%d/%m/%Y')
            return conv_date_from
        else:
            return False

    def get_date_to(self):
        data = self.localcontext['data']['form']
        date_to = data['date_to'] or False
        if date_to:
            conv_date_to = datetime.strptime(
                date_to, '%Y-%m-%d').strftime('%d/%m/%Y')
            return conv_date_to
        else:
            return False

    def get_date(self):
        date_from = self.get_date_from()
        date_to = self.get_date_to()

        if date_from and date_to:
            return date_from + ' to ' + date_to
        elif date_from and not date_to:
            return 'from ' + date_from
        elif not date_from and date_to:
            return 'to ' + date_to
        else:
            return False

    def get_date_as_of(self):
        data = self.localcontext['data']['form']
        date_as_of = data['date_as_of'] or False
        conv_date_as_of = datetime.strptime(
            date_as_of, '%Y-%m-%d').strftime('%d/%m/%Y')

        return conv_date_as_of

    def get_period_length(self):
        data = self.localcontext['data']['form']
        period_length = data['period_length'] or False

        return period_length

    def get_journals(self):
        obj_journal = self.pool.get('account.journal')
        data_form = self.localcontext['data']['form']
        journal_ids = data_form['journal_ids']
        period_length = data_form['period_length']

        if journal_ids:
            for journal in obj_journal.browse(self.cr, self.uid, journal_ids):
                data = self.get_data(journal.id)
                aging_label = {}

                for interval in range(1, 6):
                    label1 = str(period_length * (interval - 1))
                    label2 = str(period_length * (interval))
                    aging_label['aging%s' % interval] = '%s - %s' % (
                        label1, label2)

                    if interval == 5:
                        aging_label['aging5'] = '+%s' % (
                            str(period_length * (4)))

                result = {
                    'id': journal.id,
                    'name': journal.name,
                    'data': data['data'],
                    'aging1': data['aging1'],
                    'aging2': data['aging2'],
                    'aging3': data['aging3'],
                    'aging4': data['aging4'],
                    'aging5': data['aging5'],
                    'current': data['current'],
                    'aging_label1': aging_label['aging1'],
                    'aging_label2': aging_label['aging2'],
                    'aging_label3': aging_label['aging3'],
                    'aging_label4': aging_label['aging4'],
                    'aging_label5': aging_label['aging5'],
                }

                self.journal_list.append(result)

        return self.journal_list

    def get_data(self, journal_id):
        res = {}
        obj_line = self.pool.get('account.query_payable_aging')

        company_id = self.localcontext['data']['form']['company_id'][0]
        date_from = self.localcontext['data']['form']['date_from']
        date_to = self.localcontext['data']['form']['date_to']
        date_as_of = self.localcontext['data']['form']['date_as_of']
        fiscalyear_id = self.localcontext['data']['form']['fiscalyear_id'][0]
        period_length = self.localcontext['data']['form']['period_length']

        criteria = [
            ('company_id.id', '=', company_id),
            ('move_id.period_id.fiscalyear_id', '=', fiscalyear_id),
            ('journal_id.id', '=', journal_id),
            ('state', '=', 'posted')
        ]

        if date_from and not date_to:
            criteria.append(('date', '>=', date_from))
        if not date_from and date_to:
            criteria.append(('date', '<=', date_to))
        if date_from and date_to:
            criteria.append(('date', '>=', date_from))
            criteria.append(('date', '<=', date_to))

        context = {'date_as_of': date_as_of, 'period_length': period_length}

        data_list = []
        result = {}
        aging1 = aging2 = aging3 = aging4 = aging5 = 0.0
        current = 0.0

        line_ids = obj_line.search(self.cr, self.uid, criteria)

        if line_ids:
            no = 1
            for line in obj_line.browse(
                    self.cr, self.uid, line_ids, context=context):
                if line.amount_residual > 0:
                    conv_date = datetime.strptime(
                        line.date, '%Y-%m-%d').strftime('%d-%m-%Y')
                    conv_date_due = datetime.strptime(
                        line.date_due, '%Y-%m-%d').strftime('%d-%m-%Y')
                    if line.direction == 'past':
                        res = {
                            'no': no,
                            'date': conv_date,
                            'date_due': conv_date_due,
                            'transaction': line.move_id.name,
                            'description': line.name,
                            'partner': line.partner_id.name,
                            'current': 0.0,
                            'aging1': line.aging1,
                            'aging2': line.aging2,
                            'aging3': line.aging3,
                            'aging4': line.aging4,
                            'aging5': line.aging5,
                        }
                        aging1 += line.aging1
                        aging2 += line.aging2
                        aging3 += line.aging3
                        aging4 += line.aging4
                        aging5 += line.aging5
                    if line.direction == 'future':
                        res = {
                            'no': no,
                            'date': conv_date,
                            'date_due': conv_date_due,
                            'transaction': line.move_id.name,
                            'description': line.name,
                            'partner': line.partner_id.name,
                            'current': line.amount_residual,
                            'aging1': 0.0,
                            'aging2': 0.0,
                            'aging3': 0.0,
                            'aging4': 0.0,
                            'aging5': 0.0,
                        }
                        current += line.amount_residual

                    data_list.append(res)
                    no += 1

        result = {
            'data': data_list,
            'aging1': aging1,
            'aging2': aging2,
            'aging3': aging3,
            'aging4': aging4,
            'aging5': aging5,
            'current': current
        }
        return result
