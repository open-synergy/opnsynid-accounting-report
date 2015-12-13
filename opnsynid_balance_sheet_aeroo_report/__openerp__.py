# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Balance sheet report',
    'version': '8.0.1.0.0',
    'author': 'OpenSynergy Indonesia,Andhitia Rama,Michael Viriyananda',
    'category': 'Accounting',
    'summary': 'Balance sheet report',
    'description': """
    """,
    'website': 'https://opensynergy-indonesia.com',
    'images': [],
    'depends': [
        'account',
        'aeroo_report',
        ],
    'data': [
        'wizards/wizard_balance_sheet.xml',
        'reports/report_balance_sheet_ods.xml',
        'reports/report_balance_sheet_xls.xml',
        ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'AGPL-3',
}
