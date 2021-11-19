# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "General Ledger Report",
    "version": "8.0.1.0.0",
    "category": "Accounting",
    "summary": "Report General Ledger",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "depends": [
        "opnsynid_general_ledger_aeroo_report",
        "account_operating_unit",
    ],
    "data": [
        "wizard/wizard_general_ledger.xml",
        "report/report_general_ledger.xml",
    ],
    "installable": True,
    "auto_install": True,
    "application": True,
    "license": "AGPL-3",
}
