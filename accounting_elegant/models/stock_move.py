from odoo import api, fields, models
from odoo.tools import float_round, float_compare


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id, description):
        """
        Generate the account.move.line values to post to track the stock valuation difference due to the
        processing of the given quant.
        """
        self.ensure_one()

        # the standard_price of the product may be in another decimal precision, or not compatible with the coinage of
        # the company currency... so we need to use round() before creating the accounting entries.
        debit_value = self.company_id.currency_id.round(cost)
        credit_value = debit_value
        if self.picking_id.account_id:
            if self.picking_id.picking_type_id.code == 'outgoing' or self.picking_id.picking_type_id.code == 'internal':
                debit_account_id = self.picking_id.account_id.id
        else:
            if self.scrapped and self.product_id.categ_id.property_scrap_account_id:
                debit_account_id = self.product_id.categ_id.property_scrap_account_id.id

            elif not self.scrapped and self.product_id.categ_id.income_add_stock_account_id and self.location_dest_id.usage == 'internal' and self.reference == 'Product Quantity Updated':
                credit_account_id = self.product_id.categ_id.income_add_stock_account_id.id
            elif not self.scrapped and self.product_id.categ_id.income_add_stock_account_id and self.reference == 'Product Quantity Updated':
                if self.product_uom_qty < self.product_id.qty_available:
                    debit_account_id = self.product_id.categ_id.income_add_stock_account_id.id
            elif self.inventory_id:
                if not self.scrapped and self.product_id.categ_id.income_add_stock_account_id and self.reference == 'INV:' + self.inventory_id.name or '':
                    for line in self.inventory_id.line_ids:
                        if line.difference_qty > 0:
                            credit_account_id = self.product_id.categ_id.income_add_stock_account_id.id
                        elif line.difference_qty < 0:
                            debit_account_id = self.product_id.categ_id.income_add_stock_account_id.id

        valuation_partner_id = self._get_partner_id_for_valuation_lines()
        res = [(0, 0, line_vals) for line_vals in self._generate_valuation_lines_data(valuation_partner_id,
                                                                                      qty, debit_value, credit_value, debit_account_id, credit_account_id, description).values()]

        return res
