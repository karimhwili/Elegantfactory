from odoo import fields, models, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',
                                          index=True, compute="_compute_analytic_account", store=True, readonly=False,
                                          check_company=True, copy=True,required=True)

