# -*- coding: utf-8 -*-
# Copyright 2015 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Balance sheet report",
    "version": "8.0.2.0.0",
    "category": "Accounting",
    "summary": "Balance sheet report",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "depends": [
        "opnsynid_asset_account",
        "opnsynid_liablity_account",
        "report_aeroo",
    ],
    "data": [
        "wizards/wizard_balance_sheet.xml",
        "reports/report_balance_sheet_ods.xml",
        "reports/report_balance_sheet_xls.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
    "license": "AGPL-3",
}
