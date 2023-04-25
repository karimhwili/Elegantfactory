from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_type = fields.Selection([('customer', 'Customer'), ('vendor', 'Vendor'), ('employee', 'Employee')],
                                    string="Type", default='employee')
