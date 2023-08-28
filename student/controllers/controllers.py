# -*- coding: utf-8 -*-
# from odoo import http


# class PerfectTech/student(http.Controller):
#     @http.route('/perfect_tech/student/perfect_tech/student', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/perfect_tech/student/perfect_tech/student/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('perfect_tech/student.listing', {
#             'root': '/perfect_tech/student/perfect_tech/student',
#             'objects': http.request.env['perfect_tech/student.perfect_tech/student'].search([]),
#         })

#     @http.route('/perfect_tech/student/perfect_tech/student/objects/<model("perfect_tech/student.perfect_tech/student"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('perfect_tech/student.object', {
#             'object': obj
#         })
