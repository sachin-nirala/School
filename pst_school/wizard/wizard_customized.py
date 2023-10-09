# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
import logging


class SchoolStudentWizard(models.TransientModel):
    _name = "school.student.wizard"
    _description = "Student management wizard modules"
    name = fields.Char(string='Student Name')
    roll_no = fields.Integer(string='Roll NO', compute= "auto_fill")
    marks = fields.Float(string="Student marks", digits=(3, 2), compute= "auto_fill")
    start = fields.Boolean(string = "Start")


    @api.depends('roll_no', 'marks')
    def auto_fill(self):
        print('gdfhhhhnb')
        x = self.env['school.student'].browse(self.env.context.get('active_id'))
        if x.exists():
            self.roll_no = x.roll_no
            self.marks = x.marks







    @api.onchange('name')
    def action_done(self):
        # sachin = self.env.context.get('active_id')
        # print(sachin)
        records = self.env['school.student'].browse(self.env.context.get('active_id'))
        print(records)
        print("================++++++++++++++++++++============")
        if records.exists():
            self.name = records.name

    def create_student_method(self):
        print("button is clicked")
