from odoo import models, fields

class ResCompanyExtension(models.Model):
    _inherit = 'res.company'

    default_currency_id = fields.Many2one('res.currency', string='Default Currency')

    # Adaptive Approval Engine (AAE) settings
    aae_endpoint = fields.Char(string='AAE Endpoint', help='URL of the Adaptive Approval Engine (e.g. http://localhost:8001/suggest_chain)')
    aae_enabled = fields.Boolean(string='Enable AAE', default=False)
    aae_auto_approve_threshold = fields.Float(string='AAE Auto-approve Threshold', default=0.85, digits=(12, 4), help='If AAE confidence >= this value, auto-approve the claim')
