
from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"


    @api.onchange("partner_id")
    def _onchange_partner_id_default_journals(self):
        if self.partner_id and self.partner_id.default_journal_ids:
            if len(self.partner_id.default_journal_ids.ids) == 1:
                self.journal_id = self.partner_id.default_journal_ids.ids[0]
            else:
                self.journal_id = False

                return {
                    'domain': {
                        'journal_id': [('id', 'in', self.partner_id.default_journal_ids.ids)]
                    }
                }
