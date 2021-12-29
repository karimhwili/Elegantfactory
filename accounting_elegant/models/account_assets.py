# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError




class AccountAssetsInherit(models.Model):
    _inherit = 'account.asset'

    tracking = fields.One2many('assets.tracking','asset_id',"Tracking" )

    salvage_value = fields.Float(compute="_get_original_value", store=True,readonly=False)
    asset_types = fields.Many2one('asset.type',"Asset Type")
    seq = fields.Char(string="Sequence",  required=True, copy=False, readonly=True,
                           index=True, default='New')
    asset_quantity = fields.Integer("Asset Quantity")


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



    @api.depends('tracking.depreciable_value')
    def _get_original_value(self):
        d_value = 0
        for rec in self.tracking:
            d_value += rec.depreciable_value
        self.salvage_value = d_value

    @api.depends('original_move_line_ids', 'original_move_line_ids.account_id', 'asset_type','tracking.value')
    def _compute_value(self):
        o_value = 0
        for record in self:
            misc_journal_id = self.env['account.journal'].search(
                [('type', '=', 'general'), ('company_id', '=', record.company_id.id)], limit=1)
            if not record.original_move_line_ids:
                record.account_asset_id = record.account_asset_id or False
                if not record.account_asset_id and (
                        record.state == 'model' or not record.account_asset_id or record.asset_type != 'purchase'):
                    record.account_asset_id = record.account_depreciation_id if record.asset_type in (
                    'purchase', 'expense') else record.account_depreciation_expense_id
                record.original_value = record.original_value or False
                record.display_model_choice = record.state == 'draft' and self.env['account.asset'].search(
                    [('state', '=', 'model'), ('asset_type', '=', record.asset_type)])
                record.display_account_asset_id = True
                continue
            if any(line.move_id.state == 'draft' for line in record.original_move_line_ids):
                raise UserError(_("All the lines should be posted"))
            if any(account != record.original_move_line_ids[0].account_id for account in
                   record.original_move_line_ids.mapped('account_id')):
                raise UserError(_("All the lines should be from the same account"))
            record.account_asset_id = record.original_move_line_ids[0].account_id
            record.display_model_choice = record.state == 'draft' and self.env['account.asset'].search_count(
                [('state', '=', 'model'), ('account_asset_id.user_type_id', '=', record.user_type_id.id)])
            record.display_account_asset_id = False
            if not record.journal_id:
                record.journal_id = misc_journal_id
            total_credit = sum(line.credit for line in record.original_move_line_ids)
            total_debit = sum(line.debit for line in record.original_move_line_ids)
            for rec in record.tracking:
                if rec:
                    o_value += rec.value
                else:
                    o_value = 0
            record.original_value = total_credit + total_debit + o_value
            if (total_credit and total_debit) or record.original_value == 0:
                raise UserError(
                    _("You cannot create an asset from lines containing credit and debit on the account or with a null amount"))


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









