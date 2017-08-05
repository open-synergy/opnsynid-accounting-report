# -*- coding: utf-8 -*-
# © 2015 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Asset Accounts Configurator Helper',
    'version': '8.0.1.0.0',
    'author': 'OpenSynergy Indonesia',
    'category': 'Accounting',
    'summary': 'Asset view helper',
    'website': 'https://opensynergy-indonesia.com',
    'depends': [
        'opnsynid_accounting_report_configuration_page',
        ],
    'data': [
        'views/res_company_view.xml',
        ],
    'installable': False,
    'auto_install': False,
    'application': False,
    'license': 'AGPL-3',
}
