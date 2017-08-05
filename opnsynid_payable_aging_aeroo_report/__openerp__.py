# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Payable Aging Report',
    'version': '8.0.1.0.0',
    'author': 'OpenSynergy Indonesia',
    'category': 'Accounting',
    'summary': 'Report Payable Aging',
    'website': 'https://opensynergy-indonesia.com',
    'depends': [
        'account_accountant',
        'report_aeroo'
    ],
    'data': [
        'security/ir.model.access.csv',
        'report/report_payable_aging_ods.xml',
        'report/report_payable_aging_xls.xml',
        'wizard/wizard_payable_aging.xml',
        'menu_Accounting.xml'
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
    'license': 'AGPL-3'
}
