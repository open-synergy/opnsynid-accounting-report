# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Income statement report based on date",
    "version": "8.0.1.0.0",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "opnsynid_income_statement_aeroo_report",
    ],
    "data": [
        "wizards/wizard_income_statement_bydate.xml",
        "reports/report_income_statement_bydate_ods.xml",
        "reports/report_income_statement_bydate_xls.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
    "license": "AGPL-3",
}
