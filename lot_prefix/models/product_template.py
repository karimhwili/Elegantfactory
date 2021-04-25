from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    lot_tag = fields.Char('Lot Tag')
