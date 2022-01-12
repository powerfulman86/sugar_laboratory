# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

AVAILABLE_STATUS = [
    ('draft', 'Draft'),
    ('branchApproved', 'Branch Approved'),
    ('deptApproved', 'Dept. Approved'),
    ('approved', 'Approved'),
]


class LabSugarAnalysis(models.Model):
    _name = 'lab.sugar.analysis'
    _description = 'Lab Sugar Analysis'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    @api.model
    def get_seasons(self):
        return self.env['lab.season'].search([('current_season', '=', True)]).id

    @api.model
    def get_branch(self):
        if self.env.user.branch_id:
            return self.env.user.branch_id.id
        else:
            return ''

    name = fields.Char('Description')
    branch_id = fields.Many2one(comodel_name="res.branch", string="Branch", required=True, default=get_branch,
                                index=True, help='This is branch to set')
    entry_id = fields.Integer(string="Entry Number", required=True, tracking=True)
    entry_date = fields.Date(string="Transaction Date", required=True, default=fields.Date.context_today, copy=False,
                             tracking=True)
    state = fields.Selection(AVAILABLE_STATUS, string='state', tracking=True, default=AVAILABLE_STATUS[0][0],
                             required=True)
    season_id = fields.Many2one(comodel_name="lab.season", string="Season", default=get_seasons, required=True,
                                index=True, help='This is branch to set')
    season_estimate_daily = fields.Float(string="Season Daily Estimate", required=False, )
    malfunction_line = fields.One2many(comodel_name="lab.malfunctions.branch", inverse_name="analysis_id",
                                       string="Malfunction Line", required=False, )
    down_time = fields.Integer(string="Down Time", required=False, )
    entry_notes = fields.Html('Notes', help='Notes', tracking=True)

    can_crashed_ton = fields.Float(string="Can Crashed / Ton", required=True, default=0)
    can_sweetness = fields.Float(string="Sweetness", required=False, default=0)
    juice_mix_purity = fields.Float(string="Juice mixed Purity", required=False, default=0)
    juice_main_val = fields.Float(string="Juice Main Val", required=False, default=0)
    juice_lab_val = fields.Float(string="Juice Lab Val", required=False, default=0)
    first_squeeze_extract = fields.Float(string="First Squeeze Extract", required=False, default=0)
    berx_juice_mix = fields.Float(string="Berx Juice Mix", required=False, default=0)
    extract_125_fiber = fields.Float(string="Extract 12.5 Fiber", required=False, default=0)
    sugar_a_ton = fields.Float(string="Sugar A \ Ton", required=False, default=0.0, digits=(10, 3))
    sugar_brown_ton = fields.Float(string="Sugar Brown \ Ton", required=False, default=0.0, digits=(10, 3))
    sugar_b_ton = fields.Float(string="Sugar B \ Ton", required=False, default=0.0, digits=(10, 3))
    sugar_produced_ton = fields.Float(string="Sugar Produced - Ton", required=False, compute="_compute_total_produced",
                                      store=True, readonly=1, default=0)
    can_sugar_rate = fields.Float(string="Can Sugar Rate", required=False, compute="_can_sugar_rate", store=True,
                                  readonly=1, default=0, digits=(4, 2))
    sugar_a_colour = fields.Float(string="Sugar A \ Colour", required=False, default=0, digits=(10, 0))
    sugar_b_colour = fields.Float(string="Sugar B \ Colour", required=False, default=0, digits=(10, 0))
    moulas_qty_ton = fields.Float(string="Moulas Qty\Ton", required=False, default=0, digits=(10, 3))
    moulas_brix = fields.Float(string="Moulas Brix", required=False, default=0)
    moulas_purity = fields.Float(string="Moulas Purity", required=False, default=0)
    sugar_moulas_rate = fields.Float(string="Sugar Moulas rate", required=False, default=0)
    lose_moulas = fields.Float(string="Moulas Lose", required=False, default=0)
    lose_bagas = fields.Float(string="Bagas Lose", required=False, default=0)
    lose_mud = fields.Float(string="Mud Lose", required=False, default=0)
    lose_total = fields.Float(string="Total Lose", required=False, readonly=1, compute="_calculate_total_lose",
                              default=0, store=True)
    water_raw_fiber = fields.Float(string="Water Raw Fiber", required=False, default=0, digits=(10, 0))
    bagas_humidity = fields.Float(string="Bagas Humidity", required=False, default=0)
    brix_sherbat = fields.Float(string="Brix Sherbat", required=False, default=0)
    juice_clear_lees = fields.Float(string="Juice Clear Lees", required=False, default=0, digits=(10, 0))
    steam_amount = fields.Float(string="Steam Amount", required=False, default=0)
    fuel_coal_qty = fields.Float(string="Fuel Coal Qty", required=False, default=0)
    mazout_used = fields.Float(string="Mazout Used", required=False, default=0)
    gas_used = fields.Float(string="Gas Used", required=False, default=0)
    mazout_gas_rate = fields.Float(string="Mazout Gas rate", required=False, compute="_calculate_mazout_gas", default=0)
    mazout_total = fields.Float(string="Mazout Total", compute="_calculate_total_mazout", default=0)
    steam_avr = fields.Float(string="Steam Per Ton", required=False, compute="_calculate_steam_avr",
                             store=True)

    entry_month = fields.Integer(string="Month", required=False, compute="_set_month_day", store=True, )
    entry_day = fields.Integer(string="Day", required=False, compute="_set_month_day", store=True, )

    @api.onchange('entry_date')
    def _set_month_day(self):
        for rec in self:
            if rec.entry_date:
                rec.entry_month = rec.entry_date.month
                rec.entry_day = rec.entry_date.day

    @api.onchange('season_id', 'branch_id')
    def get_season_estimate(self):
        # if self.season_id:
        #     season_status = self.env['lab.season.estimate'].search([('season_id', '=', self.season_id.id)])
        #     if season_status:
        #         if season_status.state != 'approved':
        #             raise ValidationError(
        #                 _("Season Estimate Data Is Not Approved , PLease Approve Data First"))
        #     else:
        #         raise ValidationError(
        #             _("Season Estimate Data Must Be Set , PLease Record Estimate Data First"))

        if self.season_id and self.branch_id:
            branch_estimate = self.env['lab.season.estimate.line'].search(
                [('season_id', '=', self.season_id.id), ('branch_id', '=', self.branch_id.id)])
            # if branch_estimate:
            self.season_estimate_daily = branch_estimate.season_estimate_daily

    @api.depends('steam_amount', 'can_crashed_ton')
    @api.onchange('steam_amount', 'can_crashed_ton')
    def _calculate_steam_avr(self):
        for rec in self:
            if rec.steam_amount and rec.can_crashed_ton:
                if rec.can_crashed_ton > 0:
                    rec.steam_avr = ((rec.steam_amount or 0.0) * 1000) / (rec.can_crashed_ton or 0.0)

    @api.depends('can_sugar_rate', 'can_sweetness')
    @api.onchange('can_sugar_rate', 'can_sweetness')
    def _calculate_total_lose(self):
        var2 = (self.can_sugar_rate or 0.0) - .02
        self.lose_total = (self.can_sweetness or 0.0) - var2

    @api.depends('gas_used')
    @api.onchange('gas_used')
    def _calculate_mazout_gas(self):
        self.mazout_gas_rate = (self.gas_used or 0.0) / 1083

    @api.depends('mazout_gas_rate', 'mazout_used')
    @api.onchange('mazout_gas_rate', 'mazout_used')
    def _calculate_total_mazout(self):
        self.mazout_total = (self.mazout_gas_rate or 0.0) + (self.mazout_used or 0.0)

    @api.depends('sugar_a_ton', 'sugar_b_ton', 'can_crashed_ton')
    @api.onchange('sugar_a_ton', 'sugar_b_ton', 'can_crashed_ton')
    def _can_sugar_rate(self):
        if self.can_crashed_ton != 0:
            self.can_sugar_rate = ((((self.sugar_a_ton or 0.0) + ((self.sugar_b_ton or 0.0) * .9)) * 100) / (
                    self.can_crashed_ton or 0.0))

    @api.depends('sugar_a_ton', 'sugar_brown_ton', 'sugar_b_ton')
    @api.onchange('sugar_a_ton', 'sugar_brown_ton', 'sugar_b_ton')
    def _compute_total_produced(self):
        self.sugar_produced_ton = (self.sugar_a_ton or 0.0) + (self.sugar_brown_ton or 0.0) + (self.sugar_b_ton or 0.0)

    def action_branch_approved(self):
        self.state = 'branchApproved'

    def action_dept_approved(self):
        self.state = 'deptApproved'

    def action_approved(self):
        self.state = 'approved'

    def action_set_draft(self):
        self.state = 'draft'

    @api.model
    def create(self, values):
        entry_no = values['entry_id']
        if entry_no == 0:
            raise ValidationError(
                _("Entry Number Must Be Set "))
        else:
            exist_branch_entry = self.env['lab.sugar.analysis'].search([
                ('season_id', '=', values['season_id']),
                ('branch_id', '=', values['branch_id']),
                ('entry_id', '=', values['entry_id']),
            ], limit=1)
            if len(exist_branch_entry.ids) > 0:
                raise ValidationError(
                    _("Can not Duplicate Lab Analysis , Other in %s" % exist_branch_entry.name))

        res = super(LabSugarAnalysis, self).create(values)
        res.name = self.env['ir.sequence'].next_by_code('lab.sugar.analysis') or '/'
        return res

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_('You can not delete a Sugar Entry Which Is Not In Draft State.'))
        return super(LabSugarAnalysis, self).unlink()

    @api.onchange('malfunction_line')
    def _set_line_branches(self):
        for line in self.malfunction_line:
            if not line.branch_id:
                line.branch_id = self.branch_id


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
    sequence = fields.Integer(string='Sequence', default=10)
    analysis_id = fields.Many2one(comodel_name="lab.sugar.analysis", string="Malfunction Analysis",
                                  required=True, )
    branch_id = fields.Many2one(comodel_name="res.branch", related='analysis_id.branch_id', string="Branch",
                                index=True, tracking=1, help='This is branch to set malfunction for')

    line_id = fields.Many2one(comodel_name="res.branch.sugar.line", string="Sugar Line", required=True, )
    malfunction_id = fields.Many2one(comodel_name="lab.malfunctions", string="Malfunction", required=True, )

    date_start = fields.Datetime(string="Start Date", required=True, default=fields.Date.context_today, copy=False)
    date_end = fields.Datetime(string="End Date", required=True, default=fields.Date.context_today, copy=False)
    down_time = fields.Integer(string="Down Time", required=False, )
    notes = fields.Text('Notes')

    @api.constrains('date_start', 'date_end')
    def _date_validation(self):
        for rec in self:
            down_time = int((rec.date_end - rec.date_start).total_seconds() / 60.0)
            if down_time and down_time <= 0:
                raise ValidationError(_("Malfunction End Date Must Be Greater than start date !"))

            rec.down_time = down_time
            rec.analysis_id.down_time = (rec.analysis_id.down_time or 0.0) +  down_time
