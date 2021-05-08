from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    account_type = fields.Selection([('expense','Expense'),
                                     ('adding','Adding')],"Account Type",default='expense')
    account_id = fields.Many2one('account.account', string='Expense Account', domain="[('user_type_id.internal_group', '=', 'expense')]")
    account_id_adding = fields.Many2one('account.account', string='Adding Account', domain="[('user_type_id.internal_group', '=', 'asset')]")
