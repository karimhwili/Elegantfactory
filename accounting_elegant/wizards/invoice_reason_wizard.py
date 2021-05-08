from odoo import fields, models, api


class ReasonWoWizard(models.TransientModel):
    _name = 'reason.invoice'
    _description = 'Description'

    reason = fields.Char('Reason', required=1)

    def get_cancel_reason(self):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        invoice_id = self.env['account.move'].browse(docs).id
        invoice_id.reason = self.reason
        invoice_id.cancel_invoice()
