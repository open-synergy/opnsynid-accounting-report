# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Bank Statement Mutation Aeroo Report",
    "version": "8.0.1.0.0",
    "category": "Accounting",
    "website": "https://opensynergy-indonesia.com/",
    "author": "Andhitia Rama, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "report_aeroo",
        "account_accountant",
    ],
    "data": [
        "wizards/print_bank_statement_mutation_views.xml",
        "reports/bank_statement_mutation_reports.xml",
    ],
}
