# -*- coding: utf-8 -*-
# © 2015 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Receivable Aging Report',
    'version': '8.0.1.0.0',
    'author': 'OpenSynergy Indonesia',
    'category': 'Accounting',
    'summary': 'Report Receivable Aging',
    'website': 'https://opensynergy-indonesia.com',
    'depends': [
        'account_accountant',
        'report_aeroo'
    ],
    'data': [
        'security/ir.model.access.csv',
        'report/report_receivable_aging_ods.xml',
        'report/report_receivable_aging_xls.xml',
        'wizard/wizard_receivable_aging.xml',
        'menu_Accounting.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'AGPL-3'
}
