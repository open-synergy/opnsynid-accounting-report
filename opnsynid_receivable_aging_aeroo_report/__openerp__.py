# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Receivable Aging Report",
    "version": "8.0.1.3.1",
    "author": "PT. Simetri Sinergi Indonesia,OpenSynergy Indonesia",
    "category": "Accounting",
    "summary": "Report Receivable Aging",
    "website": "https://simetri-sinergi.id",
    "depends": ["account_accountant", "report_aeroo"],
    "data": [
        "security/ir.model.access.csv",
        "report/report_receivable_aging_ods.xml",
        "report/report_receivable_aging_xls.xml",
        "wizard/wizard_receivable_aging.xml",
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
