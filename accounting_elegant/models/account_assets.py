# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountAssetsInherit(models.Model):
    _inherit = 'account.asset'

    tracking = fields.One2many('assets.tracking','asset_id',"Tracking")
    original_value = fields.Float(compute="_get_original_value", store=True)
    salvage_value = fields.Float(compute="_get_original_value", store=True,readonly=False)
    asset_types = fields.Many2one('asset.type',"Asset Type")
    seq = fields.Char(string="Sequence",  required=True, copy=False, readonly=True,
                           index=True, default='New')

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


class TrackingAssets(models.Model):
    _name = 'assets.tracking'
    _description = 'Tracking Assets'

    asset_id = fields.Many2one('account.asset')
    employee_id = fields.Many2one('hr.employee',"Employee")
    reference = fields.Char("Reference")
    value = fields.Float("Value")
    depreciable_value = fields.Float("Not Depreciable Value")

class AssetsType(models.Model):
    _name = 'asset.type'
    _description = 'Assets Type'

    name = fields.Char("Type")

class InheritAccount(models.Model):
    _inherit = 'account.account'

    def unlink(self):
        if self.env['account.move.line'].search([('account_id', 'in', self.ids)], limit=1):
            raise UserError(_('You cannot perform this action on an account that contains journal items.'))
        #Checking whether the account is set as a property to any Partner or not
        values = ['account.account,%s' % (account_id,) for account_id in self.ids]
        partner_prop_acc = self.env['ir.property'].sudo().search([('value_reference', 'in', values)], limit=1)
        # if partner_prop_acc:
        #     account_name = partner_prop_acc.get_by_record().display_name
        #     raise UserError(
        #         _('You cannot remove/deactivate the account %s which is set on a customer or vendor.', account_name)
        #     )
        return super(InheritAccount, self).unlink()









