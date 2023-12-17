from odoo import api, fields, models, _
from odoo import tools
import logging
from num2words import num2words


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    amount_total_words = fields.Char("Total (In Words)", compute="_compute_amount_total_words")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('posted', 'Posted'),
        ('cancelled', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, tracking=True, default='draft', index=True, required=True)


    def action_approve(self):
        if self.payment_type == 'inbound':
            self.state = 'posted'
            self.move_id._post(soft=False)
        else:
            self.state = 'approved'

    def action_post(self):
        ''' draft -> posted '''
        self.state = 'posted'
        self.move_id._post(soft=False)

    def action_cancel(self):
        ''' draft -> cancelled '''
        self.state = 'cancelled'
        self.move_id.button_cancel()

    def action_draft(self):
        ''' posted -> draft '''
        self.state = 'draft'
        self.move_id.button_draft()


    @api.depends('amount')
    def _compute_amount_total_words(self):
        for payment in self:
            payment.amount_total_words = payment.currency_id.amount_to_text(payment.amount)
