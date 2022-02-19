from odoo import fields, models, api, _
from odoo.addons.account.models.account_move import AccountMove as AccountMove1
from odoo.exceptions import UserError, ValidationError


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
                                      ('not_required', 'Not Required'), ], default='not_required',
                                     string="Transfer Type")




class AccountMove(models.Model):
    _inherit = 'account.move'
    #
    # @api.model
    # def _get_default_journal(self):
    #     ''' Get the default journal.
    #     It could either be passed through the context using the 'default_journal_id' key containing its id,
    #     either be determined by the default type.
    #     '''
    #     move_type = self._context.get('default_move_type', 'entry')
    #     journal_types = []
    #     if move_type in self.get_sale_types(include_receipts=True):
    #         journal_types = ['sale']
    #     elif move_type in self.get_purchase_types(include_receipts=True):
    #         journal_types = ['purchase']
    #     # else:
    #     #     journal_types = self._context.get('default_move_journal_types', ['general'])
    #
    #     if self._context.get('default_journal_id'):
    #         journal = self.env['account.journal'].browse(self._context['default_journal_id'])
    #
    #         if move_type != 'entry' and journal.type not in journal_types:
    #             raise UserError(_(
    #                 "Cannot create an invoice of type %(move_type)s with a journal having %(journal_type)s as type.",
    #                 move_type=move_type,
    #                 journal_type=journal.type,
    #             ))
    #     else:
    #         if journal_types:
    #             journal = self._search_default_journal(journal_types)
    #         else:
    #             journal = False
    #     return journal
    #
    #
    #
    # @api.model
    # def _get_default_currency_updated(self):
    #     ''' Get the default currency from either the journal, either the default journal's company. '''
    #     journal = self._get_default_journal()
    #     if journal:
    #         return journal.currency_id or journal.company_id.currency_id

    reason = fields.Char("Reason for Cancel")
    is_reason = fields.Boolean()
    entry_type = fields.Selection([('entry', 'Journal Entry'),
                                   ('statement', 'Statement Entry')], default='entry', string="Entry Type")


    @api.onchange('partner_id','invoice_line_ids')
    def restriction_on_invoice_fields(self):
        if self.partner_id or self.invoice_line_ids:
            if not self.env.user.has_group('accounting_elegant.restriction_on_editing_invoice'):
                raise ValidationError(_("You Have Not Permission to Change This"))

    @api.onchange('entry_type')
    def account_type(self):
        for rec in self.line_ids:
            rec.entry_type = self.entry_type

    # journal_id = fields.Many2one('account.journal', string='Journal', required=True, readonly=True,
    #     states={'draft': [('readonly', False)]},
    #     check_company=True, domain="[('id', 'in', suitable_journal_ids)]",
    #     default=_get_default_journal)
    #
    # currency_id = fields.Many2one('res.currency', store=True, readonly=True, tracking=True, required=True,
    #                               states={'draft': [('readonly', False)]},
    #                               string='Currency',
    #                               default=_get_default_currency_updated)

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
        self.write({'auto_post': False, 'state': 'cancel', 'is_reason': True})


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    entry_type = fields.Selection([('entry', 'Journal Entry'),
                                   ('statement', 'Statement Entry')], string="Entry Type")
    analytic_mandatory = fields.Boolean()

    # account_id = fields.Many2one('account.account', string='Account',
    #                              index=True, ondelete="cascade",
    #                              domain="[('deprecated', '!=', False)]",
    #                              check_company=True,
    #                              tracking=True)

    @api.onchange('entry_type')
    def account_type(self):
        if self.entry_type == 'statement':
            return {
                'domain': {
                    'account_id': [('transfer_type', '=', 'statement'),('deprecated', '=', False),('force_auto', '=', False)]
                }
            }
        else:
            return {
                'domain': {
                    'account_id': [('transfer_type', '!=', 'statement'), ('deprecated', '=', False), ('force_auto', '=', False)]
                }
            }

    @api.onchange('partner_id')
    def get_partner_account(self):
        if self.partner_id and self.move_id.move_type == 'entry':
            if self.partner_id.supplier_rank > 0 and self.partner_id.property_account_payable_id:
                self.account_id = self.partner_id.property_account_payable_id.id

            elif self.partner_id.property_account_receivable_id:
                self.account_id = self.partner_id.property_account_receivable_id.id

            else:
                self.account_id = False

    @api.onchange('account_id')
    def get_analytic_account_id(self):
        for rec in self:
            if rec.account_id.mandatory_analytic_account:
                rec.analytic_mandatory = True
                if rec.account_id.analytic_accounts_ids:
                    rec.analytic_account_id = False
                    return {
                        'domain': {
                            'analytic_account_id': [('id', 'in',rec.account_id.analytic_accounts_ids.ids)]
                        }
                    }
                else:
                    rec.analytic_account_id = False

            else:
                rec.analytic_mandatory = False


# class Account(models.Model):
#     _inherit = 'account.journal'
#
#     next_link_synchronization = fields.Char()
#     account_online_account_id = fields.Char()
#     account_online_link_state = fields.Char()
#     bank_statement_creation_groupby = fields.Char()
