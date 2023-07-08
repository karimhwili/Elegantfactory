from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    picking_name = fields.Char(
        string='Picking Name',
        required=False, )
    po_picking_name = fields.Char(
        string='Po Picking Name',
        required=False, )
    loan_id = fields.Many2one(
        comodel_name='hr.loan',
        string='Loan',
        required=False)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    available_analytic_account = fields.Boolean(
        string='Available Analytic Account',
        required=False, related='account_id.available_analytic_account')
    available_analytic_tag = fields.Boolean(
        string='Available Analytic Tag',
        required=False, related='account_id.available_analytic_tag')
