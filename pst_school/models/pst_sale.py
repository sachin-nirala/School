# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PstSale(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order Inherit'


class PstSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _description = 'Sale Order Line Inherit'

    sr_no = fields.Integer('S. No.')
