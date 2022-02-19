from odoo import fields, models, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sequence = fields.Char(index=True, default='New',string="ID")

    @api.model
    def create(self, vals):
        search_partner_mode = self.env.context.get('res_partner_search_mode')
        if search_partner_mode == 'customer':
            if vals.get('sequence', _('New')) == _('New'):
                vals['sequence'] = "11" + self.env['ir.sequence'].next_by_code(
                    'res.customer.seq') or _('New')
        elif search_partner_mode == 'supplier':
            if vals.get('sequence', _('New')) == _('New'):
                vals['sequence'] = "10" + self.env['ir.sequence'].next_by_code(
                    'res.vendor.seq') or _('New')

        res = super(ResPartner, self).create(vals)

        return res
