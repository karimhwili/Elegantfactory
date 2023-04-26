from odoo import api, fields, models, _
from odoo import tools
import logging
from num2words import num2words


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    amount_total_words = fields.Char("Total (In Words)", compute="_compute_amount_total_words")

    @api.depends('amount')
    def _compute_amount_total_words(self):
        for payment in self:
            payment.amount_total_words = payment.currency_id.amount_to_text(payment.amount)


