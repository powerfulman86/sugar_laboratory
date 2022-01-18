# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class LabSeason(models.Model):
    _name = 'lab.season'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"
    _description = 'Lab Season'

    name = fields.Char(compute='_compute_name', string="Name", store=True)
    year_from = fields.Char('From', size=4, required=True)
    year_to = fields.Char('To', size=4, required=True)
    current_season = fields.Boolean("Current Season")
    active = fields.Boolean('Active', default=True, tracking=True,
                            help="Set active to false to hide the Season without removing it.")

    def name_get(self):
        result = []
        for rec in self:
            name = ('%s' % rec.name)
            result.append((rec.id, name))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        super(LabSeason, self).name_search(name)
        # args = args or []
        domain = []
        if name:
            domain = [('name', operator, name), ]
        recs = self.search(domain, limit=limit)
        return recs.name_get()

    @api.depends('year_from', 'year_to')
    def _compute_name(self):
        for rec in self:
            if rec.year_from and rec.year_to:
                rec.name = str(rec.year_from) + " - " + str(rec.year_to)
            else:
                rec.name = ''

    @api.constrains('year_from', 'year_to')
    def constrains_year_to(self):
        for rec in self:
            season_id = self.env['lab.season'].search([
                ('year_from', '=', rec.year_from),
                ('year_to', '=', rec.year_to),
                ('id', '!=', rec.id),
            ])
            if season_id:
                raise ValidationError(_("Season Can't be Duplicated"))
            if len(str(rec.year_to)) != 4 or len(str(rec.year_from)) != 4:
                raise ValidationError(_("Please Enter Correct Year Format"))

            if rec.year_from and rec.year_to:
                if not rec.year_from.isdigit() or not rec.year_to.isdigit():
                    raise ValidationError(_("Please Enter Year Format In Digits"))
                if int(rec.year_to) - int(rec.year_from) != 1:
                    raise ValidationError(
                        _("لابد أن تكون السنة فى الحقل <إلى> أكبر من السنة فى الحقل <من> بمقدار سنة واحدة فقط"))

    @api.constrains('current_season')
    def constrains_now(self):
        for rec in self:
            season_ids = self.env['lab.season'].search([('current_season', '=', True)], order=' id ASC')
            if len(season_ids.ids) > 1:
                for l in season_ids:
                    if l != rec:
                        raise ValidationError(_("Current Season  [ %s ] " % l.name))


AVAILABLE_STATUS = [
    ('draft', 'Draft'),
    ('approved', 'Approved'),
    ('close', 'Closed'),
    ('cancel', 'Cancel'),
]


class LabSeasonEstimate(models.Model):
    _name = 'lab.season.estimate'
    _rec_name = 'name'
    _description = 'Lab Season Estimate'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Name")
    season_id = fields.Many2one(comodel_name="lab.season", string="Season", required=True,
                                index=True, help='This is branch to set')
    notes = fields.Text(string="Notes", required=False, )
    state = fields.Selection(AVAILABLE_STATUS, string='state', tracking=True, default=AVAILABLE_STATUS[0][0],
                             required=True)
    estimate_lines = fields.One2many('lab.season.estimate.line', 'estimate_id', string='Season Estimate Lines',
                                     states={'cancel': [('readonly', True)], 'approved': [('readonly', True)]},
                                     copy=True, auto_join=True)

    def action_approved(self):
        self.state = 'approved'

    def action_cancel(self):
        self.state = 'cancel'

    def action_close(self):
        self.state = 'close'

    @api.model
    def create(self, values):
        other_season = self.env['lab.season.estimate'].search([
            ('season_id', '=', values['season_id']),
        ], limit=1)
        if len(other_season.ids) > 0:
            raise ValidationError(
                _("Can not Duplicate Season Estimate , Other in %s" % other_season.name))

        res = super(LabSeasonEstimate, self).create(values)
        res.name = self.env['ir.sequence'].next_by_code('lab.season.estimate') or '/'
        return res

    @api.onchange('season_id')
    def onchange_season(self):
        if self.season_id:
            branches = self.env['res.branch'].search([])
            estimate_lines = []
            for branch in branches:
                estimate_lines.append(self.env['lab.season.estimate.line'].create({
                    'branch_id': branch.id,
                }).id)
            self.estimate_lines = [(6, 0, estimate_lines)]

    def unlink(self):
        for rec in self:
            if rec.state not in ('draft', 'cancel'):
                raise UserError(_('You can not delete a Season Estimate Which Is Not In Draft State.'))
        return super(LabSeasonEstimate, self).unlink()

    @api.constrains('efficiency_ids')
    def constraints_estimate_lines(self):
        for rec in self:
            for line in rec.estimate_lines:
                if line.season_estimate == 0 or line.season_estimate_daily == 0:
                    raise UserError(_('Both Season Estimate And Season Daily Estimate must be set.'))

                if line.season_estimate < line.season_estimate_daily:
                    raise UserError(_('Season Estimate Must Be Larger Than Season Daily Estimate.'))


class LabSeasonEstimateLine(models.Model):
    _name = 'lab.season.estimate.line'
    _rec_name = 'name'
    _description = 'Lab Season Estimate Lines'
    _order = 'estimate_id, sequence, id'

    name = fields.Char("Name")

    sequence = fields.Integer(string='Sequence', default=10)
    estimate_id = fields.Many2one('lab.season.estimate', ondelete='cascade', index=True, copy=False)
    season_id = fields.Many2one(comodel_name="lab.season", related="estimate_id.season_id", string="Season",
                                required=True, index=True)
    branch_id = fields.Many2one("res.branch", string="Branch", required=True, index=True, )
    season_days = fields.Integer(string="Season Days", required=True, )
    sugar_produced_ton = fields.Float(string="Sugar Produced - Ton", required=True, store=True, default=0)
    moulas_qty_ton = fields.Float(string="Moulas Qty\Ton", required=False, default=0, digits=(10, 3))
    season_estimate_daily = fields.Float(string="Season Daily Estimate", required=True, )
    season_estimate = fields.Float(string="Season Estimate", required=True, )
