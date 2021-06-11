# -*- coding: utf-8 -*-
import time
import babel
from odoo import models, fields, api, tools, _
from datetime import datetime


class HrPayslip(models.Model):
    _inherit = 'hr.contract'

    def get_loan(self, date_from, date_to, employee_id):

        lon_obj = self.env['hr.loan'].search([('employee_id', '=', employee_id), ('state', '=', 'approve')])
        loan_amount = 0.0
        for loan in lon_obj:
            for loan_line in loan.loan_lines:
                if date_from <= loan_line.date <= date_to and not loan_line.paid:
                    loan_amount += loan_line.amount

        return loan_amount


class Hrpayslip(models.Model):
    _inherit = 'hr.payslip'

    def action_payslip_done(self):
        for line in self.line_ids:
            if line.code == 'LO':
                emp_id = self.employee_id
                date_from = self.date_from
                date_to = self.date_to
                lon_obj = self.env['hr.loan'].search([('employee_id', '=', emp_id.id), ('state', '=', 'approve')])
                for loan in lon_obj:
                    for loan_line in loan.loan_lines:
                        if date_from <= loan_line.date <= date_to and not loan_line.paid and line.amount == loan_line.amount:
                            loan_line.paid = True
        return super(Hrpayslip, self).action_payslip_done()
