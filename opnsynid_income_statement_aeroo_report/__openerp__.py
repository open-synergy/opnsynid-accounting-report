# -*- coding: utf-8 -*-
# © 2015 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Income statement report',
    'version': '8.0.1.0.0',
    'author': 'OpenSynergy Indonesia',
    'category': 'Accounting',
    'summary': 'Income statement report',
    'website': 'https://opensynergy-indonesia.com',
    'depends': [
        'opnsynid_income_statement_account',
        'report_aeroo',
        ],
    'data': [
        'wizards/wizard_income_statement.xml',
        'reports/report_income_statement_ods.xml',
        'reports/report_income_statement_xls.xml',
        ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'AGPL-3',
}
