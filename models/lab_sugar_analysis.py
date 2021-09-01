# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

AVAILABLE_STATUS = [
    ('draft', 'Draft'),
    ('branchApproved', 'Branch Approved'),
    ('deptApproved', 'Dept. Approved'),
    ('approved', 'Approved'),
    ('cancel', 'Cancel'),
]


class LabSugarAnalysis(models.Model):
    _name = 'lab.sugar.analysis'
    _description = 'Lab Sugar Analysis'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char('Description')
    branch_id = fields.Many2one(comodel_name="res.branch", string="Branch", required=True,
                                index=True, help='This is branch to set')
    entry_id = fields.Integer(string="Entry Number", required=True, )
    entry_date = fields.Date(string="Transaction Date", required=True, default=fields.Date.context_today, copy=False)
    state = fields.Selection(AVAILABLE_STATUS, string='state', tracking=True, default=AVAILABLE_STATUS[0][0],
                             required=True)
    season_id = fields.Many2one(comodel_name="lab.season", string="Season", required=True,
                                index=True, help='This is branch to set')
    entry_notes = fields.Html('Notes', help='Notes')

    can_crashed_ton = fields.Float(string="Can Crashed / Ton", required=True, default=0)
    can_sweetness = fields.Float(string="Sweetness", required=False, default=0)
    juice_mix_purity = fields.Float(string="Juice mixed Purity", required=False, default=0)
    juice_main_val = fields.Float(string="Juice Main Val", required=False, default=0)
    juice_lab_val = fields.Float(string="Juice Lab Val", required=False, default=0)
    first_squeeze_extract = fields.Float(string="First Squeeze Extract", required=False, default=0)
    berx_juice_mix = fields.Float(string="Berx Juice Mix", required=False, default=0)
    extract_125_fiber = fields.Float(string="Extract 12.5 Fiber", required=False, default=0)
    sugar_a_ton = fields.Float(string="Sugar A \ Ton", required=False, default=0)
    sugar_brown_ton = fields.Float(string="Sugar Brown \ Ton", required=False, default=0)
    sugar_b_ton = fields.Float(string="Sugar B \ Ton", required=False, default=0)
    sugar_produced_ton = fields.Float(string="Sugar Produced - Ton", required=False, compute="_compute_total_produced",
                                      store=True, readonly=1, default=0)
    can_sugar_rate = fields.Float(string="Can Sugar Rate", required=False, compute="_can_sugar_rate", store=True,
                                  readonly=1, default=0)
    sugar_a_colour = fields.Float(string="Sugar A \ Colour", required=False, default=0)
    sugar_b_colour = fields.Float(string="Sugar B \ Colour", required=False, default=0)
    moulas_qty_ton = fields.Float(string="Moulas Qty\Ton", required=False, default=0)
    moulas_brix = fields.Float(string="Moulas Brix", required=False, default=0)
    moulas_purity = fields.Float(string="Moulas Purity", required=False, default=0)
    lose_moulas = fields.Float(string="Moulas Lose", required=False, default=0)
    lose_bagas = fields.Float(string="Bagas Lose", required=False, default=0)
    lose_mud = fields.Float(string="Mud Lose", required=False, default=0)
    lose_total = fields.Float(string="Total Lose", required=False, readonly=1, compute="_calculate_total_lose",
                              default=0,store=True)
    water_raw_fiber = fields.Float(string="Water Raw Fiber", required=False, default=0)
    bagas_humidity = fields.Float(string="Bagas Humidity", required=False, default=0)
    brix_sherbat = fields.Float(string="Brix Sherbat", required=False, default=0)
    juice_clear_lees = fields.Float(string="Juice Clear Lees", required=False, default=0)
    steam_amount = fields.Float(string="Steam Amount", required=False, default=0)
    fuel_coal_qty = fields.Float(string="Fuel Coal Qty", required=False, default=0)
    mazout_used = fields.Float(string="Mazout Used", required=False, default=0)

    @api.depends('lose_moulas', 'lose_bagas', 'lose_mud')
    def _calculate_total_lose(self):
        self.lose_total = (self.lose_moulas or 0.0) + (self.lose_bagas or 0.0) + (self.lose_mud or 0.0)

    @api.depends('sugar_a_ton', 'sugar_b_ton')
    def _can_sugar_rate(self):
        self.can_sugar_rate = ((((self.sugar_a_ton or 0.0) + ((self.sugar_b_ton or 0.0) * .9)) * 100) / 2)

    @api.depends('sugar_a_ton', 'sugar_brown_ton', 'sugar_b_ton')
    def _compute_total_produced(self):
        self.sugar_produced_ton = (self.sugar_a_ton or 0.0) + (self.sugar_brown_ton or 0.0) + (self.sugar_b_ton or 0.0)

    def action_branch_approved(self):
        self.state = 'branchApproved'

    def action_dept_approved(self):
        self.state = 'deptApproved'

    def action_approved(self):
        self.state = 'approved'

    def action_cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, values):
        res = super(LabSugarAnalysis, self).create(values)
        res.name = self.env['ir.sequence'].next_by_code('lab.sugar.analysis') or '/'
        return res
