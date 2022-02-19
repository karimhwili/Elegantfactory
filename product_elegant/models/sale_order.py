
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.tools import get_lang


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
                for partner in line.product_id.limits_groups.group_limits:
                    if inv.partner_id == partner.customer_id:
                        inv_credit += line.price_subtotal

        for order in self:
            for line in order.order_line:
                for partner in line.product_id.limits_groups.group_limits:
                    if order.partner_id == partner.customer_id:
                        credit_product += line.price_subtotal
                    total_sales = inv_credit + credit_product
                    if total_sales > partner.limit:
                        raise ValidationError(_('You can not set amount for product %s more than %s',line.product_id.name,partner.limit))
        super(SaleOrderInherit, self).action_confirm()

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return
        valid_values = self.product_id.product_tmpl_id.valid_product_template_attribute_line_ids.product_template_value_ids
        # remove the is_custom values that don't belong to this template
        for pacv in self.product_custom_attribute_value_ids:
            if pacv.custom_product_template_attribute_value_id not in valid_values:
                self.product_custom_attribute_value_ids -= pacv

        # remove the no_variant attributes that don't belong to this template
        for ptav in self.product_no_variant_attribute_value_ids:
            if ptav._origin not in valid_values:
                self.product_no_variant_attribute_value_ids -= ptav

        vals = {}
        if not self.product_uom or (self.product_id.default_uom.id != self.product_uom.id):
            if self.product_id.default_uom:
                vals['product_uom'] = self.product_id.default_uom
            else:
                vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = self.product_uom_qty or 1.0


        product = self.product_id.with_context(
            lang=get_lang(self.env, self.order_id.partner_id.lang).code,
            partner=self.order_id.partner_id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )

        vals.update(name=self.get_sale_order_line_multiline_description_sale(product))

        self._compute_tax_id()

        if self.order_id.pricelist_id and self.order_id.partner_id:
            vals['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(
                self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
        self.update(vals)

        title = False
        message = False
        result = {}
        warning = {}
        if product.sale_line_warn != 'no-message':
            title = _("Warning for %s", product.name)
            message = product.sale_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            result = {'warning': warning}
            if product.sale_line_warn == 'block':
                self.product_id = False

        return result