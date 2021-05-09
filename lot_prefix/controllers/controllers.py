# -*- coding: utf-8 -*-
# from odoo import http


# class LotPrefix(http.Controller):
#     @http.route('/lot_prefix/lot_prefix/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lot_prefix/lot_prefix/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lot_prefix.listing', {
#             'root': '/lot_prefix/lot_prefix',
#             'objects': http.request.env['lot_prefix.lot_prefix'].search([]),
#         })

#     @http.route('/lot_prefix/lot_prefix/objects/<model("lot_prefix.lot_prefix"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lot_prefix.object', {
#             'object': obj
#         })
