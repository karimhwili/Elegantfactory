from odoo import fields, models, api, _
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    partner_type = fields.Selection([
        ('customer', 'Customer'),
        ('supplier', 'Vendor'),('salaries', 'Salaries'),
        ('other_expenses', 'Other Expenses'),('withdrawals', 'Withdrawals'),
        ('other_payments', 'Other Payments'),('other_receipts', 'Other Receipts'),('loans', 'Loans'),
    ], default=False, tracking=True, required=True)

    transfer_type = fields.Selection([('cash_to_bank','Cash to Bank'),
                                      ('cash_to_cash','Cash to Cash'),
                                      ('bank_to_bank','Bank to Bank'),
                                      ],"Transfer Type",default='cash_to_bank')

    is_internal_transfer = fields.Boolean(string="Is Internal Transfer",
                                          readonly=False,
                                          compute=False)


    destination_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Destination Account',
        store=True, readonly=False,
        compute='_compute_destination_account_id',
        domain=False,
        check_company=True)

    currency_rate = fields.Float("Currency Rate",digits=(6, 2),compute='_get_currency_rate',store=True,readonly=False)

    @api.depends('currency_id.rate')
    def _get_currency_rate(self):
        for rec in self:
            rec.currency_rate = rec.currency_id.rate

    @api.onchange('partner_type','transfer_type','is_internal_transfer')
    def _get_destination_domain(self):
        if self.partner_type in ('customer','supplier'):
            if self.is_internal_transfer == True:
                if self.transfer_type == 'cash_to_bank':
                    return {
                        'domain': {
                            'destination_account_id': [('transfer_type', '=', 'cash_to_bank'),
                                                       ]
                        }
                    }
                elif self.transfer_type == 'cash_to_cash':
                    return {
                        'domain': {
                            'destination_account_id': [('transfer_type', '=', 'cash_to_cash'),
                                                       ]
                        }
                    }
                elif self.transfer_type == 'bank_to_bank':
                    return {
                        'domain': {
                            'destination_account_id': [('transfer_type', '=', 'bank_to_bank'),
                                                       ]
                        }
                    }
            else:

                return {
                    'domain': {
                        'destination_account_id': [('user_type_id.type', 'in', ('receivable', 'payable')),
                                                   ]
                    }
                }
        elif self.partner_type == 'salaries':
            return {
                'domain': {
                    'destination_account_id': [('transfer_type', '=', 'salaries')]
                }
            }
        elif self.partner_type == 'other_payments':
            return {
                'domain': {
                    'destination_account_id': [('transfer_type', '=', 'other_payments')]
                }
            }
        elif self.partner_type == 'other_expenses':
            return {
                'domain': {
                    'destination_account_id': [('user_type_id.internal_group', '=', 'expense')]
                }
            }
        elif self.partner_type == 'other_receipts':
            return {
                'domain': {
                    'destination_account_id': [('transfer_type', '=', 'other_receipts')]
                }
            }
        elif self.partner_type == 'withdrawals':
            return {
                'domain': {
                    'destination_account_id': [('user_type_id.internal_group', '=', 'asset')]
                }
            }
        elif self.partner_type == 'loans':
            return {
                'domain': {
                    'destination_account_id': [('transfer_type', '=', 'loans')]
                }
            }


    @api.depends('journal_id', 'partner_id', 'partner_type', 'is_internal_transfer','transfer_type')
    def _compute_destination_account_id(self):
        self.destination_account_id = False
        for pay in self:
            if pay.is_internal_transfer:
                if pay.transfer_type == 'cash_to_bank':
                    pay.destination_account_id = self.env['account.account'].search([
                        ('transfer_type', '=', 'cash_to_bank'),
                    ], limit=1)
                elif pay.transfer_type == 'cash_to_cash':
                    pay.destination_account_id = self.env['account.account'].search([
                        ('transfer_type', '=', 'cash_to_cash'),
                    ], limit=1)
                elif pay.transfer_type == 'bank_to_bank':
                    pay.destination_account_id = self.env['account.account'].search([
                        ('transfer_type', '=', 'bank_to_bank'),
                    ], limit=1)
            elif pay.partner_type == 'customer':

                # Receive money from invoice or send money to refund it.
                if pay.partner_id:
                    pay.destination_account_id = pay.partner_id.with_company(
                        pay.company_id).property_account_receivable_id
                else:
                    pay.destination_account_id = self.env['account.account'].search([
                        ('company_id', '=', pay.company_id.id),
                        ('internal_type', '=', 'receivable'),
                    ], limit=1)
            elif pay.partner_type == 'supplier':
                # Send money to pay a bill or receive money to refund it.
                if pay.partner_id:
                    pay.destination_account_id = pay.partner_id.with_company(pay.company_id).property_account_payable_id
                else:
                    pay.destination_account_id = self.env['account.account'].search([
                        ('company_id', '=', pay.company_id.id),
                        ('internal_type', '=', 'payable'),
                    ], limit=1)

            elif pay.partner_type == 'salaries':
                pay.destination_account_id = self.env['account.account'].search([
                    ('transfer_type', '=', 'salaries'),
                ], limit=1)

            elif pay.partner_type == 'other_payments':
                pay.destination_account_id = self.env['account.account'].search([
                    ('transfer_type', '=', 'other_payments'),
                ], limit=1)

            elif pay.partner_type == 'other_receipts':
                pay.destination_account_id = self.env['account.account'].search([
                    ('transfer_type', '=', 'other_receipts'),
                ], limit=1)

            elif pay.partner_type == 'loans':
                pay.destination_account_id = self.env['account.account'].search([
                    ('transfer_type', '=', 'loans'),
                ], limit=1)
    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        ''' Prepare the dictionary to create the default account.move.lines for the current payment.
        :param write_off_line_vals: Optional dictionary to create a write-off account.move.line easily containing:
            * amount:       The amount to be added to the counterpart amount.
            * name:         The label to set on the line.
            * account_id:   The account on which create the write-off.
        :return: A list of python dictionary to be passed to the account.move.line's 'create' method.
        '''
        self.ensure_one()
        write_off_line_vals = write_off_line_vals or {}

        if not self.journal_id.payment_debit_account_id or not self.journal_id.payment_credit_account_id:
            raise UserError(_(
                "You can't create a new payment without an outstanding payments/receipts account set on the %s journal.",
                self.journal_id.display_name))

        # Compute amounts.
        write_off_amount = write_off_line_vals.get('amount', 0.0)


        if self.payment_type == 'inbound':
            # Receive money.
            counterpart_amount = -self.amount
            write_off_amount *= -1
        elif self.payment_type == 'outbound':
            # Send money.
            counterpart_amount = self.amount
        else:
            counterpart_amount = 0.0
            write_off_amount = 0.0

        # balance = self.currency_id._convert(counterpart_amount, self.company_id.currency_id, self.company_id, self.date)
        balance = counterpart_amount / self.currency_rate
        counterpart_amount_currency = counterpart_amount
        write_off_balance = self.currency_id._convert(write_off_amount, self.company_id.currency_id, self.company_id, self.date)
        write_off_amount_currency = write_off_amount
        currency_id = self.currency_id.id

        if self.is_internal_transfer:
            if self.payment_type == 'inbound':
                liquidity_line_name = _('Transfer to %s', self.journal_id.name)
            else: # payment.payment_type == 'outbound':
                liquidity_line_name = _('Transfer from %s', self.journal_id.name)
        else:
            liquidity_line_name = self.payment_reference

        # Compute a default label to set on the journal items.

        payment_display_name = {
            'outbound-customer': _("Customer Reimbursement"),
            'inbound-customer': _("Customer Payment"),
            'outbound-supplier': _("Vendor Payment"),
            'inbound-supplier': _("Vendor Reimbursement"),
            'outbound-salaries': _("Salaries Payment"),
            'inbound-salaries': _("Salaries Reimbursement"),
            'outbound-other_expenses': _("Other Expenses Payment"),
            'inbound-other_expenses': _("Other Expenses Reimbursement"),
            'outbound-withdrawals': _("Withdrawals Payment"),
            'inbound-withdrawals': _("Withdrawals Reimbursement"),
            'outbound-other_payments': _("Other Payments Payment"),
            'inbound-other_payments': _("Other Payments Reimbursement"),
            'outbound-other_receipts': _("Other receipts Payment"),
            'inbound-other_receipts': _("Other receipts Reimbursement"),
            'outbound-loans': _("Loans Payment"),
            'inbound-loans': _("Loans Reimbursement"),
        }

        default_line_name = self.env['account.move.line']._get_default_line_name(
            _("Internal Transfer") if self.is_internal_transfer else payment_display_name['%s-%s' % (self.payment_type, self.partner_type)],
            self.amount,
            self.currency_id,
            self.date,
            partner=self.partner_id,
        )

        line_vals_list = [
            # Liquidity line.
            {
                'name': liquidity_line_name or default_line_name,
                'date_maturity': self.date,
                'amount_currency': -counterpart_amount_currency,
                'currency_id': currency_id,
                'debit': balance < 0.0 and -balance or 0.0,
                'credit': balance > 0.0 and balance or 0.0,
                'partner_id': self.partner_id.id,
                'account_id': self.journal_id.payment_debit_account_id.id if balance < 0.0 else self.journal_id.payment_credit_account_id.id,
            },
            # Receivable / Payable.
            {
                'name': self.payment_reference or default_line_name,
                'date_maturity': self.date,
                'amount_currency': counterpart_amount_currency + write_off_amount_currency if currency_id else 0.0,
                'currency_id': currency_id,
                'debit': balance + write_off_balance > 0.0 and balance + write_off_balance or 0.0,
                'credit': balance + write_off_balance < 0.0 and -balance - write_off_balance or 0.0,
                'partner_id': self.partner_id.id,
                'account_id': self.destination_account_id.id,
            },
        ]
        if write_off_balance:
            # Write-off line.
            line_vals_list.append({
                'name': write_off_line_vals.get('name') or default_line_name,
                'amount_currency': -write_off_amount_currency,
                'currency_id': currency_id,
                'debit': write_off_balance < 0.0 and -write_off_balance or 0.0,
                'credit': write_off_balance > 0.0 and write_off_balance or 0.0,
                'partner_id': self.partner_id.id,
                'account_id': write_off_line_vals.get('account_id'),
            })
        return line_vals_list


    def _synchronize_to_moves(self, changed_fields):
        ''' Update the account.move regarding the modified account.payment.
        :param changed_fields: A list containing all modified fields on account.payment.
        '''
        if self._context.get('skip_account_move_synchronization'):
            return

        if not any(field_name in changed_fields for field_name in (
            'date', 'amount', 'payment_type','currency_rate', 'partner_type', 'payment_reference', 'is_internal_transfer',
            'currency_id', 'partner_id', 'destination_account_id', 'partner_bank_id',
        )):
            return

        for pay in self.with_context(skip_account_move_synchronization=True):
            liquidity_lines, counterpart_lines, writeoff_lines = pay._seek_for_lines()

            # Make sure to preserve the write-off amount.
            # This allows to create a new payment with custom 'line_ids'.

            if writeoff_lines:
                writeoff_amount = sum(writeoff_lines.mapped('amount_currency'))
                counterpart_amount = counterpart_lines['amount_currency']
                if writeoff_amount > 0.0 and counterpart_amount > 0.0:
                    sign = 1
                else:
                    sign = -1
                write_off_line_vals = {
                    'name': writeoff_lines[0].name,
                    'amount': writeoff_amount * sign,
                    'currency_rate':writeoff_lines[0].currency_rate,
                    'account_id': writeoff_lines[0].account_id.id,
                }
            else:
                write_off_line_vals = {}

            line_vals_list = pay._prepare_move_line_default_vals(write_off_line_vals=write_off_line_vals)

            line_ids_commands = [
                (1, liquidity_lines.id, line_vals_list[0]),
                (1, counterpart_lines.id, line_vals_list[1]),
            ]

            for line in writeoff_lines:
                line_ids_commands.append((2, line.id))

            if writeoff_lines:
                line_ids_commands.append((0, 0, line_vals_list[2]))

            # Update the existing journal items.
            # If dealing with multiple write-off lines, they are dropped and a new one is generated.

            pay.move_id.write({
                'partner_id': pay.partner_id.id,
                'currency_id': pay.currency_id.id,
                'partner_bank_id': pay.partner_bank_id.id,
                'line_ids': line_ids_commands,

            })
