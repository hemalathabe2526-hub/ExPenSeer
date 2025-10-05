from odoo import models, fields

class ApprovalFlow(models.Model):
    _name = 'expense.seer.approval.flow'
    _description = 'Approval Flow'

    name = fields.Char(string='Flow Name', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True)
    sequence = fields.Integer(string='Sequence', default=1)
    approver_id = fields.Many2one('res.users', string='Approver', required=True)
    condition = fields.Text(string='Condition (DSL)')
