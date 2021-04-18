# -*- coding: utf-8 -*-

from odoo import fields, models
from dateutil.relativedelta import relativedelta
from datetime import date, datetime


class CreateWizard(models.TransientModel):
    _name = 'payroll.allowances'
    _description = 'Payroll allowances'

    date_from = fields.Date("Date From",default=lambda self: fields.Date.to_string(date.today().replace(day=1)),required=True)
    date_to = fields.Date("Date To",default=lambda self: fields.Date.to_string((datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()),required=True)

    def _get_report_pdf(self):
        exist_payslip = self.env['hr.payslip'].search([('date_from','<=',self.date_from),('date_to','>=',self.date_to)])
        date_month = datetime.strptime(
            self.date_from.strftime('%Y-%m-%d'), '%Y-%m-%d')
        payslip_ids = []
        for payslip in exist_payslip:
            payslip_ids.append({
                'employee_name': payslip.employee_id.name,
                'employee_category': payslip.employee_id.contract_id.employee_category,
                'employee_class': payslip.employee_id.contract_id.employee_class,
                'position_name': payslip.employee_id.job_id.name,
                'basic':payslip.line_ids.filtered(lambda line: line.code == 'TOBASIC').total,
                'ALW1':payslip.line_ids.filtered(lambda line: line.code == 'ALW1').total,
                'ALW2':payslip.line_ids.filtered(lambda line: line.code == 'ALW2').total,
                'ALW3':payslip.line_ids.filtered(lambda line: line.code == 'ALW3').total,
                'ALW4':payslip.line_ids.filtered(lambda line: line.code == 'ALW4').total,
                'ALW5':payslip.line_ids.filtered(lambda line: line.code == 'ALW5').total,
                'ALW6':payslip.line_ids.filtered(lambda line: line.code == 'ALW6').total,
                'ALW7':payslip.line_ids.filtered(lambda line: line.code == 'ALW7').total,
                'ALW8':payslip.line_ids.filtered(lambda line: line.code == 'ALW8').total,
                'ALW9':payslip.line_ids.filtered(lambda line: line.code == 'ALW9').total,
                'total_taxes': payslip.line_ids.filtered(lambda line: line.code == 'RTXDED').total,
                'net_salary': payslip.line_ids.filtered(lambda line: line.code == 'NETSALARY').total,

            })

        return {
            'payslip_ids': payslip_ids,
            'date_month':date_month.month,
            'date_year' : date_month.year
        }

    def generate_payroll_allowances(self):
        data = self._get_report_pdf()
        return self.env.ref('libya_hr_payroll.report_payroll_libya_allowances_pdf').report_action([],data=data)







