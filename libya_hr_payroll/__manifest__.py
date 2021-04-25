# -*- coding: utf-8 -*-

{
    'name': 'Libya Payroll',
    'category': 'Human Resources/Payroll',
    'depends': ['hr','hr_payroll', 'hr_attendance','employee_elegant'],

    'data': [
        'reports/report.xml',
        'security/ir.model.access.csv',
        'data/structure_types.xml',
        'views/hr_employee.xml',
        'views/hr_contract_view.xml',
        'wizards/payroll_insurance.xml',
        'wizards/payroll_deduction.xml',
        'views/payroll_insurance_report.xml',
        'views/payroll_deduction_report.xml',
        'wizards/payroll_position.xml',
        'views/payroll_position_report.xml',
        'wizards/payroll_allowances.xml',
        'views/payrol_allowances_report.xml',
        'views/bank_branch.xml',
        'views/payroll_expenses_report.xml',


    ],
}
