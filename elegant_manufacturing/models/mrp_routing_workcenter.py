from odoo import fields, models, api


class MrpRoutingWorkcenter(models.Model):
    _inherit = 'mrp.routing.workcenter'

    workcenter_id = fields.Many2one('mrp.workcenter', 'Work Center', required=False, check_company=True)
    bom_id = fields.Many2one(
        'mrp.bom', 'Bill of Material',
        index=True, ondelete='cascade', required=False, check_company=True,
        help="The Bill of Material this operation is linked to")
    company_id = fields.Many2one('res.company', 'Company', related=False, default=lambda self: self.env.company)
