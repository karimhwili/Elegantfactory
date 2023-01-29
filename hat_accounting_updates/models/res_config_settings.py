from odoo import api, fields, models


class Company(models.Model):
    _inherit = 'res.company'

    so_minimum = fields.Float("Minimum Amount", )
    so_order_approval = fields.Boolean("Sale Order Approval", )


class ResDiscountSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    so_order_approval = fields.Boolean("Sale Order Approval")
    so_minimum = fields.Float("Minimum Amount", digits=[16, 3])

    @api.model
    def get_values(self):
        res = super(ResDiscountSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            so_order_approval=params.get_param('sale.so_order_approval') or False,
            so_minimum=params.get_param('sale.so_minimum') or False,
        )
        return res

    def set_values(self):
        self.ensure_one()
        super(ResDiscountSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("sale.so_order_approval", self.so_order_approval)
        self.env['ir.config_parameter'].sudo().set_param("sale.so_minimum", self.so_minimum)

