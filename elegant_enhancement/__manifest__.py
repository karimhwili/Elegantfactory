# -*- coding: utf-8 -*-
{
    'name': "Elegant Enhancement",
    'depends': ['base','sale_management', 'account','stock','sales_team'],

    # always loaded
    'data': [
        'security/groups.xml',
        'views/account_move.xml',
        'views/sale_order.xml',
        'views/res_partner.xml',
        'views/account_journal.xml',
        'views/account_payment.xml',
        'views/product_template.xml',
        'views/stock_picking.xml',
        'reports/report_receipt_action.xml',
        'reports/report_receipt_template.xml',
    ],

}
