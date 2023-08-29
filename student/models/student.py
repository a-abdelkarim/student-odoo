from datetime import datetime
from odoo import models, fields, api, exceptions


STATE_CHOICES = [
    ('draft', 'Draft'), 
    ('confirmed', 'Confirmed'), 
    ('invoiced', 'Invoiced'), 
    ('canceled', 'Canceled')
]


class StudentRegistration(models.Model):
    _name = 'student.registration'
    
    name = fields.Char(
        string='Name', 
        required=True, 
        copy=False, 
        readonly=True, 
        default=
        lambda self: self._generate_name()
    )
    student_id = fields.Many2one(comodel_name='res.partner', domain=[('is_student', '=', True)], required=True)
    phone = fields.Char(related='student_id.phone', readonly=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    date = fields.Date("Date")
    currency_id = fields.Many2one(related='student_id.company_id.currency_id',  readonly=True)
    amount = fields.Monetary(string='Registration Fees', required=True)
    state = fields.Selection(selection=STATE_CHOICES, string='State', default='draft', readonly=True)
    
    @api.model
    def _generate_name(self):
        sequence = self.env['ir.sequence'].next_by_code('student.registration.name.code')
        return sequence
    
    @api.depends('student_id.birth_date')
    def _compute_age(self):
        for record in self:
            if record.student_id.birth_date:
                birth_date = fields.Date.from_string(record.student_id.birth_date)
                today = datetime.now().date()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                record.age = age
            else:
                record.age = False
    
    # actions
    def confirm_registration(self):
        for record in self:
            if record.state == 'confirmed':
                exceptions.UserError('Registration Already Confirmed!')
            else:
                record.state = 'confirmed'
                
    def cancel_registration(self):
        for record in self:
            if record.state == 'canceled':
                exceptions.UserError('Registration Already Canceled!')
            else:
                record.state = 'canceled'