
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        for order in self.order_line:
            for partner in order.product_id.product_limits:
                if self.partner_id == partner.customer_id:
                    if order.product_uom_qty > partner.limit:
                        raise ValidationError(_('You can not set quantity for product %s more than %s',order.product_id.name,partner.limit))
        super(SaleOrderInherit, self).action_confirm()
