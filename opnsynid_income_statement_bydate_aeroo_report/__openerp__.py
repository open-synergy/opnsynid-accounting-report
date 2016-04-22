# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Income statement report based on date',
    'version': '8.0.1.0.0',
    'author': 'OpenSynergy Indonesia',
    'category': 'Accounting',
    'website': 'https://opensynergy-indonesia.com',
    'depends': [
        'opnsynid_income_statement_aeroo_report',
    ],
    'data': [
        'wizards/wizard_income_statement_bydate.xml',
        'reports/report_income_statement_bydate_ods.xml',
        'reports/report_income_statement_bydate_xls.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'AGPL-3',
}
