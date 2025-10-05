from odoo import http
from odoo.http import request
import json


class ExpenseSeerClaimController(http.Controller):
    @http.route('/expense_seer/api/claim/submit', type='json', auth='user', methods=['POST'], csrf=False)
    def submit_claim(self, **kwargs):
        """Submit a claim. Expects JSON with keys: employee_id, date, currency_id, amount, category, merchant, description."""
        data = kwargs
        try:
            claim_vals = {
                'employee_id': data.get('employee_id'),
                'company_id': request.env.company.id,
                'date': data.get('date'),
                'currency_id': data.get('currency_id'),
                'amount': data.get('amount'),
                'category': data.get('category'),
                'merchant': data.get('merchant'),
                'description': data.get('description'),
            }
            claim = request.env['expense.seer.claim'].sudo().create(claim_vals)
            # submit
            claim.sudo().action_submit()
            return {'success': True, 'claim_id': claim.id, 'name': claim.name}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    @http.route('/expense_seer/api/claim/<int:claim_id>/approve', type='json', auth='user', methods=['POST'], csrf=False)
    def approve_claim(self, claim_id, **kwargs):
        data = kwargs
        try:
            claim = request.env['expense.seer.claim'].sudo().browse(claim_id)
            if not claim.exists():
                return {'success': False, 'error': 'Claim not found'}
            ctx = {
                'decision_reason': data.get('decision_reason'),
                'aae_confidence': data.get('aae_confidence'),
                'auto_approved': data.get('auto_approved', False),
                'comments': data.get('comments')
            }
            claim.with_context(**ctx).sudo().action_approve(comments=data.get('comments'))
            return {'success': True, 'claim_id': claim.id}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    @http.route('/expense_seer/api/approval/<int:approval_id>/push_ledger', type='json', auth='user', methods=['POST'], csrf=False)
    def push_approval_to_ledger(self, approval_id, **kwargs):
        try:
            approval = request.env['expense.seer.approval.history'].sudo().browse(approval_id)
            if not approval.exists():
                return {'success': False, 'error': 'Approval event not found'}
            txid = approval.sudo().push_to_ledger(simulate=True)
            return {'success': True, 'ledger_tx': txid}
        except Exception as e:
            return {'success': False, 'error': str(e)}
