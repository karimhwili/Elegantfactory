from odoo import fields, models, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    default_uom = fields.Many2one('uom.uom', string='Default Unit of measure')

class InheritProduct(models.Model):
    _inherit = 'product.template'

    tag_lot = fields.Char("Tag Lot")

    limits_groups = fields.Many2one('group.limit',"Group Limit")

    def generate_internal_number(self):
        for rec in self:
            if rec.categ_id.code:
                if int(rec.categ_id.code) == 12:
                    seq1 = self.env['ir.sequence'].next_by_code('product.template.internal1')
                    rec.default_code = rec.categ_id.code + seq1
                elif int(rec.categ_id.code) == 14:
                    seq2 = self.env['ir.sequence'].next_by_code('product.template.internal2')
                    rec.default_code = rec.categ_id.code + seq2
                elif int(rec.categ_id.code) == 15:
                    seq3 = self.env['ir.sequence'].next_by_code('product.template.internal3')
                    rec.default_code = rec.categ_id.code + seq3
                elif int(rec.categ_id.code) == 17:
                    seq4 = self.env['ir.sequence'].next_by_code('product.template.internal4')
                    rec.default_code = rec.categ_id.code + seq4
                elif int(rec.categ_id.code) == 19:
                    seq5 = self.env['ir.sequence'].next_by_code('product.template.internal5')
                    rec.default_code = rec.categ_id.code + seq5
                elif int(rec.categ_id.code) == 22:
                    seq6 = self.env['ir.sequence'].next_by_code('product.template.internal6')
                    rec.default_code = rec.categ_id.code + seq6
                elif int(rec.categ_id.code) == 24:
                    seq7 = self.env['ir.sequence'].next_by_code('product.template.internal7')
                    rec.default_code = rec.categ_id.code + seq7
                elif int(rec.categ_id.code) == 25:
                    seq8 = self.env['ir.sequence'].next_by_code('product.template.internal8')
                    rec.default_code = rec.categ_id.code + seq8



class GroupLimit(models.Model):
    _name = 'group.limit'
    _description = "Group Limit"
    _rec_name = 'name'

    name = fields.Char("Group Limit")
    group_limits = fields.One2many(
        'product.limits', 'group_id', "Customer Limits")

class ProductLimits(models.Model):
    _name = 'product.limits'
    _description = 'Product Limits'
    _rec_name = 'customer_id'

    group_id = fields.Many2one('group.limit')

    customer_id = fields.Many2one('res.partner', "Customer")
    limit = fields.Integer("Limit amount")
