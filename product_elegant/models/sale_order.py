
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        credit_product = 0
        inv_credit = 0

        inv_rec = self.env['account.move'].search([
            ('partner_id', '=', self.partner_id.id),
            ('amount_residual','!=',0.0)])

        for inv in inv_rec:
            for line in inv.invoice_line_ids:
                for partner in line.product_id.product_limits:
                    if inv.partner_id == partner.customer_id:
                        inv_credit += line.price_subtotal

        for order in self:
            for line in order.order_line:
                for partner in line.product_id.product_limits:
                    if order.partner_id == partner.customer_id:
                        credit_product += line.price_subtotal
                    total_sales = inv_credit + credit_product
                    if total_sales > partner.limit:
                        raise ValidationError(_('You can not set amount for product %s more than %s',line.product_id.name,partner.limit))
        super(SaleOrderInherit, self).action_confirm()
