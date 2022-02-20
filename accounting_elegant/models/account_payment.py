from odoo import fields, models, api, _
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    available_partner_bank_ids = fields.Char()
    partner_type = fields.Selection([
        ('customer', 'Customer'),
        ('supplier', 'Vendor'),('salaries', 'Salaries'),
        ('other_expenses', 'Other Expenses'),('withdrawals', 'Withdrawals'),
        ('other_payments', 'Other Payments'),('other_receipts', 'Other Receipts'),('loans', 'Loans'),('liability_receipts', 'Liability Receipts'),
    ], default=False, tracking=True, required=True)
    transfer_type = fields.Selection([('cash_to_bank','Cash to Bank'),
                                      ('cash_to_cash','Cash to Cash'),
                                      ('bank_to_bank','Bank to Bank'),
                                      ],"Transfer Type",default='cash_to_bank' )

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

    currency_rate = fields.Float("Currency Rate",digits=(6, 3),compute='_get_currency_rate',store=True,readonly=False)
    amount_currency = fields.Monetary("Amount Currency",compute='get_amount_currency')
    default_currency = fields.Many2one('res.currency',default=lambda self: self.env.user.company_id.currency_id)

    @api.depends('move_id')
    def get_amount_currency(self):
        for rec in self:
            if rec.move_id:
                amount_currency = 0.0
                for line in rec.move_id.line_ids:
                    amount_currency += line.debit
                rec.amount_currency = amount_currency

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
        elif self.partner_type == 'liability_receipts':
            return {
                'domain': {
                    'destination_account_id': [('user_type_id.name', 'in', ('Current Liabilities','Non-current Liabilities'))]
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
            elif pay.partner_type == 'liability_receipts':
                pay.destination_account_id = self.env['account.account'].search([
                    ('user_type_id.name', 'in', ('Current Liabilities','Non-current Liabilities')),
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
            'outbound-liability_receipts': _("Liability Receipts Payment"),
            'inbound-liability_receipts': _("Liability Receipts Reimbursement"),
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

    def _seek_for_lines(self):
        ''' Helper used to dispatch the journal items between:
        - The lines using the temporary liquidity account.
        - The lines using the counterpart account.
        - The lines being the write-off lines.
        :return: (liquidity_lines, counterpart_lines, writeoff_lines)
        '''
        self.ensure_one()

        liquidity_lines = self.env['account.move.line']
        counterpart_lines = self.env['account.move.line']
        writeoff_lines = self.env['account.move.line']

        for line in self.move_id.line_ids:
            if line.account_id in (
                    self.journal_id.default_account_id,
                    self.journal_id.payment_debit_account_id,
                    self.journal_id.payment_credit_account_id,
            ):
                liquidity_lines += line
            elif line.account_id.internal_type in ('receivable', 'payable','liquidity','other') or line.partner_id == line.company_id.partner_id:
                counterpart_lines += line
            else:
                writeoff_lines += line

        return liquidity_lines, counterpart_lines, writeoff_lines


    def _synchronize_from_moves(self, changed_fields):
        ''' Update the account.payment regarding its related account.move.
        Also, check both models are still consistent.
        :param changed_fields: A set containing all modified fields on account.move.
        '''
        if self._context.get('skip_account_move_synchronization'):
            return

        for pay in self.with_context(skip_account_move_synchronization=True):

            # After the migration to 14.0, the journal entry could be shared between the account.payment and the
            # account.bank.statement.line. In that case, the synchronization will only be made with the statement line.
            if pay.move_id.statement_line_id:
                continue

            move = pay.move_id
            move_vals_to_write = {}
            payment_vals_to_write = {}

            if 'journal_id' in changed_fields:
                if pay.journal_id.type not in ('bank', 'cash'):
                    raise UserError(_("A payment must always belongs to a bank or cash journal."))

            if 'line_ids' in changed_fields:
                all_lines = move.line_ids
                liquidity_lines, counterpart_lines, writeoff_lines = pay._seek_for_lines()

                if len(liquidity_lines) != 1 or len(counterpart_lines) != 1:
                    raise UserError(_(
                        "The journal entry %s reached an invalid state relative to its payment.\n"
                        "To be consistent, the journal entry must always contains:\n"
                        "- one journal item involving the outstanding payment/receipts account.\n"
                        "- one journal item involving a receivable/payable account.\n"
                        "- optional journal items, all sharing the same account.\n\n"
                    ) % move.display_name)

                if writeoff_lines and len(writeoff_lines.account_id) != 1:
                    raise UserError(_(
                        "The journal entry %s reached an invalid state relative to its payment.\n"
                        "To be consistent, all the write-off journal items must share the same account."
                    ) % move.display_name)

                if any(line.currency_id != all_lines[0].currency_id for line in all_lines):
                    raise UserError(_(
                        "The journal entry %s reached an invalid state relative to its payment.\n"
                        "To be consistent, the journal items must share the same currency."
                    ) % move.display_name)

                if any(line.partner_id != all_lines[0].partner_id for line in all_lines):
                    raise UserError(_(
                        "The journal entry %s reached an invalid state relative to its payment.\n"
                        "To be consistent, the journal items must share the same partner."
                    ) % move.display_name)

                if counterpart_lines.account_id.user_type_id.type == 'receivable':
                    partner_type = 'customer'
                else:
                    partner_type = 'supplier'

                liquidity_amount = liquidity_lines.amount_currency

                move_vals_to_write.update({
                    'currency_id': liquidity_lines.currency_id.id,
                    'partner_id': liquidity_lines.partner_id.id,
                })
                payment_vals_to_write.update({
                    'amount': abs(liquidity_amount),
                    'payment_type': 'inbound' if liquidity_amount > 0.0 else 'outbound',
                    # 'partner_type': partner_type,
                    'currency_id': liquidity_lines.currency_id.id,
                    'destination_account_id': counterpart_lines.account_id.id,
                    'partner_id': liquidity_lines.partner_id.id,
                })

            move.write(move._cleanup_write_orm_values(move, move_vals_to_write))
            pay.write(move._cleanup_write_orm_values(pay, payment_vals_to_write))

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
                    # 'currency_rate':writeoff_lines[0].currency_rate,
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


    @api.depends('partner_bank_id', 'amount', 'ref', 'currency_id', 'journal_id', 'move_id.state',
                 'payment_method_id', 'payment_type')
    def _compute_qr_code(self):
        for pay in self:
            if pay.state in ('draft', 'posted') \
                    and pay.partner_bank_id \
                    and pay.payment_method_id.code == 'manual' \
                    and pay.payment_type == 'outbound' \
                    and pay.currency_id:


                if pay.partner_bank_id:
                    qr_code = pay.partner_bank_id.build_qr_code_url(pay.amount, pay.ref, pay.ref, pay.currency_id,
                                                                    pay.partner_id)
                else:
                    qr_code = None

                if qr_code:
                    pay.qr_code = '''
                           <br/>
                           <img class="border border-dark rounded" src="{qr_code}"/>
                           <br/>
                           <strong class="text-center">{txt}</strong>
                           '''.format(txt=_('Scan me with your banking app.'),
                                      qr_code=qr_code)
                    continue

            pay.qr_code = None