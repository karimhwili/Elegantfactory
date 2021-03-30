# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountAssetsInherit(models.Model):
    _inherit = 'account.asset'

    tracking = fields.One2many('assets.tracking','asset_id',"Tracking")
    original_value = fields.Float(compute="_get_original_value", store=True)
    salvage_value = fields.Float(compute="_get_original_value", store=True,readonly=False)


    @api.depends('tracking.value', 'tracking.depreciable_value')
    def _get_original_value(self):
        o_value = 0
        d_value = 0
        for rec in self.tracking:
            o_value += rec.value
            d_value += rec.depreciable_value
        self.original_value = o_value
        self.salvage_value = d_value


class TrackingAssets(models.Model):
    _name = 'assets.tracking'
    _description = 'Tracking Assets'

    asset_id = fields.Many2one('account.asset')
    employee_id = fields.Many2one('hr.employee',"Employee")
    reference = fields.Char("Reference")
    value = fields.Float("Value")
    depreciable_value = fields.Float("Depreciable Value")








