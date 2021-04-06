# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

from odoo import api, fields, models


class HrEmpolyee(models.Model):
    _inherit = 'hr.employee'

    overtime_hour_rate = fields.Float(
        'Over Time Hour Rate', digits='Product Unit of Measure')

    name = fields.Char(string='Name')
    tax_exemption = fields.Float(
        'Tax Exemption', digits='Product Unit of Measure', compute='_compute_tax_exemption')  # الاعفاء الضريبي

    # الحالة الاجتماعية   يسمى حد الاعفاء من الضرائب .(اعزب 150/متزوج200/متزوج ويعول على كل طفل25)
    supporting_family = fields.Boolean('Supporting Family')

    def _compute_tax_exemption(self):
        for employee in self:
            tax_exc = 0
            if employee.marital == 'single':
                tax_exc += 150
            if employee.marital == 'married':
                tax_exc += 200

            if employee.supporting_family:
                tax_exc += employee.children * 25

            employee.tax_exemption = tax_exc


class HrPayslip(models.Model):
    '''Employee Pay Slip'''
    
    _inherit = 'hr.payslip'
    _description = 'Pay Slips'

    advice_id = fields.Many2one(
        'hr.payroll.advice', string='Bank Advice', copy=False)

    def _compute_overtime(self):
        """compute the amount of the overtime done by the employee if there is.

        Returns:
            Float
        """
        self.ensure_one()
        overtime_hours = sum(self.env['hr.attendance'].sudo().search(
            [
                ('employee_id', '=', self.employee_id.id),
                ('check_in', '>=', self.date_from),
                ('check_in', '<=', self.date_to),

            ]).mapped('worked_hours'))
        return self.employee_id.overtime_hour_rate * overtime_hours

    # .المرتب الاساسي    = العقد +ساعات العمل الاضافي
    def _compute_salary_basic(self):
        self.ensure_one()
        return self.basic_wage + self._compute_overtime

    def get_details_by_rule_category(self):
        payslip_lines = self.line_ids
        PayslipLine = self.env['hr.payslip.line']
        RuleCateg = self.env['hr.salary.rule.category']

        def get_recursive_parent(current_rule_category, rule_categories=None):
            if rule_categories:
                rule_categories = current_rule_category | rule_categories
            else:
                rule_categories = current_rule_category

            if current_rule_category.parent_id:
                return get_recursive_parent(current_rule_category.parent_id, rule_categories)
            else:
                return rule_categories

        res = {}
        result = {}

        if payslip_lines:
            self.env.cr.execute("""
                SELECT pl.id, pl.category_id, pl.slip_id FROM hr_payslip_line as pl
                LEFT JOIN hr_salary_rule_category AS rc on (pl.category_id = rc.id)
                WHERE pl.id in %s
                GROUP BY rc.parent_id, pl.sequence, pl.id, pl.category_id
                ORDER BY pl.sequence, rc.parent_id""",
                                (tuple(payslip_lines.ids),))
            for record in self.env.cr.fetchall():
                result.setdefault(record[2], {})
                result[record[2]].setdefault(record[1], [])
                result[record[2]][record[1]].append(record[0])
            for payslip_id, lines_dict in result.items():
                res.setdefault(payslip_id, [])
                for rule_categ_id, line_ids in lines_dict.items():
                    rule_categories = RuleCateg.browse(rule_categ_id)
                    lines = PayslipLine.browse(line_ids)
                    level = 0
                    for parent in get_recursive_parent(rule_categories):
                        res[payslip_id].append({
                            'rule_category': parent.name,
                            'name': parent.name,
                            'code': parent.code,
                            'level': level,
                            'total': sum(lines.mapped('total')),
                        })
                        level += 1
                    for line in lines:
                        res[payslip_id].append({
                            'rule_category': line.name,
                            'name': line.name,
                            'code': line.code,
                            'total': line.total,
                            'level': level
                        })
        return res

    # .خصم الضمان    خصم 3.75% من قيمة المرتب الاساسي

    def social_security_deduction(self):
        self.ensure_one()
        return 0.375 * self._compute_salary_basic()

    # .خصم التضامن   خصم 1 % منقيمة المرتب الاساسي

    def tadamon_deduction(self):
        self.ensure_one()
        return 0.01 * self._compute_salary_basic()
