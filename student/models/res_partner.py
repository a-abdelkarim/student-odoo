from datetime import datetime, timedelta

from odoo import models, fields, api, exceptions

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_student = fields.Boolean(string='Is Student', default=False)
    birth_date = fields.Date(string='Birth Date')
    
    # Validate date of birth value
    @api.constrains('birth_date')
    def _check_age(self):
        # get current date
        today = datetime.today().date()
        # calc min & max birth date
        min_birth_date = today - timedelta(days=5*365)
        max_birth_date = today - timedelta(days=4*365)
        for partner in self:
            if partner.birth_date:
                if partner.birth_date < min_birth_date or partner.birth_date > max_birth_date:
                    raise exceptions.ValidationError("Your age must be between 4 and 5 years old.")