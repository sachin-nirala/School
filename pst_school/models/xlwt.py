# # -*- coding: utf-8 -*-
# from odoo import api, fields, models, _, tools
# from odoo.osv import expression
# from dateutil.relativedelta import relativedelta
# from datetime import date
# from odoo.exceptions import UserError, ValidationError
# import xlwt
#
#
#
#
# class SchoolStudent(models.Model):
#     _name = "school.student"
#     _description = "Student management modules"
#     name = fields.Char(string='student Name')
#     reference = fields.Char(string='Reference', required=True, copy=False, readonly=True, default=lambda self: _('new'))
#     roll_no = fields.Integer(string='Roll NO')
#
#     present_day = fields.Date(string="Date")
#
#     marks = fields.Float(string="Student marks", digits=(3, 2))
#     remarks = fields.Text(string='Remarks')
#
#     date_closed = fields.Datetime(string='Closed Date', copy=False)
#
#     date_of_birth = fields.Datetime(string='Date of Birth')
#
#     age = fields.Char(string='Age', compute="_compute_age")
#
#     subject = fields.Selection(
#         selection=[('mathmatics', 'Mathmatics'), ('english', 'Englist'), ('hindi', 'Hindi'), ('science', 'Science')],
#         string='subject')
#     ispass = fields.Boolean(string='Is pass')
#
#     @api.model
#     def create(self, vals):
#         if not vals.get('name'):
#             raise UserError(_('New value change'))
#         vals['reference'] = self.env['ir.sequence'].next_by_code('school.student') or _('New')
#         res = super(SchoolStudent, self).create(vals)
#         return res
#
#     @api.depends('age')
#     def _compute_age(self):
#         years = ''
#         months = ''
#         day = ''
#         for rec in self:
#             if rec.date_of_birth:
#                 years = relativedelta(date.today(), rec.date_of_birth).years
#                 months = relativedelta(date.today(), rec.date_of_birth).months
#                 day = relativedelta(date.today(), rec.date_of_birth).days
#
#                 rec.age = str(int(years)) + ' Year\'s ' + str(int(months)) + ' Month\'s ' + str(int(day)) + ' Day\'s'
#             else:
#                 rec.age = 'I don t know!!'
#
#     teacher_id = fields.Many2one('school.teacher', string='Teacher ID')
#
#     book_line_ids = fields.One2many('school.book.line', 'student_id', string='Book Ids')
#     marks_line_ids = fields.One2many('school.marks.line', 'marks_id', string='Marks Ids')
#     total_marks = fields.Integer(string='Total marks', compute="_compute_total_marks")
#     sub = fields.Char(string='SUBJECT', compute="_show_subjects")
#     tag_ids = fields.Many2many('school.book.line', string='Tags')
#
#     # @api.onchange('name')
#     # def onchange_name(self):
#     #     raise UserError(_('New value change'))
#
#     @api.depends('subject')
#     def _show_subjects(self):
#         for rec in self:
#             all_subjects = ""
#
#             for each in rec.marks_line_ids:
#                 if each.subjects:
#                     all_subjects += str(each.subjects) + ', '
#             rec.sub = all_subjects
#
#     @api.depends('marks')
#     def _compute_total_marks(self):
#         for rec in self:
#             if rec.marks_line_ids:
#                 for each in rec.marks_line_ids:
#                     rec.total_marks += each.marks
#             else:
#                 rec.total_marks = 0
#         else:
#             pass
#
#     def check_method(self):
#         for rec in self:
#             # search in odoo
#             students = self.env['school.student'].search([])
#             math_students = self.env['school.student'].search([('subject', '=', 'mathmatics')])
#             math_students_roll_no = self.env['school.student'].search(
#                 [('subject', '=', 'mathmatics'), ('roll_no', '=', '2')])
#             print("students __________", students)
#             print("Mathmatics student ======== ", math_students)
#             print("Mathmatics student roll_no ======== ", math_students_roll_no)
#             students_count = self.env['school.student'].search_count([])
#             # search_count in odoo
#             math_students_count = self.env['school.student'].search_count([('subject', '=', 'mathmatics')])
#             students_count = self.env['school.student'].search_count([])
#             print("Total student of mathmatics======", math_students_count)
#             print("Total student is ", students_count)
#             math_students = self.env['school.student'].search([('subject', '=', 'physics')])
#             print("++++++++++++++++", math_students)
#
#             # # ref method in odoo
#             # school_students = self.env.ref('school.student.school_student_view_form')
#             # print(school_students)
#
#             # ================browse method===================
#             # browse_student = self.env['school.student'].browse([1, 4])
#             # browse_student = self.env['school.student'].browse(2000)
#             # if browse_student.exists():
#             #     print(" This record is Exists")
#             # else:
#             #     print("Nooooot exists")
#
#             # print("browse student=========", browse_student)
#             # ================create method===================
#             vals = [
#                 {
#                     'name': 'prjwfj',
#                     'roll_no': '789458',
#                     'marks': '97',
#                     'remarks': 'hell*****o'
#
#                 },
#                 {
#                     'name': 'mtrv',
#                     'roll_no': '13665',
#                     'marks': '70',
#                     'remarks': 'hell---------'
#                 },
#                 {
#                     'name': 'manmcvercveak',
#                     'roll_no': '2290856',
#                     'marks': '71',
#                     'remarks': 'hel0896589+++++++++++++------llo'
#                 }
#             ]
#             # for val in vals:
#             #     created_record = self.env['school.student'].create(val)
#             #
#             #
#             #     print(" print record id is=====", created_record, created_record.id)
#
#             ######====================write methord-------------------------------
#             update_created_record = self.env['school.student'].browse(19)
#             if update_created_record.exists:
#                 vals = {
#                     'name': 'Mungarilal',
#                     'roll_no': '007',
#                     'marks': '24',
#                     'remarks': 'mungarilan ka gao bada sunder hai.'
#                 }
#                 update_created_record.write(vals)
#             #####========================copy----------------------
#             copy_created_record = self.env['school.student'].browse(74)
#             # copy_created_record.copy()
#             #     ========================unlink-----------------
#             unlink_created_record = self.env['school.student'].browse(75)
#             unlink_created_record.unlink()
#
#         # print("==============Sachin===============")
#
#
# class SchoolTeacher(models.Model):
#     _name = "school.teacher"
#     _description = "Teacher management modules"
#
#     name = fields.Char(string='Teacher Name')
#     student_id = fields.Many2one('school.student', string='Student')
#
#
# class SchoolBooksLine(models.Model):
#     _name = "school.book.line"
#     _description = "Books management"
#
#     name = fields.Char(string='Book Name')
#     color = fields.Integer(string='color')
#     color_2 = fields.Char(string='color 2')
#     # author = fields.Char(string='Author name')
#     student_id = fields.Many2one('school.student', string='Student')
#     sale_order_id = fields.Many2one('sale.order', string='Sale order')
#
#
# class SchoolMarksLine(models.Model):
#     _name = "school.marks.line"
#     _description = "Marks sum module"
#
#     name = fields.Char(string='name')
#     subjects = fields.Selection(
#         selection=[('mathmatics', 'Mathmatics'), ('english', 'Englist'), ('hindi', 'Hindi'), ('science', 'Science')],
#         string='subjects')
#     marks = fields.Integer(string='marks')
#
#     marks_id = fields.Many2one('school.student', string='Marks')
#
#     # @api.onchange('name')
#     # def onchange_name(self):
#     #     raise UserError(_('New value change'))
