# -*- coding: utf-8 -*-

from odoo import fields, models
from dateutil.relativedelta import relativedelta
from datetime import date, datetime


class CreateWizard(models.TransientModel):
    _name = 'payroll.position'
    _description = 'Payroll Position'

    date_from = fields.Date("Date From",default=lambda self: fields.Date.to_string(date.today().replace(day=1)),required=True)
    date_to = fields.Date("Date To",default=lambda self: fields.Date.to_string((datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()),required=True)

    def _get_report_pdf(self):
        exist_position = self.env['hr.job']
        date_month = datetime.strptime(
            self.date_from.strftime('%Y-%m-%d'), '%Y-%m-%d')
        payslip_ids = []
        for position in exist_position.search([]):
            total_wage = 0
            exist_employee = self.env['hr.employee'].search([('job_id','=',position.id)])
            for employee in exist_employee:
                total_wage+= employee.contract_id.wage
            payslip_ids.append({
                'position_name': position.name,
                'basic': total_wage,
                'total': len(exist_employee),
                'average': total_wage / len(exist_employee) if exist_employee else 0

            })
        return {
            'payslip_ids': payslip_ids,
            'date_month': date_month.month,
            'date_year': date_month.year
        }

    def generate_payroll_position(self):
        data = self._get_report_pdf()
        return self.env.ref('libya_hr_payroll.report_payroll_libya_position_pdf').report_action([],data=data)







