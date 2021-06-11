# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    add_analytic_acc_tag = fields.Boolean(string="Analytic Account & Tags")
    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account")
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string="Analytic Tags")

    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        res = super(AccountPayment, self)._prepare_move_line_default_vals(write_off_line_vals)
        tags = [tag.id for tag in self.analytic_tag_ids]
        if self.add_analytic_acc_tag:
            for move_line in res:
                move_line.update({'analytic_account_id':self.analytic_account_id.id,'analytic_tag_ids':[(6,0,tags)]})
        return res

    def action_post(self):
        res = super(AccountPayment, self).action_post()
        account_move = self.env['account.move'].browse(self._context.get('active_id'))
        tags = [tag.id for tag in self.analytic_tag_ids]
        if self.add_analytic_acc_tag:
            for invoice_line in account_move.invoice_line_ids:
                invoice_line.update({'analytic_account_id':self.analytic_account_id.id, 'analytic_tag_ids':[(6,0,tags)]})
        return res    
