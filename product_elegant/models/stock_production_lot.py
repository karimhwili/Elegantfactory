from odoo import fields, models, api, _


class ProductionLotInherit(models.Model):
    _inherit = 'stock.production.lot'

    name = fields.Char(index=True, default='New')

    @api.model
    def create(self, vals):
        res = super(ProductionLotInherit, self).create(vals)
        if vals.get('name', _('New')) == _('New'):
            res.name = res.product_id.tag_lot + self.env['ir.sequence'].next_by_code(
                'stock.lot.serial') or _('New')

        return res

