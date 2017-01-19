# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Payment Instruction",
    "version": "8.0.1.0.0",
    "category": "Accounting",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "report_aeroo",
        "account_payment",
    ],
    "data": [
        "security/ir.model.access.csv",
        "reports/payment_instruction_reports.xml",
        "wizards/print_payment_instruction_views.xml",
    ],
}
