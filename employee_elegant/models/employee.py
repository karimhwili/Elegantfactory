# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


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

    @api.model
    def create(self, vals):
        if vals.get('seq', _('New')) == _('New'):
            vals['seq'] = self.env['ir.sequence'].next_by_code(
                'hr.employee.seq') or _('New')

        result = super(HrEmployeesInherit, self).create(vals)
        return result


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
    old_depart = fields.Char("Old depart")
    new_depart = fields.Char("New depart")
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










