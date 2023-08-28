from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_student = fields.Boolean(string='Is Student', default=False)
    birth_date = fields.Date(string='Birth Date')