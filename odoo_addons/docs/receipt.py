from odoo import models, fields

class Receipt(models.Model):
    _name = 'expense.seer.receipt'
    _description = 'Receipt'

    name = fields.Char(string='Receipt Name', required=True)
    claim_id = fields.Many2one('expense.seer.claim', string='Expense Claim', required=True)
    attachment_id = fields.Many2one('ir.attachment', string='Attachment')
