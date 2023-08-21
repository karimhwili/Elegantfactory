from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_type = fields.Selection(
        [('customer', 'Customer'), ('vendor', 'Vendor'), ('both', 'Both'), ('employee', 'Employee')],
        string="Type", )
    agent = fields.Many2one('hr.employee', "Agent")
