# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Payment Order Summary",
    "version": "8.0.1.0.0",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "report_aeroo",
        "account_payment",
    ],
    "data": [
        "reports/payment_order_summary_reports.xml",
        "wizards/print_payment_order_summary_views.xml",
    ],
}
