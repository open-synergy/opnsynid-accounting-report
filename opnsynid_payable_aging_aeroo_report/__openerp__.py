# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Payable Aging Report",
    "version": "8.0.1.2.0",
    "author": "PT. Simetri Sinergi Indonesia,OpenSynergy Indonesia",
    "category": "Accounting",
    "summary": "Report Payable Aging",
    "website": "https://simetri-sinergi.id",
    "depends": ["account_accountant", "report_aeroo"],
    "data": [
        "security/ir.model.access.csv",
        "report/report_payable_aging_ods.xml",
        "report/report_payable_aging_xls.xml",
        "wizard/wizard_payable_aging.xml",
        "menu_Accounting.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
    "license": "AGPL-3",
}
