from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResUsers(models.Model):
    _inherit = 'res.users'

    computed_balance = fields.Boolean("Make statement with negative value")


class AccountStatement(models.Model):
    _inherit = 'account.bank.statement'

    @api.constrains('balance_end')
    def _check_balance_end(self):
        for rec in self:
            if rec.balance_end < 0 and rec.user_id.computed_balance == False:
                raise ValidationError(_('The Computed Balance should be Positive.'))
