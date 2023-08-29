from odoo import http
from odoo.http import request

class StudentRegistrationWebsite(http.Controller):

    @http.route('/student/registration/submit', type='http', auth="public", website=True, csrf=False)
    def student_registration_create(self, **post):
        if post:
            # Validate fields and create the student registration
            student_registration = request.env['student.registration'].sudo().create({
                'student_id': int(post.get('student_id')),
                'phone': post.get('phone'),
                'date': post.get('date'),
                'amount': float(post.get('amount')),
            })
            # Provide feedback to the user
            return request.render('student.registration_success_template')
        
        students = request.env['res.partner'].sudo().search([('is_student', '=', True)])
        context = {
            'students': students,
        }

        return request.render('student.website_student_registration_page', context)
