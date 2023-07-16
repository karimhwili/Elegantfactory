from odoo import fields, models, api, _
from odoo.exceptions import UserError

from num2words import num2words

import logging
from odoo import api, fields, models, tools, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    currency_ber_unit = fields.Float("Currency ber Unit", digits=[16, 3])

    @api.depends('currency_id.rate', 'currency_ber_unit')
    def _get_currency_rate(self):
        for rec in self:
            if rec.currency_ber_unit:
                rec.currency_rate = 1 / rec.currency_ber_unit
            else:
                rec.currency_rate = rec.currency_id.rate

    def fix_draft_payment(self):
        for rec in self:
            if rec.state == 'draft' and rec.move_id.state == 'posted':
                rec.state = 'posted'


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    # def amount_to_text(self, amount, lang='en_US'):
    #     self.ensure_one()
    #
    #     def amount_to_text(self, amount, lang='en_US'):
    #         self.ensure_one()
    #
    #         def _num2words(number, lang):
    #             lang = 'ar_SY'
    #             try:
    #                 return num2words(number, lang=lang).title()
    #             except NotImplementedError:
    #                 return num2words(number, lang='en').title()
    #
    #         if num2words is None:
    #             logging.getLogger(__name__).warning(
    #                 "The library 'num2words' is missing, cannot render textual amounts.")
    #             return ""
    #         formatted = "%.{0}f".format(self.decimal_places) % amount
    #         parts = formatted.partition('.')
    #         integer_value = int(parts[0])
    #         fractional_value = int(parts[2] or 0)
    #
    #         # lang = tools.get_lang(self.env)
    #         if self.currency_unit_label == "Dollars" and lang == 'ar_SY':
    #             amount_words = tools.ustr('{amt_value} {amt_word}').format(
    #                 amt_value=_num2words(integer_value, lang=lang),
    #                 amt_word=str(self.currency_unit_label.replace("Dollars", 'دولار')) + " فقط لا غير ",
    #             )
    #         elif self.currency_unit_label == "Pound" and lang == 'ar':
    #             amount_words = tools.ustr('{amt_value} {amt_word}').format(
    #                 amt_value=_num2words(integer_value, lang='ar_SY'),
    #                 amt_word=str(self.currency_unit_label.replace("Pound", 'جنية')) + " فقط لا غير ",
    #             )
    #         else:
    #             amount_words = tools.ustr('{amt_value} {amt_word}').format(
    #                 amt_value=_num2words(integer_value, lang=lang),
    #                 amt_word=self.currency_unit_label,
    #             )
    #         return amount_words
