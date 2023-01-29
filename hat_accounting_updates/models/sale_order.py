from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    picking_name = fields.Char(
        string='Picking Name',
        required=False, compute='get_picking_seq')

    @api.depends("picking_ids", "picking_ids.name")
    def get_picking_seq(self):
        for order in self:
            if order.picking_ids:
                first_picking = order.picking_ids.filtered(lambda x: x.state != 'cancel')[0]
                if first_picking:
                    order.picking_name = first_picking.name
                else:
                    order.picking_name = False
            else:
                order.picking_name = False

    state = fields.Selection(selection_add=[('to_approve', 'To Approve'), ])

    def button_action_approved(self):
        self.action_confirm()

    def action_confirm(self):
        if self.user_has_groups('sales_team.group_sale_salesman') or self.user_has_groups(
                'sales_team.group_sale_salesman_all_leads'):
            so_minium = self.env["ir.config_parameter"].sudo().get_param("sale.so_minimum")
            if self.amount_total > so_minium:
                self.state = 'to_approve'
            else:
                return super(SaleOrder, self).action_confirm()
        if self.user_has_groups('sales_team.group_sale_manager'):
            return super(SaleOrder, self).action_confirm()

    def _prepare_invoice(self, ):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({
            'picking_name': self.picking_name
        })
        return invoice_vals

    @api.model
    def _prepare_purchase_order_line_data(self, so_line, date_order, company):
        """ Generate purchase order line values, from the SO line
            :param so_line : origin SO line
            :rtype so_line : sale.order.line record
            :param date_order : the date of the orgin SO
            :param company : the company in which the PO line will be created
            :rtype company : res.company record
        """
        # price on PO so_line should be so_line - discount
        price = so_line.price_unit - (so_line.price_unit * (so_line.discount / 100))
        quantity = so_line.product_id and so_line.product_uom._compute_quantity(so_line.product_uom_qty,
                                                                                so_line.product_id.uom_po_id) or so_line.product_uom_qty
        price = so_line.product_id and so_line.product_uom._compute_price(price, so_line.product_id.uom_po_id) or price
        return {
            'name': so_line.name,
            'product_qty': quantity,
            'product_id': so_line.product_id and so_line.product_id.id or False,
            'product_uom': so_line.product_id and so_line.product_id.uom_po_id.id or so_line.product_uom.id,
            'price_unit': price or 0.0,
            'company_id': company.id,
            'date_planned': so_line.order_id.expected_date or date_order,
            'display_type': so_line.display_type,
            'lot_id': so_line.lot_id.id,
        }
