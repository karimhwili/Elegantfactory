from odoo import fields, models, api, _
from odoo.addons.account.models.account_move import AccountMove as AccountMove1
from odoo.exceptions import UserError


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
                                      ('treasury', 'Treasury'),
                                      ('statement', 'Statement'),
                                      ('not_required', 'Not Required'),],default='not_required' ,string="Transfer Type")

class AccountMove(models.Model):
    _inherit = 'account.move'

    reason = fields.Char("Reason for Cancel")
    is_reason = fields.Boolean()
    entry_type = fields.Selection([('entry','Journal Entry'),
                             ('statement','Statement Entry')],default='entry',string="Entry Type")






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

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    entry_type = fields.Selection([('entry', 'Journal Entry'),
                             ('statement', 'Statement Entry')], string="Entry Type")

    @api.onchange('entry_type')
    def account_type(self):
        if self.entry_type == 'statement':
            return {
                'domain': {
                    'account_id': [('transfer_type', '=', 'statement'),
                                               ]
                }
            }
        else:
            return {
                'domain': {
                    'account_id': [('transfer_type', '!=', 'statement'),
                                   ]
                }
            }

    @api.onchange('partner_id')
    def get_partner_account(self):
        if self.partner_id and self.partner_id.customer_rank > 0:
            self.account_id = self.partner_id.property_account_receivable_id.id
        elif self.partner_id and self.partner_id.supplier_rank > 0:
            self.account_id = self.partner_id.property_account_payable_id.id


# class Account(models.Model):
#     _inherit = 'account.journal'
#
#     next_link_synchronization = fields.Char()
#     account_online_account_id = fields.Char()
#     account_online_link_state = fields.Char()
#     bank_statement_creation_groupby = fields.Char()