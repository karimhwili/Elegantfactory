from odoo import api, fields, models


class Company(models.Model):
    _inherit = 'res.company'

    so_minimum = fields.Float("Minimum Amount", )
    so_order_approval = fields.Boolean("Sale Order Approval", )


class ResDiscountSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    so_order_approval = fields.Boolean("Sale Order Approval", related='company_id.so_order_approval', store=True,
                                       readonly=False)
    so_minimum = fields.Float("Minimum Amount", related='company_id.so_minimum', readonly=False, store=True,
                              digits=[16, 3], default=5000)
