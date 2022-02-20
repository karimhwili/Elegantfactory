# -*- coding: utf-8 -*-
{
    'name': "Product Elegant",

    'author': "M.Shorbagy (Sahara)",

    'depends': ['base','stock','sale','purchase_stock','sale_stock','quality','quality_control','stock_landed_costs'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/product_product.xml',
        'views/purchase_order.xml',
        'views/product_category.xml',
        'views/res_partner.xml',
        'views/group_limits.xml',
        'views/stock_landed_cost.xml',
        'views/sale_order.xml',
    ],

}
