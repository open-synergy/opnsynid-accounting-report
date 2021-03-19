# -*- coding: utf-8 -*-
# Copyright 2015 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Income statement report",
    "version": "8.0.1.1.0",
    "summary": "Income statement report",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "opnsynid_income_statement_account",
        "report_aeroo",
    ],
    "data": [
        "wizards/wizard_income_statement.xml",
        "reports/report_income_statement_ods.xml",
        "reports/report_income_statement_xls.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
    "license": "AGPL-3",
}
