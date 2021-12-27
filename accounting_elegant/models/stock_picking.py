from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = 'stock.picking'


    account_id = fields.Many2one('account.account', string='Expense Account', domain="[('user_type_id.internal_group', '=', 'expense')]")

