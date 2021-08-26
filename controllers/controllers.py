# -*- coding: utf-8 -*-
# from odoo import http


# class SugarLaboratory(http.Controller):
#     @http.route('/sugar_laboratory/sugar_laboratory/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sugar_laboratory/sugar_laboratory/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sugar_laboratory.listing', {
#             'root': '/sugar_laboratory/sugar_laboratory',
#             'objects': http.request.env['sugar_laboratory.sugar_laboratory'].search([]),
#         })

#     @http.route('/sugar_laboratory/sugar_laboratory/objects/<model("sugar_laboratory.sugar_laboratory"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sugar_laboratory.object', {
#             'object': obj
#         })
