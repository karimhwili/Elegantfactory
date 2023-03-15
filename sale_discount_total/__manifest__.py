# -*- coding: utf-8 -*-


{
    'name': 'Sale Discount on Total Amount',
    'version': '14.0.1.1.0',
    'category': 'Sales Management',
    'live_test_url': 'https://www.youtube.com/watch?v=CigmHe9iC4s&feature=youtu.be',
    'summary': "Discount on Total in Sale and Invoice With Discount Limit and Approval",
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'website': 'http://www.cybrosys.com',
    'description': """

Sale Discount for Total Amount
=======================
Module to manage discount on total amount in Sale.
        as an specific amount or percentage
""",
    'depends': ['sale',
                'account',
                ],
    'data': [
        'security/security.xml',
        'views/sale_view.xml',
        'views/account_invoice_view.xml',
        'views/invoice_report.xml',
        'views/sale_order_report.xml',
        'views/sales_team.xml',
        # 'views/res_config_view.xml',

    ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'application': True,
    'installable': True,
    'auto_install': False,
}
