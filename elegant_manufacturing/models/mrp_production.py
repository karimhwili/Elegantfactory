from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    workcenter_id = fields.Many2one('mrp.workcenter', "Work Center")

    bom_id = fields.Many2one(
        'mrp.bom', 'Bill of Material',
        readonly=True, states={'draft': [('readonly', False)]},
        domain=False,
        check_company=True,
        help="Bill of Materials allow you to define the list of required components to make a finished product.")

    @api.onchange('workcenter_id')
    def get_bom_relatedof_workcenter(self):
        for rec in self:
            operations_ids = [(5, 0, 0)]
            for operation in rec.workcenter_id.operations_ids:
                operations_ids.append((0, 0, {
                    'name': operation.operation_id.name,
                    'workcenter_id': rec.workcenter_id.id,
                    'production_id': rec.id,
                    'product_uom_id': rec.product_uom_id.id,
                    'operation_id': operation.id,
                    'state': 'pending',
                    'consumption': 'flexible',
                }))
            rec.workorder_ids = operations_ids
            # if rec.workcenter_id:
            #     bom_ids = rec.workcenter_id.bom_ids.ids
            #     print("bom",bom_ids)
            #     rec.bom_id = False
            #     return {
            #         'domain': {
            #             'bom_id': [('id', 'in', bom_ids)]
            #         }
            #     }

    @api.onchange('bom_id', 'product_id')
    def _onchange_workorder_ids(self):
        pass

    @api.onchange('bom_id')
    def _onchange_bom_id(self):
        if not self.product_id and self.bom_id:
            self.product_id = self.bom_id.product_id or self.bom_id.product_tmpl_id.product_variant_ids[0]
        self.product_qty = self.bom_id.product_qty or 1.0
        self.product_uom_id = self.bom_id and self.bom_id.product_uom_id.id or self.product_id.uom_id.id
        self.move_raw_ids = [(2, move.id) for move in self.move_raw_ids.filtered(lambda m: m.bom_line_id)]
        self.move_finished_ids = [(2, move.id) for move in self.move_finished_ids]
        self.picking_type_id = self.bom_id.picking_type_id or self.picking_type_id
