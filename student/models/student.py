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
    phone = fields.Char(related='student_id.phone')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    date = fields.Date(string="Date", required=True)
    currency_id = fields.Many2one(comodel_name='res.currency',  readonly=True, default=lambda self: self.env.company.currency_id)
    amount = fields.Monetary(string='Registration Fees', required=True)
    state = fields.Selection(selection=STATE_CHOICES, string='State', default='draft')
    invoice_id = fields.Many2one(comodel_name='account.move')
    
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
                
    def create_invoice(self):
        # Create an invoice associated with this registration
        invoice_vals = {
            'partner_id': self.student_id.id,
            'currency_id': self.currency_id.id,
            'amount_total': self.amount,
        }
        invoice = self.env['account.move'].create(invoice_vals)
        self.write({'invoice_id': invoice.id})
        
    def open_invoice(self):
        if self.invoice_id:
            action = self.env.ref('account.action_move_out_invoice_type').read()[0]
            action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
            action['res_id'] = self.invoice_id.id
            return action
        else:
            return {'type': 'ir.actions.act_window_close'}