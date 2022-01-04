# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResBranchSugarLines(models.Model):
    _name = 'res.branch.sugar.line'
    _rec_name = 'name'
    _description = 'Branch Sugar Line'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char('Description')
    branch_id = fields.Many2one(comodel_name="res.branch", string="Branch", required=True,
                                index=True, tracking=1, help='This is branch to set malfunction for')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True, tracking=True,
                            help="Set active to false to hide the Malfunction without removing it.")


class ResBranchSugarPool(models.Model):
    _name = 'res.branch.sugar.pool'
    _rec_name = 'name'
    _description = 'Branch Sugar Pool'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char('Description')
    branch_id = fields.Many2one(comodel_name="res.branch", string="Branch", required=True,
                                index=True, tracking=1, help='This is branch to set malfunction for')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True, tracking=True,
                            help="Set active to false to hide the Malfunction without removing it.")


class SugarAnalysisType(models.Model):
    _name = 'sugar.analysis.type'
    _rec_name = 'name'
    _description = 'Sugar Analysis Type'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char('Description')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True, tracking=True,
                            help="Set active to false to hide the Malfunction without removing it.")