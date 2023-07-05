# -*- coding: utf-8 -*-
# from odoo import http


# class PayrollNbet(http.Controller):
#     @http.route('/payroll_nbet/payroll_nbet', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/payroll_nbet/payroll_nbet/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('payroll_nbet.listing', {
#             'root': '/payroll_nbet/payroll_nbet',
#             'objects': http.request.env['payroll_nbet.payroll_nbet'].search([]),
#         })

#     @http.route('/payroll_nbet/payroll_nbet/objects/<model("payroll_nbet.payroll_nbet"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payroll_nbet.object', {
#             'object': obj
#         })
