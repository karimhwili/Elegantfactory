# -*- coding:utf-8 -*-

from odoo import api, fields, models
from datetime import datetime, timedelta


class HrEmpolyee(models.Model):
    _inherit = 'hr.employee'

    overtime_hour_rate = fields.Float(
        'Over Time Hour Rate', digits='Product Unit of Measure')

    name = fields.Char(string='Name')
    supporting_family = fields.Boolean('Supporting Family')


class HrContract(models.Model):
    _inherit = 'hr.contract'


    payslip_id = fields.Many2one('hr.payslip')
    allowances = fields.Float(string="Overtime working hours",
                              digits='Payroll')

    other_alw_ids = fields.One2many(comodel_name="hr.alw.line",
                                    inverse_name="contract_id",
                                    string="Other Allowances")

    other_ded_ids = fields.One2many(comodel_name="hr.ded.line",
                                    inverse_name="contract_id",
                                    string="Other Deduction")

    payslip_date_from = fields.Date()
    payslip_date_to = fields.Date()
    hours_per_day = fields.Float()

    def get_alw(self, alw_code):
        alw_id = self.other_alw_ids.filtered(lambda x: x.code == alw_code)
        return alw_id

    def get_ded(self, ded_code):
        ded_id = self.other_ded_ids.filtered(lambda x: x.code == ded_code)
        return ded_id

    def get_payslip_date_from(self):
        Payslip = self.env['hr.payslip'].search([('employee_id','=',self.employee_id.id)],limit=1)
        print("",Payslip)
        for rec in Payslip:
            self.payslip_date_from = rec.date_from

        return

    def get_payslip_date_to(self):
        Payslip = self.env['hr.payslip'].search([('employee_id','=',self.employee_id.id)],limit=1)
        print("",Payslip)
        for rec in Payslip:
            self.payslip_date_to = rec.date_to
        return



    def compute_salary_basic(self):
        return self.wage

    def compute_salary_wdec(self):
        return self.wage - (0.01*self.wage + 0.0375*self.wage)

    def compute_tax_exemption(self):
        Employees = self.env['hr.employee'].search([('id','=',self.employee_id.id)])
        for employee in Employees:
            tax_exc = 0
            if employee.marital == 'single':
                tax_exc += 150
            elif employee.marital == 'married' and employee.supporting_family == False:
                tax_exc += 200
            elif employee.supporting_family:
                tax_exc += 200 + employee.children * 25

            return tax_exc

    def calculate_ly_tax(self):

        TAX_lEVELS = [[0, 1000, 5],
                      [1000, 100000000, 10],
                      ]


        salary = self.compute_salary_wdec() - self.compute_tax_exemption()

        tax_amounts = []
        total_tax = 0
        levels = []
        if salary > 0:
            levels = TAX_lEVELS

        for level in levels:
            if salary < level[0]:
                continue
            elif salary > level[1]:
                tax_amount = (level[1] - level[0]) * level[2] / 100
                tax_amounts.append(tax_amount)
                continue
            elif level[0] < salary <= level[1]:
                tax_amount = (salary - level[0]) * level[2] / 100
                tax_amounts.append(tax_amount)

        if tax_amounts:
            total_tax = sum(tax_amounts)
        return total_tax

    def compute_deduction_dinar(self):
        d_dinar = 0
        if self.compute_salary_basic() > 0:
            d_dinar += 1
        else:
            d_dinar += 0
        return d_dinar


class HrAlwsLine(models.Model):
    _name = "hr.alw.line"
    alw_id = fields.Many2one(comodel_name="hr.alw", string="name",
                             required=True)
    code = fields.Char(string="Code", required=True)
    amount = fields.Float(string="Amount", required=True)
    contract_id = fields.Many2one(comodel_name="hr.contract", string="Contract")

    @api.onchange('alw_id')
    def onchange_alw_id(self):
        self.code = self.alw_id.code
        self.amount = self.alw_id.amount

class HrAlows(models.Model):
    _name = "hr.alw"
    name = fields.Char(string="name", required=True, translate=True)
    code = fields.Char(string="Code", required=True)
    amount = fields.Float(string="Amount")

    @api.model
    def create(self, values):
        res = super(HrAlows, self).create(values)
        cat_id = self.env['hr.salary.rule.category'].search(
            [('code', '=', 'ALW')], limit=1)
        rule_obj = self.env['hr.salary.rule']
        condition_exp = 'result = contract.get_alw("%s") and contract.get_alw("%s").amount > 0 or False' % (
            values['code'], values['code'])
        amount_exp = 'result = contract.get_alw("%s").amount' % values['code']
        structure_id = self.env.ref('libya_hr_payroll.hr_salary_structure_ly')
        if not structure_id:
            structure_id = self.env['hr.payroll.structure'].search([],limit=1)

        vals = {
            'name': values['name'],
            'category_id': cat_id.id,
            'struct_id':structure_id.id,
            'code': values['code'],
            'condition_select': 'python',
            'condition_python': condition_exp,
            'amount_select': 'code',
            'amount_python_compute': amount_exp,
            'sequence': 35
        }
        rule_obj.create(vals)
        return res

    def unlink(self):
        for rule in self.env['hr.salary.rule'].search(
                [('code', '=', self.code)]):
            rule.unlink()
        return super(HrAlows, self).unlink()


class HrDeductLine(models.Model):
    _name = "hr.ded.line"
    ded_id = fields.Many2one(comodel_name="hr.ded", string="name",
                             required=True)
    code = fields.Char(string="Code", required=True)
    amount = fields.Float(string="Amount", required=True)
    contract_id = fields.Many2one(comodel_name="hr.contract", string="Contract")

    @api.onchange('ded_id')
    def onchange_ded_id(self):
        self.code = self.ded_id.code
        self.amount = self.ded_id.amount

class HrDeduction(models.Model):
    _name = "hr.ded"
    name = fields.Char(string="name", required=True, translate=True)
    code = fields.Char(string="Code", required=True)
    amount = fields.Float(string="Amount")

    @api.model
    def create(self, values):
        res = super(HrDeduction, self).create(values)
        cat_id = self.env['hr.salary.rule.category'].search(
            [('code', '=', 'ODED')], limit=1)
        rule_obj = self.env['hr.salary.rule']
        condition_exp = 'result = contract.get_ded("%s") and contract.get_ded("%s").amount > 0 or False' % (
            values['code'], values['code'])
        amount_exp = 'result = contract.get_ded("%s").amount' % values['code']
        structure_id = self.env.ref('libya_hr_payroll.hr_salary_structure_ly')
        if not structure_id:
            structure_id = self.env['hr.payroll.structure'].search([],limit=1)

        vals = {
            'name': values['name'],
            'category_id': cat_id.id,
            'struct_id':structure_id.id,
            'code': values['code'],
            'condition_select': 'python',
            'condition_python': condition_exp,
            'amount_select': 'code',
            'amount_python_compute': amount_exp,
            'sequence': 35
        }
        rule_obj.create(vals)
        return res

    def unlink(self):
        for rule in self.env['hr.salary.rule'].search(
                [('code', '=', self.code)]):
            rule.unlink()
        return super(HrDeduction, self).unlink()





