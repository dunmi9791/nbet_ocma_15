# -*- coding: utf-8 -*-

{
    'name': "Journal Voucher",
    'summary': """
        NBET Journal Voucher print out
        """,
    'description': """
        NBET Journal Voucher Template
    """,
    'author': "PGL",
    'website': "http://www.pglgroup.com",
    'category': 'Uncategorized',
    'version': '15.0.0.1',
    'depends': ['account'],
    'data': [
        'reports/report.xml',
        'reports/journal_voucher.xml',
        'reports/payment_voucher.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False
}
