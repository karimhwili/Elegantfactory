# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompanyBrand(models.Model):
    _inherit = 'res.company'

    brand = fields.One2many('brand.image','company_id', string="Brands Images")

class Brands(models.Model):
    _name = 'brand.image'

    company_id = fields.Many2one('res.company')
    brand = fields.Binary("Brand Image")
