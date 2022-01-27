# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class LabMalfunctionReport(models.Model):
    _name = 'lab.malfunction.report'
    _description = 'Sugar Daily Malfunction Report'
    _auto = False
    _rec_name = 'entry_date'

    name = fields.Char()
    analysis_id = fields.Many2one(comodel_name="lab.sugar.analysis", string="Malfunction Analysis", )
    entry_id = fields.Integer(string="Entry Number",)
    entry_date = fields.Date(string="Transaction Date",)
    season_id = fields.Many2one(comodel_name="lab.season", string="Season", )
    branch_id = fields.Many2one(comodel_name="res.branch", string="Branch", )
    line_id = fields.Many2one(comodel_name="res.branch.sugar.line", string="Sugar Line",)
    malfunction_id = fields.Many2one(comodel_name="lab.malfunctions", string="Malfunction", )
    down_time = fields.Integer(string="Down Time/m", default='0')
    down_time_hour = fields.Integer(string="Down Time/h",default='0')
    down_time_day = fields.Integer(string="Down Time/d", default='0')
    notes = fields.Text('Notes')

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
                       min(l.id) as id,
                       l.name as name,
                       l.entry_id as entry_id,
                       l.entry_date as entry_date,
                       l.branch_id as branch_id,
                       l.season_id as season_id,
                       l.line_id as line_id,
                       l.malfunction_id as malfunction_id,
                       l.down_time as down_time,
                       (l.down_time / 60) as down_time_hour,
                       (l.down_time / (60 * 24)) as down_time_day,
                       l.notes as notes
                   """

        for field in fields.values():
            select_ += field

        from_ = """
                      lab_malfunctions_branch l
                       join res_branch b on (l.branch_id=b.id)
                       join lab_season s on(l.season_id = s.id)
                       join res_branch_sugar_line li on (l.line_id = li.id) 
                       join lab_malfunctions lm on (l.malfunction_id = lm.id)
                       %s
                   """ % from_clause

        groupby_ = """
                       l.name,
                       l.entry_id,
                       l.entry_date,
                       l.branch_id,
                       l.season_id,
                       l.line_id,
                       l.malfunction_id,
                       l.down_time,
                        l.notes %s
                   """ % groupby

        return '%s (SELECT %s FROM %s WHERE l.id IS NOT NULL GROUP BY %s)' % (with_, select_, from_, groupby_)

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))