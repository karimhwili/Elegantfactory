# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    validate_debit_credit = fields.Boolean(copy=False, compute='check_validate_debit_credit')
    agent = fields.Many2one('res.partner', related='partner_id.agent', store=True)

    def check_validate_debit_credit(self):
        for rec in self:
            if not self.env.user.has_group('elegant_enhancement.can_validate_debi_credit_note') and rec.move_type in [
                'in_refund', 'out_refund']:
                rec.validate_debit_credit = False
            else:
                rec.validate_debit_credit = True

    validate_inv_bill = fields.Boolean(copy=False, compute='check_validate_invoices_bills')

    def check_validate_invoices_bills(self):
        for rec in self:
            if not self.env.user.has_group('elegant_enhancement.can_validate_invoices_bills') and rec.move_type in [
                'in_invoice', 'out_invoice']:
                rec.validate_inv_bill = False
            else:
                rec.validate_inv_bill = True

    @api.onchange('move_type')
    def onchange_move_type(self):
        b = {}
        if self.move_type == 'entry':
            self.journal_id = False
            b = {'domain': {'journal_id': [('allowed_for_manual', '=', True)]}}
        return b
