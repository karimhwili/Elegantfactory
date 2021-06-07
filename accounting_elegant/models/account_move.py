from odoo import fields, models, api
from odoo.addons.account.models.account_move import AccountMove as AccountMove1

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
                                      ('not_required', 'Not Required'),],default='not_required' ,string="Transfer Type")

class AccountMove(models.Model):
    _inherit = 'account.move'

    reason = fields.Char("Reason for Cancel")
    is_reason = fields.Boolean()

    # def button_create_landed_costs(self):
    #     """Create a `stock.landed.cost` record associated to the account move of `self`, each
    #     `stock.landed.costs` lines mirroring the current `account.move.line` of self.
    #     """
    #     self.ensure_one()
    #     landed_costs_lines = self.line_ids.filtered(lambda line: line.is_landed_costs_line)
    #
    #     landed_costs = self.env['stock.landed.cost'].create({
    #         'vendor_bill_id': self.id,
    #         'cost_lines': [(0, 0, {
    #             'product_id': l.product_id.id,
    #             'name': l.product_id.name,
    #             'account_journal_id': self.journal_id.id,
    #             'account_id': l.product_id.product_tmpl_id.get_product_accounts()['stock_input'].id,
    #             'price_unit': l.currency_id._convert(l.price_subtotal, l.company_currency_id, l.company_id, l.move_id.date),
    #             'split_method': 'equal',
    #         }) for l in landed_costs_lines],
    #     })
    #     action = self.env["ir.actions.actions"]._for_xml_id("stock_landed_costs.action_stock_landed_cost")
    #     return dict(action, view_mode='form', res_id=landed_costs.id, views=[(False, 'form')])

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
#
# class Account(models.Model):
#     _inherit = 'account.journal'
#
#     next_link_synchronization = fields.Char()
#     account_online_account_id = fields.Char()
#     account_online_link_state = fields.Char()
#     bank_statement_creation_groupby = fields.Char()