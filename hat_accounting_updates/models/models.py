# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class hat_accounting_updates(models.Model):
#     _name = 'hat_accounting_updates.hat_accounting_updates'
#     _description = 'hat_accounting_updates.hat_accounting_updates'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
