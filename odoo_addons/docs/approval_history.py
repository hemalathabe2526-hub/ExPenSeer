from odoo import models, fields, api
import hashlib


class ApprovalHistory(models.Model):
    _name = 'expense.seer.approval.history'
    _description = 'Approval History'

    claim_id = fields.Many2one('expense.seer.claim', string='Expense Claim', required=True, ondelete='cascade')
    approver_id = fields.Many2one('res.users', string='Approver', required=True)
    approver_role = fields.Selection([
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('finance', 'Finance'),
        ('director', 'Director'),
        ('system', 'System')
    ], string='Approver Role')
    date = fields.Datetime(string='Date', required=True, default=fields.Datetime.now)
    state = fields.Selection([
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending')
    ], string='State', required=True)
    comments = fields.Text(string='Comments')

    # Explainability / AAE fields
    decision_reason = fields.Text(string='Decision Reason')
    aae_confidence = fields.Float(string='AAE Confidence', digits=(12, 6))
    was_auto_approved = fields.Boolean(string='Auto Approved by AAE', default=False)

    # Immutable audit fields (stored on-chain in a complete system)
    blockchain_hash = fields.Char(string='Blockchain Hash', readonly=True, copy=False)
    ledger_tx = fields.Char(string='Ledger Transaction ID', readonly=True)

    @api.model
    def _compute_audit_hash(self, vals):
        """Compute a SHA256 hex digest for the approval event.

        This provides a stable fingerprint suitable for writing to a ledger in a later step.
        The computation uses claim reference (if available), approver id, date, state and comments.
        """
        parts = []
        # claim name may not be in vals; try to resolve when possible
        claim_name = None
        if vals.get('claim_id'):
            try:
                claim = self.env['expense.seer.claim'].browse(int(vals.get('claim_id')))
                claim_name = claim.name
            except Exception:
                claim_name = None
        if claim_name:
            parts.append(str(claim_name))
        else:
            parts.append(str(vals.get('claim_id', '')))
        parts.append(str(vals.get('approver_id', '')))
        parts.append(str(vals.get('date', fields.Datetime.now())))
        parts.append(str(vals.get('state', '')))
        parts.append(str(vals.get('comments', '') or ''))
        digest_input = '|'.join(parts).encode('utf-8')
        return hashlib.sha256(digest_input).hexdigest()

    @api.model_create_multi
    def create(self, vals_list):
        # compute blockchain_hash for each record before creation
        for vals in vals_list:
            try:
                vals['blockchain_hash'] = self._compute_audit_hash(vals)
            except Exception:
                vals['blockchain_hash'] = False
        records = super(ApprovalHistory, self).create(vals_list)

        # Link approver role if possible (best-effort)
        for rec in records:
            if not rec.approver_role and rec.approver_id:
                # try to copy role from res.users extension
                try:
                    rec.approver_role = rec.approver_id.role or False
                except Exception:
                    pass

        return records

    def verify_blockchain_hash(self):
        """Verify stored blockchain_hash matches a locally computed hash.

        Returns a dict mapping record id to (stored, computed, matches).
        """
        self.ensure_one()
        vals = {
            'claim_id': self.claim_id.id,
            'approver_id': self.approver_id.id,
            'date': self.date,
            'state': self.state,
            'comments': self.comments,
        }
        computed = self._compute_audit_hash(vals)
        stored = self.blockchain_hash or ''
        return {'stored': stored, 'computed': computed, 'matches': stored == computed}

    def push_to_ledger(self, simulate=True):
        """Simulate pushing this approval event to a ledger.

        In a full implementation this would call a ledger client (Hyperledger Fabric / Ganache)
        and persist the returned transaction id in `ledger_tx`.

        Here we set `ledger_tx` to a mock value if not already set and return it.
        """
        self.ensure_one()
        if self.ledger_tx:
            return self.ledger_tx

        if not self.blockchain_hash:
            # compute if missing (best-effort)
            try:
                vals = {
                    'claim_id': self.claim_id.id,
                    'approver_id': self.approver_id.id,
                    'date': self.date,
                    'state': self.state,
                    'comments': self.comments,
                }
                self.blockchain_hash = self._compute_audit_hash(vals)
            except Exception:
                self.blockchain_hash = False

        # Simulate ledger write
        if simulate:
            txid = 'mockchain:' + (self.blockchain_hash or '')[:24]
            self.ledger_tx = txid
            return txid
        # In a real implementation, place ledger client call here and update ledger_tx
        return False

