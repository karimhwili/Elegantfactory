# -*- coding: utf-8 -*-
{
    'name': "Product Elegant",

    'author': "M.Shorbagy (Sahara)",

    'depends': ['base','stock','sale','purchase_stock','quality','quality_control'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/product_product.xml',
        'views/purchase_order.xml',
        'views/product_category.xml',
        'views/res_partner.xml',
        'views/group_limits.xml'
    ],

}
