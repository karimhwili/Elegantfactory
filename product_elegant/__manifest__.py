# -*- coding: utf-8 -*-
{
    'name': "Employee Product",

    'author': "M.Shorbagy (Sahara)",

    'depends': ['base','stock','sale','purchase_stock','quality','quality_control'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_product.xml',
        'views/purchase_order.xml'
    ],

}
