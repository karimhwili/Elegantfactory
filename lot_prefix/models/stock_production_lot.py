from odoo import api, fields, models


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    @api.onchange("product_id")
    def _onchange_product_id(self):
        self.update(
            {
                'name': self.product_id.lot_tag + self.name}
        )
