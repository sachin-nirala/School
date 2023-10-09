# -*- coding: utf-8 -*-
import xlwt
import base64
from io import BytesIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning



class SaleOrder(models.Model):
    _inherit = "sale.order"
    _description = "Student management modules"

    teacher_id = fields.Many2one('school.teacher', string='Teacher Name')


    sale_description = fields.Many2one('sale.order', string='Sale description')
    sale_line_ids = fields.One2many('school.book.line', 'sale_order_id', string='Book Ids')

    def action_xlwt_report(self):
        company_name = self.company_id.name
        file_name = 'Report.xls'
        workbook = xlwt.Workbook(encoding="UTF-8")
        format0 = xlwt.easyxf(
            'font:height 500,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center; borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;')
        formathead2 = xlwt.easyxf(
            'font:height 250,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center; borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;')
        format1 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left; borders: top_color black, bottom_color black, right_color black, left_color black,\
                                  left thin, right thin, top thin, bottom thin;')
        format2 = xlwt.easyxf('font:bold True;align: horiz left')
        format3 = xlwt.easyxf('align: horiz left; borders: top_color black, bottom_color black, right_color black, left_color black,\
                                  left thin, right thin, top thin, bottom thin;')
        format4 = xlwt.easyxf( 'font:bold True, color red; align: horiz left; borders: top_color black, bottom_color black, right_color black, left_color black,\
                                          left thin, right thin, top thin, bottom thin;')
        sheet = workbook.add_sheet("Payslip Summary Report")
        sheet.col(0).width = int(7 * 260)
        sheet.col(1).width = int(30 * 260)
        sheet.col(2).width = int(40 * 260)
        sheet.col(3).width = int(20 * 260)
        sheet.row(0).height_mismatch = True
        sheet.row(0).height = 150 * 4
        sheet.row(1).height_mismatch = True
        sheet.row(1).height = 150 * 2
        sheet.row(2).height_mismatch = True
        sheet.row(2).height = 150 * 3
        sheet.write_merge(0, 0, 0, 3, 'Advance Bank Report', format0)
        sheet.write_merge(1, 1, 0, 3, 'Date:' + str(self.date_order), formathead2)
        sheet.write_merge(2, 2, 0, 3, 'Company : ' + company_name, formathead2)
        sheet.write_merge(15, 16, 0, 0, 'S.No', format1)
        sheet.write_merge(15, 16, 1, 1, 'Product Lines', format1)
        sheet.write_merge(15, 16, 2, 2, 'Description', format1)
        sheet.write_merge(15, 16, 3, 3, 'Quantity', format1)
        sheet.write_merge(15, 16, 4, 4, 'UoM', format1)
        sheet.write_merge(15, 16, 5, 5, 'Price', format1)
        sheet.write_merge(15, 16, 6, 6, 'Subtotal', format1)
        sheet.write(3, 0, self.name, format1)
        sheet.write(4, 0,'Custumer : ', format1)
        sheet.write(4, 1, self.partner_id.name, format3)
        sheet.write(5, 1, self.partner_id.street, format3)
        sheet.write(6, 1, self.partner_id.state_id.name, format3)
        sheet.write(7, 1, self.partner_id.zip, format3)

        a = 17

        s = 1

        for each in self.order_line:
            sheet.write(a, 0, s, format1)
            sheet.write(a, 1, each.product_id.name, format3)
            sheet.write(a, 2, each.name, format3)
            sheet.write(a, 3, each.product_uom_qty, format3)
            sheet.write(a, 4, each.product_uom.name, format3)
            sheet.write(a, 5, each.price_unit, format3)
            sheet.write(a, 6, each.price_subtotal, format3)
            a += 1
            s += 1
        sheet.write_merge(a, a+1, 5, 6, "Total: " + str(self.amount_total), format4)
        fp = BytesIO()
        workbook.save(fp)
        out = base64.encodebytes(fp.getvalue())

        view_report_status_id = self.env['view.xls.report'].create({'file_name': out, 'datas_fname': file_name})

        fp.close()
        return {
            'res_id': view_report_status_id.id,
            'name': 'Sale Order',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'view.xls.report',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }


class ViewXlsReport(models.TransientModel):
    _name = 'view.xls.report'
    _description = 'XL report'
    _rec_name = 'datas_fname'

    datas_fname = fields.Char('File Name', size=256)
    file_name = fields.Binary('Download Here')
