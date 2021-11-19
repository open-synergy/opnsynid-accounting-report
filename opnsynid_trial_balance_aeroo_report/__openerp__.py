# -*- coding: utf-8 -*-
# Copyright 2015 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Trial Balance Report",
    "version": "8.0.2.1.0",
    "category": "Accounting",
    "summary": "Report Trial Balance",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "account_accountant",
        "report_aeroo",
        "web_m2x_options",
    ],
    "data": [
        "report/report_trial_balance.xml",
        "wizard/wizard_trial_balance.xml",
        "menu_Accounting.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "license": "AGPL-3",
}
