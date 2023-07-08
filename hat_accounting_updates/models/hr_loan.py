from odoo import api, fields, models, _


class HrLoan(models.Model):
    _inherit = 'hr.loan'

    def action_inverse_journal_entry(self):
        for loan in self:
            journal_entry = self.env['account.move']
            if loan.balance_amount > 0:
                line_ids = [
                    (0, 0, {
                        'name': '',
                        'debit': loan.balance_amount,
                        'credit': 0.0,
                        'account_id': loan.treasury_account_id.id,
                        'currency_id': loan.currency_id.id,
                        'partner_id': loan.employee_id.address_id.id,
                    })]

                line_ids += [
                    (0, 0, {
                        'name': '',
                        'debit': 0.0,
                        'credit': loan.balance_amount,
                        'account_id': self.employee_account_id.id,
                        'currency_id': loan.currency_id.id,
                        'partner_id': loan.employee_id.address_id.id,
                    })]
                journal_entry.create({
                    'move_type': 'entry',
                    'ref': loan.name,
                    'currency_id': loan.currency_id.id,
                    'journal_id': loan.journal_id.id,
                    'loan_id': loan.id,
                    'line_ids': line_ids,
                })
                loan.advance_payment = True

    def journal_task_view_button(self):
        for loan in self:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Journals'),
                'res_model': 'account.move',
                'target': 'current',
                'view_mode': 'tree,form',
                'domain': [('loan_id', '=', loan.id), ('move_type', '=', 'entry')],
            }

    journal_count = fields.Integer(
        string='Project',
        required=False, compute="get_journals_count")
    advance_payment = fields.Boolean(
        string='Advance Payment',
        required=False)
    balance_check = fields.Boolean(
        string='Balance',
        required=False, compute="check_balance")

    def check_balance(self):
        if self.balance_amount > 0:
            self.balance_check = True
        else:
            self.balance_check = False

    def get_journals_count(self):
        for loan in self:
            journal_ids = self.env['account.move'].search([('loan_id', '=', loan.id), ('move_type', '=', 'entry')])
            loan.journal_count = len(journal_ids.ids)

    def _compute_loan_amount(self):
        total_paid = 0.0
        for loan in self:
            for line in loan.loan_lines:
                if line.paid:
                    total_paid += line.amount
            balance_amount = loan.loan_amount - total_paid
            self.total_amount = loan.loan_amount
            if loan.advance_payment:
                self.total_paid_amount += balance_amount
                self.balance_amount = 0
            else:
                self.balance_amount = balance_amount
                self.total_paid_amount = total_paid

    @api.depends('employee_id', 'balance_amount')
    def _compute_total_balance(self):
        for loan in self:
            all_loans = self.search([('employee_id', '=', loan.employee_id.id), ('state', '=', 'approve')])
            total_balance = 0.0
            for rec in all_loans:
                total_amount = rec.loan_amount
                total_paid = 0.0
                for line in rec.loan_lines:
                    if line.paid:
                        total_paid += line.amount
                total_balance += total_amount - total_paid
            loan.total_balance = loan.balance_amount
