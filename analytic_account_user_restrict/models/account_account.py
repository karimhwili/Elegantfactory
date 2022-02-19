from odoo import fields, models, api


class AccountAccount(models.Model):
    _inherit = 'account.account'

    mandatory_analytic_account = fields.Boolean("Mandatory Analytic Account")
    analytic_accounts_ids = fields.Many2many('account.analytic.account', string="Analytic Accounts")

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    analytic_mandatory = fields.Boolean()

    @api.onchange('account_id')
    def get_analytic_account_id(self):
        for rec in self:
            if rec.account_id.mandatory_analytic_account:
                rec.analytic_mandatory = True
                if rec.account_id.analytic_accounts_ids:
                    rec.analytic_account_id = False
                    return {
                        'domain': {
                            'analytic_account_id': [('id', 'in',rec.account_id.analytic_accounts_ids.ids)]
                        }
                    }
                else:
                    rec.analytic_account_id = False

            else:
                rec.analytic_mandatory = False

