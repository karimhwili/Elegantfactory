# -*- coding: utf-8 -*-

{
    'name': 'Libya Payroll',
    'category': 'Human Resources/Payroll',
    'depends': ['hr_payroll', 'hr_attendance'],

    'data': [
        'security/ir.model.access.csv',
        'data/structure_types.xml',
        'views/hr_employee.xml',
        'views/hr_contract_view.xml'
    ],
}
