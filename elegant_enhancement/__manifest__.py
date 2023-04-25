# -*- coding: utf-8 -*-
{
    'name': "Elegant Enhancement",
    'depends': ['base','sale_management', 'account','stock'],

    # always loaded
    'data': [
        'security/groups.xml',
        'views/account_move.xml',
        'views/sale_order.xml',
        'views/res_partner.xml',
        'views/account_journal.xml',
        'views/account_payment.xml',
        'views/product_template.xml',
    ],

}
