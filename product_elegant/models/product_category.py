from odoo import fields, models, api


class ProductCategory(models.Model):
    _inherit = 'product.category'

    code = fields.Char("code")
