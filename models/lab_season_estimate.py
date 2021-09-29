# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

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
    season_estimate = fields.Float(string="Season Estimate", required=False, )
    season_estimate_daily = fields.Float(string="Season Daily Estimate", required=False, )
