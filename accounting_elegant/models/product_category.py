from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'
    property_scrap_account_id = fields.Many2one('account.account', 'Scrap Account',
                                                domain="[('internal_group', '=', 'expense')]", company_dependent=True)

    income_add_stock_account_id = fields.Many2one(
        'account.account', string='Add Account', domain="[('internal_group','=','expense')]", company_dependent=True)
