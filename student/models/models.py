# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class perfect_tech/student(models.Model):
#     _name = 'perfect_tech/student.perfect_tech/student'
#     _description = 'perfect_tech/student.perfect_tech/student'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
