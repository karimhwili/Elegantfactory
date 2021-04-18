# -*- coding: utf-8 -*-
from dateutil import relativedelta
from datetime import date, datetime

from odoo import models, fields, api, _
from odoo.tools import float_round


class HrEmployeesInherit(models.Model):
    _inherit = 'hr.employee'

    tracking = fields.One2many('employee.assets','employee_id',"Tracking")
    followup_upgrade = fields.One2many('employee.upgrade','employee_id',"FollowUp")
    followup_transfer = fields.One2many('employee.transfer','employee_id',"FollowUp")
    followup_evaluation = fields.One2many('employee.evaluation','employee_id',"FollowUp")
    followup_warning = fields.One2many('employee.warning','employee_id',"FollowUp")

    certificate_id = fields.Char("Health Certificate ID")
    certificate_date_issue = fields.Date("Health certificate date of issues")
    certificate_date_ex = fields.Date("Health certificate date of expired")
    certificate_pdf = fields.Many2many('ir.attachment', string="Upload health certificate pdf")

    mother_name = fields.Char("Mother Name")
    social_security = fields.Char("Social security number")
    foreign_date = fields.Date("Date of leave country for foreign")
    city_birth = fields.Char("City of birth")
    current_city = fields.Char("Current city")
    current_address = fields.Text("Current address")
    home_localization = fields.Text("Home Localization of live")
    first_cont_date = fields.Date("Date of first contract")
    direct_date = fields.Date("Date of Direct")

    seq = fields.Char(string="Sequence", required=True, copy=False, readonly=True,
                      index=True, default='New')

    legal_leave_monthly_allocation = fields.Float(string="Legal Leave Monthly Allocation",
                                                  compute='_compute_legal_leave_monthly_allocation', stored=True)

    leave_name = fields.Many2one('hr.leave.type', string="Leave Name")
    check_contract = fields.Boolean(compute='_get_check_contract',store=True)


    @api.depends('contract_id.state')
    def _get_check_contract(self):
        for rec in self:
            if rec.contract_id.state in ('close','cancel'):
                rec.check_contract = True
            else:
                rec.check_contract = False

    @api.depends('first_contract_date', 'birthday')
    def _compute_legal_leave_monthly_allocation(self):
        for rec in self:
            today = date.today()
            y = relativedelta.relativedelta(today, rec.birthday)
            e = relativedelta.relativedelta(today, rec.first_contract_date)
            total_age = y.years
            experience_years = e.years
            if total_age > 50 or experience_years >= 20:
                rec.legal_leave_monthly_allocation = 3.75
            else:
                rec.legal_leave_monthly_allocation = 2.5

    @api.model
    def create(self, vals):
        if vals.get('seq', _('New')) == _('New'):
            vals['seq'] = self.env['ir.sequence'].next_by_code(
                'hr.employee.seq') or _('New')

        result = super(HrEmployeesInherit, self).create(vals)
        return result

class BaisEmployee(models.AbstractModel):
    _inherit = 'hr.employee.base'

    basic_balance = fields.Float(string="Total TimeOff", readonly=True)
    consumed_balance = fields.Float(string="Consumed Balance", readonly=True)
    remaining_balance = fields.Float(string="Remaining Balance", readonly=True)


    def _compute_allocation_count(self):
        data = self.env['hr.leave.allocation'].read_group([
            ('employee_id', 'in', self.ids),
            ('holiday_status_id.active', '=', True),
            ('state', '=', 'validate'),
        ], ['number_of_days:sum', 'employee_id'], ['employee_id'])
        rg_results = dict((d['employee_id'][0], d['number_of_days']) for d in data)
        for employee in self:
            employee.allocation_count = float_round(rg_results.get(employee.id, 0.0), precision_digits=2)
            employee.allocation_display = "%g" % employee.allocation_count
            employee.basic_balance = "%g" % employee.allocation_count

    def _compute_total_allocation_used(self):
        for employee in self:
            employee.allocation_used_count = float_round(employee.allocation_count - employee.remaining_leaves, precision_digits=2)
            employee.allocation_used_display = "%g" % employee.allocation_used_count
            employee.consumed_balance = "%g" % employee.allocation_used_count
            employee.remaining_balance = employee.basic_balance - employee.consumed_balance



class TrackingAssets(models.Model):
    _name = 'employee.assets'
    _description = 'Tracking Assets'

    employee_id = fields.Many2one('hr.employee')
    asset_id = fields.Many2one('account.asset',"Fixed Asset")
    date = fields.Date("Date of Obtained")
    reference = fields.Char("Reference")
    asset_type = fields.Many2one('asset.type',"Asset Type")
    value = fields.Float("Price estimation")

class FollowUpUpgrade(models.Model):
    _name = 'employee.upgrade'
    _description = 'Followup Upgrade'

    employee_id = fields.Many2one('hr.employee')

    upgrade_fun_name = fields.Char("Upgrade Functional Name")
    upgrade_fun_date = fields.Date("Upgrade Functional Date")
    responsible_upgrade = fields.Char("Responsible for Upgrade functional")

class FollowUpTransfer(models.Model):
    _name = 'employee.transfer'
    _description = 'Followup Transfer'

    employee_id = fields.Many2one('hr.employee')

    job_transfer_date = fields.Date("Job transfer date")
    old_depart = fields.Many2one('hr.department',"Old depart")
    new_depart = fields.Many2one('hr.department',"New depart")
    responsible_transfer = fields.Char("Responsible of transfer")

class FollowUpEvaluation(models.Model):
    _name = 'employee.evaluation'
    _description = 'Followup Evaluation'

    employee_id = fields.Many2one('hr.employee')

    evaluation_date = fields.Date("Date of evaluation")
    evaluation_result = fields.Char("Result of evaluation")
    responsible_evaluation = fields.Char("Responsible of evaluation")

class FollowUpWarning(models.Model):
    _name = 'employee.warning'
    _description = 'Followup Warning'

    employee_id = fields.Many2one('hr.employee')

    warning_date = fields.Date("Warning employee date")
    warning_reason = fields.Char("Warning Reason")
    responsible_warning = fields.Char("Responsible of warning")


class HrTownship(models.Model):
    _name = 'hr.partner.township'

    name = fields.Char('municipality')

class EmployeeState(models.Model):
    _inherit = 'res.partner'

    municipality = fields.Many2one('hr.partner.township',"municipality")













