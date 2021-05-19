# -*- coding: utf-8 -*-
{
    'name': "ZKTeco",
    'summary': """Integration with ZKTeco Biometric Devices""",
    'description': "",
    'license':  "Other proprietary",
    'author': 'Mohamed essam',
    'maintainer': 'Muhamed essam',
    'website': 'https://www.linkedin.com/in/mohamed-essam-in/',
    'category': 'Human Resources',
    'version': '14',
    'depends': ['base', 'hr', 'hr_payroll', 'hr_contract', 'hr_attendance', 'mail', 'resource'],
    'data': [
        'data/get_attendance.xml',
        'security/biometricdevice_security.xml',
        'security/ir.model.access.csv',
        'views/company_view.xml',
        'views/hr_attendance_view.xml',
        'views/biometricdevice_view.xml',
        'views/hr_extensionview.xml',
        'wizard/move_attendance_wizard_view.xml',
        'wizard/generate_missing_attendance.xml',
       
    ],


    'installable': True,
    'auto_install': False,
    'application':False,    
}
