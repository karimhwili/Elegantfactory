# -*- coding: utf-8 -*-
{
    'name': "Accounting Elegant",

    'author': "M.Shorbagy (Sahara)",

    'version': '0.1.2',

    'depends': ['base', 'account_asset', 'hr', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'data/sequence.xml',
        'groups/groups.xml',
        'views/account_assets.xml',
        'views/journal_entry.xml',
        'views/stock_picking.xml',
        'views/product_category.xml',
        'views/account_account.xml',
        'wizards/invoice_reason_wizard.py.xml',
        'views/res_users.xml',
        'data/account_type.xml'

    ],

}
