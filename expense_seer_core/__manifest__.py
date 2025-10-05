# Manifest file for expense_seer_core module
{
    'name': 'Expense Seer Core',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'security/expense_seer_security.xml',
        'views/expense_claim_views.xml',
        'views/expense_menu.xml',
        'views/company_views.xml',
        'views/approval_flow_views.xml',
        'data/demo_data.xml',
    ],
}