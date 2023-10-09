# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.osv import expression
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.exceptions import UserError, ValidationError
import logging
try:
   import qrcode
except ImportError:
   qrcode = None
try:
   import base64
except ImportError:
   base64 = None
from io import BytesIO
import xlwt
import os
from PIL import Image
directory = os.path.dirname(__file__)

# _logger = logging.getLogger(__name__)


class SchoolStudent(models.Model):
    _name = "school.student"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Student management modules"

    def action_share_whatsapp(self):
        pass
    name = fields.Char(string='Student Name', tracking=True)
    reference = fields.Char(string='Reference', required=True, copy=False, readonly=True, default=lambda self: _('new'))
    roll_no = fields.Integer(string='Roll NO')

    present_day = fields.Date(string="Date")

    marks = fields.Float(string="Student marks", digits=(3, 2))
    remarks = fields.Text(string='Remarks')

    date_closed = fields.Datetime(string='Closed Date', copy=False)

    date_of_birth = fields.Datetime(string='Date of Birth')
    my_barcode = fields.Char(sting="Barcode")

    age = fields.Char(string='Age', compute="_compute_age")
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    fee = fields.Monetary(string="Fee")
    note = fields.Html(string='My Notes', tracking=True)
    image = fields.Image(string="Image")
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority",
        help='Gives the rate us')
    choose_one = fields.Selection(
        selection=[('mathmatics', 'Mathmatics'), ('english', 'Englist'), ('hindi', 'Hindi'), ('science', 'Science')],
        string='subjects')


    state = fields.Selection([
        ('draft', 'Draft'),
        ('conform', 'Conform'),
        ('done', 'Final'),
    ], string='Status', default='draft')
    progress = fields.Integer(Sting="Progress", compute='_compute_progress')

    subject = fields.Selection(
        selection=[('mathmatics', 'Mathmatics'), ('english', 'Englist'), ('hindi', 'Hindi'), ('science', 'Science')],
        string='subject')
    ispass = fields.Boolean(string='Is pass')
    file = fields.Binary(string="Choose file")

    # def add_professor(self):
    #     ids = [18,19,20,21]
    #     self.write({"tag_ids": [(6, 0, ids)]})


    def add_professor(self):
        pass
        # ids = self.tag_ids.st_tag_ids.ids
        # self.write({"tag_ids": [(6, 0, ids)]})


    @api.model
    def create(self, vals):
        # if not vals.get('name'):
        #     raise UserError(_('New value change'))
        vals['reference'] = self.env['ir.sequence'].next_by_code('school.student') or _('New')
        res = super(SchoolStudent, self).create(vals)
        return res

    @api.depends('age')
    def _compute_age(self):
        years = ''
        months = ''
        day = ''
        for rec in self:
            if rec.date_of_birth:
                years = relativedelta(date.today(), rec.date_of_birth).years
                months = relativedelta(date.today(), rec.date_of_birth).months
                day = relativedelta(date.today(), rec.date_of_birth).days

                rec.age = str(int(years)) + ' Year\'s ' + str(int(months)) + ' Month\'s ' + str(int(day)) + ' Day\'s'
            else:
                rec.age = 'I don t know!!'
    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = 25
            elif rec.state == 'conform':
                progress = 50
            elif rec.state == 'final':
                progress = 100
            else:
                progress = 0
            rec.progress = progress



    teacher_id = fields.Many2one('school.teacher', string='Teacher ID')

    book_line_ids = fields.One2many('school.book.line', 'student_id', string='Book Ids')
    marks_line_ids = fields.One2many('school.marks.line', 'marks_id', string='Marks Ids')
    total_marks = fields.Integer(string='Total marks', compute="_compute_total_marks")
    sub = fields.Char(string='SUBJECT', compute="_show_subjects")
    tag_ids = fields.Many2many('school.book.line', string='Tags')

    def update_my_field(self):
        for field in self.book_line_ids:
            field.write({'name': self.tag_id.name})

    # @api.onchange('name')
    # def onchange_name(self):
    #     raise UserError(_('Kuch toh name daloo!'))



    @api.depends('subject')
    def _show_subjects(self):
        for rec in self:
            all_subjects = ""

            for each in rec.marks_line_ids:
                if each.subjects:
                    all_subjects += str(each.subjects) + ', '
            rec.sub = all_subjects

    @api.depends('marks')
    def _compute_total_marks(self):
        for rec in self:
            if rec.marks_line_ids:
                for each in rec.marks_line_ids:
                    rec.total_marks += each.marks
            else:
                rec.total_marks = 0
        else:
            pass

    def state_method_conform(self):
        self.write({'state': "conform"})

    def state_method_final(self):
        self.write({'state': "done"})
        if not self.name:
            raise UserError(_('Kuch toh name daloo!'))

    def state_method_draft(self):
        self.write({'state': "draft"})

    # # @api.multi
    # def write(self, vals):
    #     if any(state == 'done' for state in set(self.mapped('state'))):
    #         raise UserError(_("No edit in final state"))
    #     else:
    #         return super().write(vals)

    def check_method(self):
        for rec in self:
            # search in odoo
            students = self.env['school.student'].search([])
            math_students = self.env['school.student'].search([('subject', '=', 'mathmatics')])
            math_students_roll_no = self.env['school.student'].search(
                [('subject', '=', 'mathmatics'), ('roll_no', '=', '2')])
            print("students __________", students)
            print("Mathmatics student ======== ", math_students)
            print("Mathmatics student roll_no ======== ", math_students_roll_no)
            students_count = self.env['school.student'].search_count([])
            # search_count in odoo
            math_students_count = self.env['school.student'].search_count([('subject', '=', 'mathmatics')])
            students_count = self.env['school.student'].search_count([])
            print("Total student of mathmatics======", math_students_count)
            print("Total student is ", students_count)
            math_students = self.env['school.student'].search([('subject', '=', 'physics')])
            print("++++++++++++++++", math_students)

            # # ref method in odoo
            # school_students = self.env.ref('school.student.school_student_view_form')
            # print(school_students)

            # ================browse method===================
            # browse_student = self.env['school.student'].browse([1, 4])
            # browse_student = self.env['school.student'].browse(2000)
            # if browse_student.exists():
            #     print(" This record is Exists")
            # else:
            #     print("Nooooot exists")

            # print("browse student=========", browse_student)
            # ================create method===================
            vals = [
                {
                    'name': 'prjwfj',
                    'roll_no': '789458',
                    'marks': '97',
                    'remarks': 'hell*****o'

                },
                {
                    'name': 'mtrv',
                    'roll_no': '13665',
                    'marks': '70',
                    'remarks': 'hell---------'
                },
                {
                    'name': 'manmcvercveak',
                    'roll_no': '2290856',
                    'marks': '71',
                    'remarks': 'hel0896589+++++++++++++------llo'
                }
            ]
            # for val in vals:
            #     created_record = self.env['school.student'].create(val)
            #
            #
            #     print(" print record id is=====", created_record, created_record.id)

            ######====================write methord-------------------------------
            update_created_record = self.env['school.student'].browse(19)
            if update_created_record.exists:
                vals = {
                    'name': 'Mungarilal',
                    'roll_no': '007',
                    'marks': '24',
                    'remarks': 'mungarilan ka gao bada sunder hai.'
                }
                update_created_record.write(vals)
            #####========================copy----------------------
            copy_created_record = self.env['school.student'].browse(74)
            # copy_created_record.copy()
            #     ========================unlink-----------------
            unlink_created_record = self.env['school.student'].browse(75)
            unlink_created_record.unlink()
            
            
        #     Excel report generating methord
    def action_invoice_xls_print(self):
        string = ''
        if self.state == 'draft':
            string = 'drafted_invoice'
        else:
            string = str(self.name)
        wb = xlwt.Workbook(encoding='utf-8')
        sheet = wb.add_sheet(string)
        sheet = wb.add_sheet("Sheet 1", cell_overwrite_ok=True)
        style = xlwt.easyxf('font: bold 1; align: horiz centre; borders: top_color black, bottom_color black, right_color black, left_color black,\
                                              left thin, right thin, top thin, bottom thin;\
                                    pattern: pattern solid, fore_color white;')
        centre_border = xlwt.easyxf('align: horiz centre; borders: top_color black, bottom_color black, right_color black, left_color black,\
                                              left thin, right thin, top thin, bottom thin;\
                                            pattern: pattern solid, fore_color white;')
        left_border = xlwt.easyxf('align: horiz left; borders: top_color black, bottom_color black, right_color black, left_color black,\
                                              left thin, right thin, top thin, bottom thin;\
                                            pattern: pattern solid, fore_color white;')
        centre_border_yel = xlwt.easyxf('align: horiz centre; borders: top_color black, bottom_color black, right_color black, left_color black,\
                                              left thin, right thin, top thin, bottom thin;\
                                            pattern: pattern solid, fore_color yellow;')
        centre_border_red = xlwt.easyxf('align: horiz centre; borders: top_color black, bottom_color black, right_color black, left_color black,\
                                                      left thin, right thin, top thin, bottom thin;\
                                                    pattern: pattern solid, fore_color red;')
        centre_border_gr = xlwt.easyxf('align: horiz centre; borders: top_color black, bottom_color black, right_color black, left_color black,\
                                                              left thin, right thin, top thin, bottom thin;\
                                                            pattern: pattern solid, fore_color green;')
        style1 = xlwt.easyxf('font: bold 1; align: vert centre;')
        style1_bor = xlwt.easyxf('font: bold 1; align: vert centre; borders: top_color black, bottom_color black, right_color black, left_color black,\
                                              left thin, right thin, top thin, bottom thin;\
                                    pattern: pattern solid, fore_color white;')
        borders = xlwt.easyxf('borders: top_color black, bottom_color black, right_color black, left_color black,\
                                              left thin, right thin, top thin, bottom thin;\
                                    pattern: pattern solid, fore_color white;')
        centre_border_grey = xlwt.easyxf('font: bold 1; pattern: pattern solid, fore_color gray25 ;')
        centre_border_blue = xlwt.easyxf(
            'font: bold 1,color white; pattern: pattern solid, fore_color light_blue ;')

        # bold_borders = xlwt.easyxf('font: bold 1; align: horiz centre; borders: top_color black, bottom_color black, right_color black, left_color black,\
        #                                       left thin, right thin, top thin, bottom thin;\
        #                             pattern: pattern solid, fore_colour custom_colour_gr;')
        date_format = xlwt.XFStyle()
        date_format.num_format_str = 'dd/mm/yyyy'

        a = 2

        filename = str(string + '.xls')

        # Insert Logo
        direc = ''
        if os.name == 'nt':
            direc = directory.replace('models', '') + "static\description\school.png"
        if os.name == 'posix':
            direc = directory.replace('models', '') + "static\description\school.png"
        img = Image.open(direc)
        image_parts = img.split()
        r = image_parts[0]
        g = image_parts[1]
        b = image_parts[2]
        img = Image.merge("RGB", (r, g, b))
        fo = BytesIO()
        img.save(fo, format='bmp')
        sheet.insert_bitmap_data(fo.getvalue(), 0, 0)

        # im = PILImage.open(StringIO(str(self.company_id.logo)))
        # img = Image(im)
        # img.anchor(ws.cell('F1'))
        # ws.add_image(img)

        # Billed From
        c = 10
        sheet.write(c, 0, 'Billed From.', style1_bor)
        sheet.write(c, 0, 'Sr. No.', style1_bor)
        sheet.write(c, 1, 'Item Code', style1_bor)
        sheet.write(c, 2, 'Primary Description', style1_bor)
        sheet.write(c, 3, 'Secondary Description', style1_bor)
        sheet.write(c, 4, 'HSN Code', style1_bor)
        sheet.write(c, 5, 'Qty', style1_bor)
        sheet.write(c, 6, 'UoM', style1_bor)
        sheet.write(c, 7, 'Attributes', style1_bor)
        sheet.write(c, 8, 'Rate', style1_bor)
        sheet.write(c, 9, 'Amount', style1_bor)
        c += 1
        c += 3
        fp = BytesIO()
        wb.save(fp)
        out = base64.encodebytes(fp.getvalue())

        view_report_status_id = self.env['view.xls.report'].create({'file_name': out, 'datas_fname': filename})
        return {
            'res_id': view_report_status_id.id,
            'name': 'Sale Order',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'view.xls.report',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }

    # print("==============Sachin===============")


class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _description = "Teacher management modules"

    name = fields.Char(string='Teacher Name')
    student_id = fields.Many2one('school.student', string='Student')

    def add_teacher(self):
        self.env['school.teacher'].create({
            'name': 'Ganesh',
        })

    def write(self, values):
        student_rec_set = self.env['school.student'].browse(values.get('student_id'))
        student_rec_set.write({'teacher_id':self.id})
        return super(SchoolTeacher, self).write(values)


class SchoolBooksLine(models.Model):
    _name = "school.book.line"
    _description = "Books management"

    name = fields.Char(string='Book Name')
    color = fields.Integer(string='color')
    color_2 = fields.Char(string='color 2')
    # author = fields.Char(string='Author name')
    st_tag_ids = fields.Many2many('school.student', string='Tags')
    student_id = fields.Many2one('school.student', string='Student')
    sale_order_id = fields.Many2one('sale.order', string='Sale order')
    roll_no = fields.Integer(related = 'student_id.roll_no', string = "Roll No")




class SchoolMarksLine(models.Model):
    _name = "school.marks.line"
    _description = "Marks sum module"

    name = fields.Char(string='name')
    subjects = fields.Selection(
        selection=[('mathmatics', 'Mathmatics'), ('english', 'Englist'), ('hindi', 'Hindi'), ('science', 'Science')],
        string='subjects')
    marks = fields.Integer(string='marks')

    marks_id = fields.Many2one('school.student', string='Marks')

    # @api.onchange('name')
    # def onchange_name(self):
    #     raise UserError(_('New value change'))

# class search(models.Model):
#     _inherit = 'res.partner'
#     def get_vehicles(self):
#         self.ensure_one()
#         return {
#             'type': 'ir.actions.act_window',
#             'name': 'Vehicles',
#             'view_mode': 'tree',
#             'res_model': 'fleet.vehicle',
#             'domain': [('driver_id', '=', self.id)],
#             'context': "{'create': False}"
#         }
class Product(models.Model):
   """ inherit Invoice to add report settings """
   _inherit = "product.template"
   qr_code = fields.Binary('QRcode', compute="_generate_qr")