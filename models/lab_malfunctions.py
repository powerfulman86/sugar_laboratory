# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class LabMalfunctions(models.Model):
    _name = 'lab.malfunctions'
    _description = 'Laboratory Malfunctions'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char('Description')
    internal_reference = fields.Integer(string="Internal Reference", required=False, )
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True, tracking=True,
                            help="Set active to false to hide the Malfunction without removing it.")
    child_ids = fields.One2many(comodel_name="lab.malfunctions.branch", string="Child Ids",
                                inverse_name="malfunction_id")


class LabMalfunctionsBranch(models.Model):
    _name = 'lab.malfunctions.branch'
    _description = 'Lab Branch Malfunctions'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char()
    branch_id = fields.Many2one(comodel_name="res.branch", string="Branch", required=True,
                                index=True, tracking=1, help='This is branch to set malfunction for')
    malfunction_id = fields.Many2one(comodel_name="lab.malfunctions", string="Malfunction", required=True, )
    date_start = fields.Datetime(string="Start Date", required=True, default=fields.Date.context_today, copy=False)
    date_end = fields.Datetime(string="End Date", required=True, default=fields.Date.context_today, copy=False)
    notes = fields.Text('Notes')
    state = fields.Selection(string="Status",
                             selection=[('draft', 'Draft'), ('approved', 'Approved'), ('cancel', 'Cancel'), ],
                             required=True, default='draft')

    def action_approve(self):
        self.state = 'approved'

    def action_cancel(self):
        self.state = 'cancel'

    def unlink(self):
        if self.state != 'draft':
            raise ValidationError(_("Record Can't be deleted, it's not in draft status"))
        return super(LabMalfunctionsBranch, self).unlink()

    @api.model
    def create(self, values):
        res = super(LabMalfunctionsBranch, self).create(values)
        res.name = self.env['ir.sequence'].next_by_code('lab.malfunctions.branch') or '/'
        return res
