# -*- coding: utf-8 -*-
# from odoo import http


# class Nbet15Cus(http.Controller):
#     @http.route('/nbet15_cus/nbet15_cus', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nbet15_cus/nbet15_cus/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('nbet15_cus.listing', {
#             'root': '/nbet15_cus/nbet15_cus',
#             'objects': http.request.env['nbet15_cus.nbet15_cus'].search([]),
#         })

#     @http.route('/nbet15_cus/nbet15_cus/objects/<model("nbet15_cus.nbet15_cus"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nbet15_cus.object', {
#             'object': obj
#         })
