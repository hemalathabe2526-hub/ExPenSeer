import requests
import json

# Config
AAE_URL = 'http://localhost:8001/suggest_chain'
ODOO_APPROVE_URL = 'http://localhost:8069/expense_seer/api/claim/{claim_id}/approve'
CONF_THRESHOLD = 0.8


def demo(claim):
    r = requests.post(AAE_URL, json=claim)
    print('AAE response', r.json())
    resp = r.json()
    if resp.get('confidence', 0) >= CONF_THRESHOLD:
        # Auto-approve demo (requires session auth/cookie or token in headers in real setup)
        payload = {
            'decision_reason': 'Auto-approved by AAE',
            'aae_confidence': resp.get('confidence'),
            'auto_approved': True,
            'comments': 'Auto-approved by AAE demo script'
        }
        url = ODOO_APPROVE_URL.format(claim_id=claim['claim_id'])
        # Note: this will fail unless you add auth/session details; this is illustrative
        r2 = requests.post(url, json=payload)
        print('Odoo approve response', r2.status_code, r2.text)


if __name__ == '__main__':
    demo({'claim_id': 1, 'employee_id': 10, 'amount': 50.0, 'currency': 'USD', 'category': 'meal', 'merchant': 'Cafe'})
