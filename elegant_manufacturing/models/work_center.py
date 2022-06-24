# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WorkCenter(models.Model):
    _inherit = 'mrp.workcenter'

    operations_ids = fields.One2many('mrp.operations', 'workcenter_id', "Operations")
    bom_ids = fields.One2many('mrp.billofmaterials', 'workcenter_id', "Bill Of Materials")


class MrpOperations(models.Model):
    _name = 'mrp.operations'

    workcenter_id = fields.Many2one('mrp.workcenter')
    operation_id = fields.Many2one('mrp.routing.workcenter', "Operation")


class BillOfMaterials(models.Model):
    _name = 'mrp.billofmaterials'

    workcenter_id = fields.Many2one('mrp.workcenter')
    bom_id = fields.Many2one('mrp.bom', "BOM")
