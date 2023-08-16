from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_id = fields.Many2one(
        'res.partner', string='Customer', readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        required=True, change_default=True, index=True, tracking=1,
        domain="[('partner_type', 'in', ['customer','both'])]", )
    agent = fields.Many2one('hr.employee', related='partner_id.agent',store=True)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    can_edit_price_unit = fields.Boolean(copy=False)

    @api.onchange('product_id')
    def check_edit_price_unit(self):
        if not self.env.user.has_group('elegant_enhancement.can_edit_price_unit_in_sales'):
            self.can_edit_price_unit = False
        else:
            self.can_edit_price_unit = True
