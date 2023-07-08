from odoo import fields, models, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    allowed_for_manual = fields.Boolean(copy=False, string="Allowed For Manual Entry")
