# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class LabSugarAnalysisNetReport(models.Model):
    _name = 'lab.sugar.analysis.net.report'
    _description = 'Lab Sugar Analysis Net Report'
    _auto = False

    name = fields.Char('Description')
    branch_id = fields.Many2one(comodel_name="res.branch", string="Branch",)
    entry_date = fields.Date(string="Transaction Date", required=True, default=fields.Date.context_today, copy=False)
    season_id = fields.Many2one(comodel_name="lab.season", string="Season", index=True, help='This is branch to set')
    can_crashed_ton = fields.Float(string="Can Crashed / Ton", required=True, )
    can_sweetness = fields.Float(string="Sweetness", required=False, )
    sugar_a_ton = fields.Float(string="Sugar A \ Ton", required=False, )
    sugar_brown_ton = fields.Float(string="Sugar Brown \ Ton", required=False, )
    sugar_b_ton = fields.Float(string="Sugar B \ Ton", required=False, )
    sugar_produced_ton = fields.Float(string="Sugar Produced - Ton", )
    can_sugar_rate = fields.Float(string="Can Sugar Rate", )
    sugar_a_colour = fields.Float(string="Sugar A \ Colour", required=False, )
    sugar_b_colour = fields.Float(string="Sugar B \ Colour", required=False, )
    moulas_qty_ton = fields.Float(string="Moulas Qty\Ton", required=False, )
    fuel_coal_qty = fields.Float(string="Fuel Coal Qty", required=False, )
    mazout_used = fields.Float(string="Mazout Used", required=False, )
    gas_used = fields.Float(string="Gas Used", required=False, )

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
                    min(l.id) as id,
                    l.name as name,
                    l.branch_id as branch_id,
                    l.entry_date as entry_date,
                    l.season_id as season_id,
                    sum(l.can_crashed_ton) as  can_crashed_ton,
                    sum(l.can_sweetness) as can_sweetness,
                    sum(l.sugar_a_ton) as   sugar_a_ton,
                    sum(l.sugar_brown_ton) as   sugar_brown_ton,
                    sum(l.sugar_b_ton) as   sugar_b_ton,
                    sum(l.sugar_produced_ton) as    sugar_produced_ton,
                    sum(l.can_sugar_rate) as   can_sugar_rate,
                    sum(l.sugar_a_colour) as   sugar_a_colour,
                    sum(l.sugar_b_colour) as   sugar_b_colour,
                    sum(l.moulas_qty_ton) as  moulas_qty_ton,
                    sum(l.fuel_coal_qty) as fuel_coal_qty,
                    sum(l.mazout_used) as   mazout_used,
                    sum(l.gas_used) as   gas_used
                """

        for field in fields.values():
            select_ += field

        from_ = """
                   lab_sugar_analysis l
                    join res_branch b on (l.branch_id=b.id)
                    join lab_season s on(l.season_id = s.id)
                    %s
                """ % from_clause

        groupby_ = """
                    l.name,
                    l.branch_id,
                    l.entry_date,
                    l.season_id %s
                """ % groupby

        return '%s (SELECT %s FROM %s WHERE l.id IS NOT NULL GROUP BY %s)' % (with_, select_, from_, groupby_)

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))

    class SaleNetReportProforma(models.AbstractModel):
        _name = 'lab.sugar.analysis.report_saleproforma'
        _description = 'Lab Sugar Analysis Net Report'

        def _get_report_values(self, docids, data=None):
            docs = self.env['lab.sugar.analysis.net.report'].browse(docids)
            return {
                'doc_ids': docs.ids,
                'doc_model': 'lab.sugar.analysis.net.report',
                'docs': docs,
                'proforma': True
            }
