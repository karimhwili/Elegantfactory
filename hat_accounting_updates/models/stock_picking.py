from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # @api.model
    # def create(self, vals):
    #     res = super(StockPicking, self).create(vals)
    #     if self.move_ids_without_package and res.purchase_id.order_line and not res.move_line_ids_without_package[
    #         0].lot_id:
    #         print(("^^^^^^^^^^^^^^^^^^^^^^^^"))
    #
    #         res.write(vals)
    #     # self.move_line_ids_without_package['lot_id'] = res.purchase_id.order_line.lot_id.id
    #     print(("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"))
    #     return res
    #
    # def write(self, vals):
    #     print('####################', vals)
    #     if self.move_ids_without_package and self.purchase_id.order_line and not self.move_line_ids_without_package[
    #         0].lot_id:
    #         print("@@@@@@@@@@@@@@@@@@@@@", self.purchase_id.order_line[0].lot_id)
    #         self.move_line_ids_without_package['lot_id'] = self.purchase_id.order_line[0].lot_id.id
    #         print("$$$$$$$$$$$$$$$$$$$$$$$$", self.move_ids_without_package['lot_ids'])
    #
    #     return super(StockPicking, self).write(vals)
