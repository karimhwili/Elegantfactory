from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    check_quality = fields.Boolean(compute='_get_check_quality',store=True,default=False)

    @api.depends('picking_ids.state','picking_ids.quality_check_fail')
    def _get_check_quality(self):
        for rec in self:
            for picking in self.picking_ids:
                if picking.state == 'done' and picking.quality_check_fail == False:
                    rec.check_quality = True
                else:
                    rec.check_quality = False




