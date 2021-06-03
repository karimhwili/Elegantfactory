from odoo import fields, models, api
from odoo.addons.account.models.account_move import AccountMove as AccountMove1

class AccountAccount(models.Model):
    _inherit = 'account.account'

    force_auto = fields.Boolean("Force Automation")
    transfer_type = fields.Selection([('cash_to_bank', 'Cash to Bank'),
                                      ('cash_to_cash', 'Cash to Cash'),
                                      ('bank_to_bank', 'Bank to Bank'),
                                      ('salaries', 'Salaries'),
                                      ('other_payments', 'Other Payments'),
                                      ('other_receipts', 'Other Receipts'),
                                      ('loans', 'Loans'),
                                      ('not_required', 'Not Required'),],default='not_required' ,string="Transfer Type")

class AccountMove(models.Model):
    _inherit = 'account.move'

    reason = fields.Char("Reason for Cancel")
    is_reason = fields.Boolean()


    def unlink(self):
        for move in self:
            if move.posted_before and not self._context.get('force_delete'):
                # raise UserError(_("You cannot delete an entry which has been posted once."))
                continue
        self.line_ids.unlink()
        # return super(AccountMove, self).unlink()

    AccountMove1.unlink = unlink
    def button_cancel(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Warning : you must select reason',
            'res_model': 'reason.invoice',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('accounting_elegant.pause_reason_wizard_view_form', False).id,
            'target': 'new',
        }

    def cancel_invoice(self):
        self.write({'auto_post': False, 'state': 'cancel','is_reason':True})
#
# class Account(models.Model):
#     _inherit = 'account.journal'
#
#     next_link_synchronization = fields.Char()
#     account_online_account_id = fields.Char()
#     account_online_link_state = fields.Char()
#     bank_statement_creation_groupby = fields.Char()