# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models

AVAILABLE_STATUS = [
    ('draft', 'Draft'),
    ('branchApproved', 'Branch Approved'),
    ('deptApproved', 'Dept. Approved'),
    ('approved', 'Approved'),
    ('cancel', 'Cancel'),
]


class LabSugarAnalysisReport(models.Model):
    _name = 'lab.sugar.analysis.report'
    _description = 'Lab Sugar Analysis Report'
    _auto = False

    name = fields.Char('Description')
    branch_id = fields.Many2one(comodel_name="res.branch", string="Branch",)
    entry_id = fields.Integer(string="Entry Number", required=True, )
    entry_date = fields.Date(string="Transaction Date", required=True, default=fields.Date.context_today, copy=False)
    state = fields.Selection(AVAILABLE_STATUS, string='state')
    season_id = fields.Many2one(comodel_name="lab.season", string="Season", index=True, help='This is branch to set')
    can_crashed_ton = fields.Float(string="Can Crashed / Ton", required=True, )
    can_sweetness = fields.Float(string="Sweetness", required=False, )
    juice_mix_purity = fields.Float(string="Juice mixed Purity", required=False, )
    juice_main_val = fields.Float(string="Juice Main Val", required=False, )
    juice_lab_val = fields.Float(string="Juice Lab Val", required=False, )
    first_squeeze_extract = fields.Float(string="First Squeeze Extract", required=False, )
    berx_juice_mix = fields.Float(string="Berx Juice Mix", required=False, )
    extract_125_fiber = fields.Float(string="Extract 12.5 Fiber", required=False, )
    sugar_a_ton = fields.Float(string="Sugar A \ Ton", required=False, )
    sugar_brown_ton = fields.Float(string="Sugar Brown \ Ton", required=False, )
    sugar_b_ton = fields.Float(string="Sugar B \ Ton", required=False, )
    sugar_produced_ton = fields.Float(string="Sugar Produced - Ton", )
    can_sugar_rate = fields.Float(string="Can Sugar Rate", )
    sugar_a_colour = fields.Float(string="Sugar A \ Colour", required=False, )
    sugar_b_colour = fields.Float(string="Sugar B \ Colour", required=False, )
    moulas_qty_ton = fields.Float(string="Moulas Qty\Ton", required=False, )
    moulas_brix = fields.Float(string="Moulas Brix", required=False, )
    moulas_purity = fields.Float(string="Moulas Purity", required=False, )
    lose_moulas = fields.Float(string="Moulas Lose", required=False, )
    lose_bagas = fields.Float(string="Bagas Lose", required=False, )
    lose_mud = fields.Float(string="Mud Lose", required=False, )
    lose_total = fields.Float(string="Total Lose", required=False, )
    water_raw_fiber = fields.Float(string="Water Raw Fiber", required=False, )
    bagas_humidity = fields.Float(string="Bagas Humidity", required=False, )
    brix_sherbat = fields.Float(string="Brix Sherbat", required=False, )
    juice_clear_lees = fields.Float(string="Juice Clear Lees", required=False, )
    steam_amount = fields.Float(string="Steam Amount", required=False, )
    fuel_coal_qty = fields.Float(string="Fuel Coal Qty", required=False, )
    mazout_used = fields.Float(string="Mazout Used", required=False, )
    gas_used = fields.Float(string="Gas Used", required=False, )
    steam_avr = fields.Float(string="Steam Per Ton")

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
                    min(l.id) as id,
                    l.name as name,
                    l.branch_id as branch_id,
                    l.entry_id as entry_id,
                    l.entry_date as entry_date,
                    l.state as state,
                    l.season_id as season_id,
                    sum(l.can_crashed_ton) as  can_crashed_ton,
                    sum(l.can_sweetness) as can_sweetness,
                    sum(l.juice_mix_purity) as juice_mix_purity,
                    sum(l.juice_main_val) as juice_main_val,
                    sum(l.juice_lab_val) as juice_lab_val,
                    sum(l.first_squeeze_extract) as first_squeeze_extract,
                    sum(l.berx_juice_mix) as    berx_juice_mix,
                    sum(l.extract_125_fiber) as extract_125_fiber,
                    sum(l.sugar_a_ton) as   sugar_a_ton,
                    sum(l.sugar_brown_ton) as   sugar_brown_ton,
                    sum(l.sugar_b_ton) as   sugar_b_ton,
                    sum(l.sugar_produced_ton) as    sugar_produced_ton,
                    sum(l.can_sugar_rate) as   can_sugar_rate,
                    sum(l.sugar_a_colour) as   sugar_a_colour,
                    sum(l.sugar_b_colour) as   sugar_b_colour,
                    sum(l.moulas_qty_ton) as  moulas_qty_ton,
                    sum(l.moulas_brix) as   moulas_brix,
                    sum(l.moulas_purity) as moulas_purity,
                    sum(l.lose_moulas) as   lose_moulas,
                    sum(l.lose_bagas) as    lose_bagas,
                    sum(l.lose_mud) as  lose_mud,
                    sum(l.lose_total) as  lose_total,
                    sum(l.water_raw_fiber) as   water_raw_fiber,
                    sum(l.bagas_humidity) as    bagas_humidity,
                    sum(l.brix_sherbat) as  brix_sherbat,
                    sum(l.juice_clear_lees) as  juice_clear_lees,
                    sum(l.steam_amount) as  steam_amount,
                    sum(l.fuel_coal_qty) as fuel_coal_qty,
                    sum(l.mazout_used) as   mazout_used,
                    sum(l.gas_used) as   gas_used,
                    sum(l.steam_avr) as   steam_avr
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
                    l.entry_id,
                    l.entry_date,
                    l.state,
                    l.season_id %s
                """ % groupby

        return '%s (SELECT %s FROM %s WHERE l.id IS NOT NULL GROUP BY %s)' % (with_, select_, from_, groupby_)

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))

    class LabSugarAnalysisReport(models.AbstractModel):
        _name = 'lab.sugar.analysis.report'
        _description = 'Lab Sugar Analysis Report'

        def _get_report_values(self, docids, data=None):
            docs = self.env['sale.net'].browse(docids)
            return {
                'doc_ids': docs.ids,
                'doc_model': 'lab.sugar.analysis.report',
                'docs': docs,
                'proforma': True
            }
