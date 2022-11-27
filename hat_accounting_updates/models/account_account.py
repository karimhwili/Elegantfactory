from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountAccount(models.Model):
    _inherit = 'account.account'
    available_analytic_account = fields.Boolean(
        string='Available Analytic Account',
        required=False)
    available_analytic_tag = fields.Boolean(
        string='Available Analytic Tag',
        required=False)
