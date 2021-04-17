from odoo import fields, models, api


class RespartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    bank_branch = fields.Many2one('bank.branch',"Bank branch",domain="[('bank_id','=',bank_id)]")


class BankBranch(models.Model):
    _name = 'bank.branch'
    _rec_name = 'name'

    name = fields.Char('Branch',store=True)
    bank_id = fields.Many2one('res.bank',"Bank")


