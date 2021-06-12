import math

from odoo import api, fields, models, _
from odoo.exceptions import AccessError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_enabled_roundoff = fields.Boolean('Enabled Roundoff',
                                         default=lambda self: self.env["ir.config_parameter"].sudo().get_param(
                                             "account.invoice_roundoff"))
    amount_round_off = fields.Monetary(string='Roundoff Amount', store=True, readonly=True, compute='_amount_all')

    @api.depends('order_line.price_total','order_line.price_tax','order_line.price_subtotal')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0; amount_round_off =0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
            })
            if order.is_enabled_roundoff == True:
                val = order.amount_total
                if (float(val) % 1) >= 0.5:
                    amount_total = math.ceil(val)
                elif (float(val) % 1) < 0.5 and (float(val) % 1) > 0:
                    amount_total = round(val) + 0.5
                else:
                    amount_total = 0
                if order.amount_total and amount_total:
                    amount_round_off = amount_total - order.amount_total
                    order.update({
                        'amount_total': amount_total,
                        'amount_round_off': amount_round_off})
                else:
                    order.update({
                        'amount_total': order.amount_total,
                        'amount_round_off': 0.00})
                    
                    
                    
                    
                    
                    
                    