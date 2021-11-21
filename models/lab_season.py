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
