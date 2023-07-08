# -*- coding: utf-8 -*-
# from odoo import http


# class HatAccountingUpdates(http.Controller):
#     @http.route('/hat_accounting_updates/hat_accounting_updates/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hat_accounting_updates/hat_accounting_updates/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hat_accounting_updates.listing', {
#             'root': '/hat_accounting_updates/hat_accounting_updates',
#             'objects': http.request.env['hat_accounting_updates.hat_accounting_updates'].search([]),
#         })

#     @http.route('/hat_accounting_updates/hat_accounting_updates/objects/<model("hat_accounting_updates.hat_accounting_updates"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hat_accounting_updates.object', {
#             'object': obj
#         })
