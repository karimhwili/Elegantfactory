from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    partner_id = fields.Many2one('res.partner', string='Vendor', required=True,
                                 change_default=True, tracking=True,
                                 domain="[('partner_type', 'in', ['vendor','employee'])]",
                                 help="You can find a vendor by its Name, TIN, Email or Internal Reference.")
