from odoo import models, fields, api, exceptions

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
    student_id = fields.Many2one(comodel_name='res.partner', required=True)
    phone = fields.Char(related='student_id.phone')
    
    @api.model
    def _generate_name(self):
        sequence = self.env['ir.sequence'].next_by_code('student.registration.name.code')
        return sequence