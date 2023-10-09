# -*- coding: utf-8 -*-
# from odoo import http


# class PstSale(http.Controller):
#     @http.route('/pst_sale/pst_sale', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pst_sale/pst_sale/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pst_sale.listing', {
#             'root': '/pst_sale/pst_sale',
#             'objects': http.request.env['pst_sale.pst_sale'].search([]),
#         })

#     @http.route('/pst_sale/pst_sale/objects/<model("pst_sale.pst_sale"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pst_sale.object', {
#             'object': obj
#         })
