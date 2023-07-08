# -*- coding: utf-8 -*-
{
    'name': "Accounting Updates",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'OPL-1',
    'depends': ['base', 'account', 'purchase', 'sale', 'stock', 'sale_stock', 'sale_purchase_inter_company_rules',
                'accounting_elegant', 'hr_payroll', 'hr', 'ohrms_loan'],

    'data': [
        'security/groups.xml',
        'reports/quotation_order_report.xml',
        'reports/purchase_order_report.xml',
        'reports/invoice_report.xml',
        'reports/payment_report.xml',
        'views/account_account.xml',
        'views/sale_order.xml',
        'views/hr_loan.xml',
        'views/account_payment.xml',
        'views/account_move.xml',
        'views/res_config_view.xml',
        'views/purchase_order.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
