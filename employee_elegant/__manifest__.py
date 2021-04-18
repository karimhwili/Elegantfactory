# -*- coding: utf-8 -*-
{
    'name': "Employee Elegant",

    'author': "M.Shorbagy (Sahara)",

    'depends': ['base','hr','account_asset','hr_contract','hr_holidays','hr_payroll'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/allocation_schdule_data.xml',
        'data/sequence.xml',
        'views/employee.xml',
        'views/hr_township.xml',
        'views/leave_type.xml',
        'views/payslip_report.xml'

    ],

}
