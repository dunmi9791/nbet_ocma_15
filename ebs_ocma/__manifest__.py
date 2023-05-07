# -*- coding: utf-8 -*-
{
    'name': "ebs_ocma",

    'summary': """
        This module manages Gencos, Discos, Genco Invoicing and Disco Invoicing""",

    'description': """
        The features that the module manages are:
        - Gencos Setup
        - Discos Setup
        - Gencos Invoicing
        - Gencos Invoicing
    """,

    'author': "PGL",
    'website': "http://www.pglgroup.com",

    'category': 'Uncategorized',
    'version': '0.2',
    'license': 'LGPL-3',

    'depends': [
        'base', 
        'account',
        'board',
        'contacts',
        'hr',
        'ks_dashboard_ninja',
    ],

    'data': [
        'wizard/genco_invoice_verification.xml',
        'wizard/disco_mro_application_views.xml',
        'wizard/rate_compute.xml',
        'wizard/input_import.xml',
        'wizard/parameters_input.xml',
        'data/sequence.xml',
        'data/precision.xml',
        'data/ocma_account_journals.xml',
        'security/ir.model.access.csv',
        'views/dashboard.xml',
        'views/genco_analytics.xml',
        'views/billing_cycle_views.xml',
        'views/res_partner_views.xml',
        'views/genco_invoice_views.xml',
        'views/disco_mro_views.xml',
        'views/disco_invoice_views.xml',
        'views/disco_invoicing.xml',
        'views/myto_rate_views.xml',
        'views/actions.xml',
        'views/menu.xml',
    ],

    'demo': [
        'demo/ocma_demo.xml',
    ],
}