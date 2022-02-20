# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    analytic_config_ids = fields.Many2many(
        comodel_name='account.analytic.account',
        string='Allowed Analytic Account',

    )

    def write(self, values):
        res = super(ResUsers, self).write(values)
        if 'analytic_config_ids' in values:
            self.env['ir.model.access'].call_cache_clearing_methods()
            self.env['ir.rule'].clear_caches()
            self.has_group.clear_cache(self)
        return res

    # @api.constrains('analytic_config_ids')
    # def update_analytic_restrict(self):
    #     restrict_group = self.env.ref('analytic_account_user_restrict.analytic_restrict_group')
    #     for user in self:
    #         if user.analytic_config_ids:
    #             # add users to restriction group
    #             # Due to strange behaviuor, we must remove the user from the group then
    #             # re-add him again to get restrictions applied
    #             restrict_group.write({'users': [(3, user.id)]})
    #             user.groups_id = [(3, restrict_group.id)]
    #             ## re-add
    #             restrict_group.write({'users': [(4, user.id)]})
    #             user.groups_id = [(4, restrict_group.id)]
    #         else:
    #             restrict_group.write({'users': [(3, user.id)]})
    #             user.groups_id = [(3, restrict_group.id)]
    #
    #         self.env.user.context_get.clear_cache(self)
