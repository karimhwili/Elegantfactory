# -*- coding: utf-8 -*-
{
    'name': "Lot Prefix",

    'summary': """
        Specify the lot prefix on the product level""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Sahara International Group",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
