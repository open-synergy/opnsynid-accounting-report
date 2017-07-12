# -*- coding: utf-8 -*-
# © 2015 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Trial Balance Report',
    'version': '8.0.1.0.1',
    'author': 'OpenSynergy Indonesia',
    'category': 'Accounting',
    'summary': 'Report Trial Balance',
    'website': 'https://opensynergy-indonesia.com',
    'depends': [
        'account_accountant',
        'report_aeroo'
    ],
    'data': [
        'security/ir.model.access.csv',
        'report/report_trial_balance.xml',
        'wizard/wizard_trial_balance.xml',
        'menu_Accounting.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'AGPL-3'
}
