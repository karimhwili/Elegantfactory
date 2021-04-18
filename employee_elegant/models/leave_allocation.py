from odoo import fields, models, api, _
import datetime
import calendar



class CustomLeave(models.Model):
    _inherit = 'hr.leave.type'
    _description = 'Custom Leaves'

    custom_leave = fields.Boolean(string="Special Leave", default=False)

class HrAllocation(models.Model):
    _inherit = 'hr.leave.allocation'

    @api.model
    def create_employee_allocation(self):
        Employees = self.env['hr.employee'].search([])
        Timeeofftyp = self.env['hr.leave.type'].search(
            [('custom_leave', '=', True)], limit=1)
        today = datetime.datetime.today()
        # get last day in the month
        last_day = calendar.monthrange(today.year, today.month)[1]
        t_today = today.day
        for employee in Employees:
            if employee.contract_id.state == 'open':
                if t_today == last_day:
                    allocation_vals = {
                        'name': _('Monthly Leave for ') + employee.name,
                        'holiday_status_id': Timeeofftyp.id,
                        'allocation_type': 'regular',
                        'holiday_type': 'employee',
                        'number_of_days': employee.legal_leave_monthly_allocation,
                        'employee_id': employee.id,
                    }
                    self.env['hr.leave.allocation'].create(allocation_vals)
    
