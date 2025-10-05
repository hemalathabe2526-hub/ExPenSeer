from odoo import models, fields

class ResUsersExtension(models.Model):
    _inherit = 'res.users'

    role = fields.Selection([
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee')
    ], string='Role', default='employee')
