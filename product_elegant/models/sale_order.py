
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        credit_product = 0
        for order in self.search([('state','in',('draft','sale'))]):
            for line in order.order_line:
                for partner in line.product_id.product_limits:
                    if order.partner_id == partner.customer_id:
                        credit_product += line.price_subtotal
                        if credit_product > partner.limit:
                            raise ValidationError(_('You can not set quantity for product %s more than %s',line.product_id.name,partner.limit))
        super(SaleOrderInherit, self).action_confirm()
