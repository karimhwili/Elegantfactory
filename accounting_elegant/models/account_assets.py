# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import numpy as np



class AccountAssetsInherit(models.Model):
    _inherit = 'account.asset'

    tracking = fields.One2many('assets.tracking','asset_id',"Tracking" )
    original_value = fields.Float(compute="_get_original_value", store=True)
    salvage_value = fields.Float(compute="_get_original_value", store=True,readonly=False)
    asset_types = fields.Many2one('asset.type',"Asset Type")
    seq = fields.Char(string="Sequence",  required=True, copy=False, readonly=True,
                           index=True, default='New')


    # def _get_account_move_line(self):
    #     for rec in self:
    #         move_lines_ids = self.env['account.move.line'].search([('credit','=',0),('move_id.state','=','posted')])
    #         current_move_lines_ids = self.search([]).mapped('original_move_line_ids')
    #
    #         filtered_moves = move_lines_ids - current_move_lines_ids
    #
    #         return [('id', 'in', filtered_moves.ids)]
    #
    #
    #
    # original_move_line_ids = fields.Many2many('account.move.line', 'asset_move_line_rel', 'asset_id', 'line_id',
    #                                           string='Journal Items', readonly=True,
    #                                           states={'draft': [('readonly', False)]}, copy=False,domain=_get_account_move_line)
    @api.model
    def create(self, vals):
        if vals.get('seq', _('New')) == _('New'):
            vals['seq'] = self.env['ir.sequence'].next_by_code(
                'account.asset.seq') or _('New')

        result = super(AccountAssetsInherit, self).create(vals)
        return result



    @api.depends('tracking.value', 'tracking.depreciable_value')
    def _get_original_value(self):
        o_value = 0
        d_value = 0
        for rec in self.tracking:
            o_value += rec.value
            d_value += rec.depreciable_value
        self.original_value = o_value
        self.salvage_value = d_value



class AssetsTrackingLocation(models.Model):
    _name = 'assets.tracking.location'
    _description = 'New Description'
    name = fields.Char(string='Name')


class TrackingAssets(models.Model):
    _name = 'assets.tracking'
    _description = 'Tracking Assets'

    asset_id = fields.Many2one('account.asset')
    employee_id = fields.Many2one('hr.employee',"Employee")
    reference = fields.Char("Reference", required=True)
    value = fields.Float("Value")
    depreciable_value = fields.Float("Not Depreciable Value")
    location_id = fields.Many2one('assets.tracking.location', string='Location')
    
    @api.constrains("employee_id", "location_id")
    def _check_field(self):
        for s in self:
            if not (s.location_id or s.employee_id):
                raise UserError(_("Please select either an employee or a location in the tracking!"))

class AssetsType(models.Model):
    _name = 'asset.type'
    _description = 'Assets Type'

    name = fields.Char("Type")









