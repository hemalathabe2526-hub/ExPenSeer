from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ExpenseClaim(models.Model):
    _name = 'expense.seer.claim'
    _description = 'Expense Claim'

    name = fields.Char(string='Claim Reference', required=True, copy=False, readonly=True, default='New')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    date = fields.Date(string='Date', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True)
    amount = fields.Monetary(string='Amount', required=True)
    category = fields.Selection([
        ('travel', 'Travel'),
        ('meal', 'Meal'),
        ('office', 'Office Supplies'),
        ('entertainment', 'Entertainment'),
        ('other', 'Other')
    ], string='Category', required=True)
    merchant = fields.Char(string='Merchant')
    description = fields.Text(string='Description')
    receipt_ids = fields.One2many('expense.seer.receipt', 'claim_id', string='Receipts')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    approval_history_ids = fields.One2many('expense.seer.approval.history', 'claim_id', string='Approval History')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('expense.seer.claim') or 'New'
        return super(ExpenseClaim, self).create(vals)

    def action_submit(self):
        for claim in self:
            if claim.state != 'draft':
                raise ValidationError("Only draft claims can be submitted.")
            claim.state = 'submitted'
            # record a submission / pending event in approval history
            try:
                self.env['expense.seer.approval.history'].create({
                    'claim_id': claim.id,
                    'approver_id': self.env.uid,
                    'state': 'pending',
                    'comments': 'Submitted by %s' % (self.env.user.name,),
                    'approver_role': getattr(self.env.user, 'role', False) or 'employee',
                })
            except Exception:
                # best-effort: do not block submission if history create fails
                pass
            # Adaptive Approval Engine integration (best-effort)
            try:
                company = claim.company_id
                if getattr(company, 'aae_enabled', False) and company.aae_endpoint:
                    # call AAE endpoint
                    import requests
                    payload = {
                        'claim_id': claim.id,
                        'employee_id': claim.employee_id.id if claim.employee_id else False,
                        'amount': float(claim.amount or 0.0),
                        'currency': claim.currency_id.name if claim.currency_id else '',
                        'category': claim.category,
                        'merchant': claim.merchant or ''
                    }
                    try:
                        resp = requests.post(company.aae_endpoint, json=payload, timeout=3.0)
                        if resp.status_code == 200:
                            data = resp.json()
                            conf = float(data.get('confidence', 0.0))
                            reason = 'Suggested chain: %s' % (data.get('suggested_chain'),)
                            # auto-approve if confidence >= threshold
                            if conf >= float(getattr(company, 'aae_auto_approve_threshold', 0.9999)):
                                ctx = {
                                    'decision_reason': reason,
                                    'aae_confidence': conf,
                                    'auto_approved': True,
                                }
                                # call approve using context
                                claim.with_context(**ctx).action_approve()
                            else:
                                # add an approval history entry with the suggestion
                                try:
                                    self.env['expense.seer.approval.history'].create({
                                        'claim_id': claim.id,
                                        'approver_id': self.env.uid,
                                        'state': 'pending',
                                        'comments': 'AAE suggestion: %s (conf=%s)' % (data.get('suggested_chain'), conf),
                                        'decision_reason': reason,
                                        'aae_confidence': conf,
                                    })
                                except Exception:
                                    pass
                    except Exception:
                        # network / timeouts should not block submission
                        pass
            except Exception:
                pass

    def action_approve(self, comments=None):
        """Approve the claim and append an approval history record.

        Optional behaviour can be passed via context:
        - decision_reason: explainability text from AAE or rules
        - aae_confidence: float confidence score
        - auto_approved: boolean flag when AAE auto-approved
        """
        ctx = self.env.context or {}
        for claim in self:
            if claim.state != 'submitted':
                raise ValidationError("Only submitted claims can be approved.")
            claim.state = 'approved'
            vals = {
                'claim_id': claim.id,
                'approver_id': self.env.uid,
                'state': 'approved',
                'comments': comments or ctx.get('comments') or 'Approved by %s' % (self.env.user.name,),
                'decision_reason': ctx.get('decision_reason') or '',
                'aae_confidence': ctx.get('aae_confidence') or False,
                'was_auto_approved': bool(ctx.get('auto_approved', False)),
                'approver_role': getattr(self.env.user, 'role', False) or False,
            }
            try:
                self.env['expense.seer.approval.history'].create(vals)
            except Exception:
                # best-effort: proceed even if history logging fails
                pass

    def action_reject(self, comments=None):
        """Reject the claim and append an approval history record."""
        ctx = self.env.context or {}
        for claim in self:
            if claim.state != 'submitted':
                raise ValidationError("Only submitted claims can be rejected.")
            claim.state = 'rejected'
            vals = {
                'claim_id': claim.id,
                'approver_id': self.env.uid,
                'state': 'rejected',
                'comments': comments or ctx.get('comments') or 'Rejected by %s' % (self.env.user.name,),
                'decision_reason': ctx.get('decision_reason') or '',
                'aae_confidence': ctx.get('aae_confidence') or False,
                'was_auto_approved': False,
                'approver_role': getattr(self.env.user, 'role', False) or False,
            }
            try:
                self.env['expense.seer.approval.history'].create(vals)
            except Exception:
                pass