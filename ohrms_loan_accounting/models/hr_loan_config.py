from odoo import models, fields, api, _


class AccConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    loan_approve = fields.Boolean(default=False, string="Approval from Accounting Department",
                                  help="Loan Approval from account manager")

    treasury_account = fields.Many2one('account.account', "Treasury Account")
    loan_account = fields.Many2one('account.account', "Loan Journal")
    loan_journal = fields.Many2one('account.journal', "Loan Journal")

    @api.model
    def get_values(self):
        res = super(AccConfig, self).get_values()
        res.update(
            treasury_account=int(
                self.env['ir.config_parameter'].sudo().get_param('account.treasury_account')),
            loan_account=int(
                self.env['ir.config_parameter'].sudo().get_param('account.loan_account')),
            loan_journal=int(self.env['ir.config_parameter'].sudo().get_param('account.loan_journal'))
        )
        return res

    def set_values(self):
        super(AccConfig, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('account.treasury_account',
                                                         self.treasury_account.id)
        self.env['ir.config_parameter'].sudo().set_param('account.loan_account',
                                                         self.loan_account.id)
        self.env['ir.config_parameter'].sudo().set_param('account.loan_journal', self.loan_journal.id)

