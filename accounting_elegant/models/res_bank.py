from odoo import fields, models, api,_
from odoo.exceptions import UserError


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    def build_qr_code_url(self, amount, free_communication, structured_communication, currency, debtor_partner,
                          qr_method=None, silent_errors=True):
        """ Returns the QR-code report URL to pay to this account with the given parameters,
        or None if no QR-code could be generated.

        :param amount: The amount to be paid
        :param free_communication: Free communication to add to the payment when generating one with the QR-code
        :param structured_communication: Structured communication to add to the payment when generating one with the QR-code
        :param currency: The currency in which amount is expressed
        :param debtor_partner: The partner to which this QR-code is aimed (so the one who will have to pay)
        :param qr_method: The QR generation method to be used to make the QR-code. If None, the first one giving a result will be used.
        :param silent_errors: If true, forbids errors to be raised if some tested QR-code format can't be generated because of incorrect data.
        """
        if not self:
            return None

        self.ensure_one()

        if not currency:
            raise UserError(_("Currency must always be provided in order to generate a QR-code"))

        available_qr_methods = self.get_available_qr_methods_in_sequence()
        candidate_methods = qr_method and [(qr_method, dict(available_qr_methods)[qr_method])] or available_qr_methods
        for candidate_method, candidate_name in candidate_methods:
            if self._eligible_for_qr_code(candidate_method, debtor_partner, currency):
                error_message = self._check_for_qr_code_errors(candidate_method, amount, currency, debtor_partner,
                                                               free_communication, structured_communication)

                if not error_message:
                    return self._get_qr_code_url(candidate_method, amount, currency, debtor_partner, free_communication,
                                                 structured_communication)

                elif not silent_errors:
                    error_header = _(
                        "The following error prevented '%s' QR-code to be generated though it was detected as eligible: ",
                        candidate_name)
                    raise UserError(error_header + error_message)

        return None
