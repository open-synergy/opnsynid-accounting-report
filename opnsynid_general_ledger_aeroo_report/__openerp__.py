# -*- coding: utf-8 -*-
# Copyright 2015 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "General Ledger Report",
    "version": "8.0.1.5.1",
    "summary": "Report General Ledger",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "account_accountant",
        "report_aeroo"
    ],
    "data": [
        "report/report_general_ledger.xml",
        "wizard/wizard_general_ledger.xml",
        "menu_Accounting.xml"
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "license": "AGPL-3"
}
