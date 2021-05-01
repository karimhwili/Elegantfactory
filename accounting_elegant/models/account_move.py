from odoo import fields, models, api


class AccountAccount(models.Model):
    _inherit = 'account.account'

    force_auto = fields.Boolean("Force Automation")

class AccountMove(models.Model):
    _inherit = 'account.move'

    reason = fields.Char("Reason for Cancel")
    is_reason = fields.Boolean()

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



class AccountJournal(models.Model):
    _inherit = 'account.journal'

    next_link_synchronization = fields.Char("Force Automation")
    account_online_account_id = fields.Char("Force Automation")
    account_online_link_state = fields.Char("Force Automation")

