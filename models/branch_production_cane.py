# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CaneProductionOrder(models.Model):
    _name = 'cane.production.order'
    _rec_name = 'name'
    _description = 'Cane Production Order'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']

    name = fields.Char(string='Request Reference', required=True, copy=False, readonly=True,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    user_id = fields.Many2one(
        'res.users', string='Responsible', index=True, tracking=2, default=lambda self: self.env.user)
    note = fields.Text('Notes')
    order_line = fields.One2many('cane.production.order.line', 'order_id', string='Cane Production Order Lines',
                                 states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True,
                                 auto_join=True)
    branch_shift = fields.Selection(string="Shift", selection=[('1', 'First'), ('2', 'Second'), ('3', 'Third'), ],
                                    required=False, )
    branch_id = fields.Many2one(comodel_name="res.branch", string="Branch", required=True,
                                index=True, tracking=1, readonly=True, states={'draft': [('readonly', False)]}, )
    order_date = fields.Date(string="Date", required=False, default=fields.Date.context_today)


class CaneProductionOrderLine(models.Model):
    _name = 'cane.production.order.line'
    _rec_name = 'name'
    _description = 'Cane Production Order Line'

    order_id = fields.Many2one('cane.production.order', string='Cane Production Order', required=False,
                               ondelete='cascade', index=True, copy=False)
    name = fields.Text(string='Description', )
