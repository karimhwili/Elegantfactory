from odoo import fields, models, api


class InheritProduct(models.Model):
    _inherit = 'product.template'

    tag_lot = fields.Char("Tag Lot")
    product_limits = fields.One2many('product.limits','product_id',"Product Limits")


class ProductLimits(models.Model):
    _name = 'product.limits'
    _description = 'Product Limits'

    product_id = fields.Many2one('product.template')
    customer_id = fields.Many2one('res.partner',"Customer")
    limit = fields.Integer("Limit")


