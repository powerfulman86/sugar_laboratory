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
    _rec_name = 'entry_date'
    _order = 'entry_date desc'

    name = fields.Char('Description')
    branch_id = fields.Many2one(comodel_name="res.branch", string="Branch", )
    entry_id = fields.Integer(string="Entry Number", group_operator='')
    entry_date = fields.Date(string="Transaction Date", group_operator='')
    entry_month = fields.Integer(string="Month", group_operator='')
    entry_day = fields.Integer(string="Day", group_operator='')
    state = fields.Selection(AVAILABLE_STATUS, string='state')
    season_id = fields.Many2one(comodel_name="lab.season", string="Season")
    season_estimate_daily = fields.Float(string="Season Daily Estimate",)
    can_crashed_ton = fields.Float(string="Can Crashed / Ton", )
    can_sweetness = fields.Float(string="Sweetness", group_operator="avg")
    juice_mix_purity = fields.Float(string="Juice mixed Purity", group_operator="avg")
    juice_main_val = fields.Float(string="Juice Main Val", group_operator="avg")
    juice_lab_val = fields.Float(string="Juice Lab Val", group_operator="avg")
    first_squeeze_extract = fields.Float(string="First Squeeze Extract", group_operator="avg")
    berx_juice_mix = fields.Float(string="Berx Juice Mix", group_operator="avg")
    extract_125_fiber = fields.Float(string="Extract 12.5 Fiber", group_operator="avg")
    sugar_a_ton = fields.Float(string="Sugar A \ Ton", )
    sugar_brown_ton = fields.Float(string="Sugar Brown \ Ton", )
    sugar_b_ton = fields.Float(string="Sugar B \ Ton", )
    sugar_produced_ton = fields.Float(string="Sugar Produced - Ton", )
    can_sugar_rate = fields.Float(string="Can Sugar Rate", group_operator="avg")
    sugar_a_colour = fields.Float(string="Sugar A \ Colour", group_operator="avg")
    sugar_b_colour = fields.Float(string="Sugar B \ Colour", group_operator="avg")
    moulas_qty_ton = fields.Float(string="Moulas Qty\Ton", )
    moulas_brix = fields.Float(string="Moulas Brix", )
    moulas_purity = fields.Float(string="Moulas Purity", )
    lose_moulas = fields.Float(string="Moulas Lose", )
    lose_bagas = fields.Float(string="Bagas Lose", )
    lose_mud = fields.Float(string="Mud Lose", )
    lose_total = fields.Float(string="Total Lose", )
    water_raw_fiber = fields.Float(string="Water Raw Fiber", group_operator="avg")
    bagas_humidity = fields.Float(string="Bagas Humidity", group_operator="avg")
    brix_sherbat = fields.Float(string="Brix Sherbat", )
    juice_clear_lees = fields.Float(string="Juice Clear Lees", group_operator="avg")
    steam_amount = fields.Float(string="Steam Amount", )
    fuel_coal_qty = fields.Float(string="Fuel Coal Qty", )
    mazout_used = fields.Float(string="Mazout Used", )
    gas_used = fields.Float(string="Gas Used", )
    steam_avr = fields.Float(string="Steam Per Ton", group_operator="avg")
    down_time = fields.Integer(string="Down Time", )

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
                    min(l.id) as id,
                    l.name as name,
                    l.branch_id as branch_id,
                    l.entry_id as entry_id,
                    l.entry_date as entry_date,
                    l.entry_month as entry_month,
                    l.entry_day as entry_day,
                    l.state as state,
                    l.season_id as season_id,
                    est.season_estimate_daily as season_estimate_daily,
                    l.down_time as down_time,
                    l.can_crashed_ton as  can_crashed_ton,
                    l.can_sweetness as can_sweetness,
                    l.juice_mix_purity as juice_mix_purity,
                    l.juice_main_val as juice_main_val,
                    l.juice_lab_val as juice_lab_val,
                    l.first_squeeze_extract as first_squeeze_extract,
                    l.berx_juice_mix as    berx_juice_mix,
                    l.extract_125_fiber as extract_125_fiber,
                    l.sugar_a_ton as   sugar_a_ton,
                    l.sugar_brown_ton as   sugar_brown_ton,
                    l.sugar_b_ton as   sugar_b_ton,
                    l.sugar_produced_ton as    sugar_produced_ton,
                    l.can_sugar_rate as   can_sugar_rate,
                    l.sugar_a_colour as   sugar_a_colour,
                    l.sugar_b_colour as   sugar_b_colour,
                    l.moulas_qty_ton as  moulas_qty_ton,
                    l.moulas_brix as   moulas_brix,
                    l.moulas_purity as moulas_purity,
                    l.lose_moulas as   lose_moulas,
                    l.lose_bagas as    lose_bagas,
                    l.lose_mud as  lose_mud,
                    l.lose_total as  lose_total,
                    l.water_raw_fiber as   water_raw_fiber,
                    l.bagas_humidity as    bagas_humidity,
                    l.brix_sherbat as  brix_sherbat,
                    l.juice_clear_lees as  juice_clear_lees,
                    l.steam_amount as  steam_amount,
                    l.fuel_coal_qty as fuel_coal_qty,
                    l.mazout_used as   mazout_used,
                    l.gas_used as   gas_used,
                    l.steam_avr as   steam_avr
                """

        for field in fields.values():
            select_ += field

        from_ = """
                   lab_sugar_analysis l
                    join res_branch b on (l.branch_id=b.id)
                    join lab_season s on(l.season_id = s.id)
                    left outer join lab_season_estimate_line est on(est.branch_id = l.branch_id and est.season_id = l.season_id)
                    %s
                """ % from_clause

        groupby_ = """
                    l.name,
                    l.branch_id,
                    l.entry_id,
                    l.entry_date,
                    l.entry_month,
                    l.entry_day,
                    l.state,
                    l.season_id,
                    est.season_estimate_daily,
                    l.down_time,
                    l.can_crashed_ton,
                    l.can_sweetness,
                    l.juice_mix_purity,
                    l.juice_main_val,
                    l.juice_lab_val,
                    l.first_squeeze_extract,
                    l.berx_juice_mix,
                    l.extract_125_fiber,
                    l.sugar_a_ton,
                    l.sugar_brown_ton,
                    l.sugar_b_ton,
                    l.sugar_produced_ton,
                    l.can_sugar_rate,
                    l.sugar_a_colour,
                    l.sugar_b_colour,
                    l.moulas_qty_ton,
                    l.moulas_brix,
                    l.moulas_purity,
                    l.lose_moulas,
                    l.lose_bagas,
                    l.lose_mud,
                    l.lose_total,
                    l.water_raw_fiber,
                    l.bagas_humidity,
                    l.brix_sherbat,
                    l.juice_clear_lees,
                    l.steam_amount,
                    l.fuel_coal_qty,
                    l.mazout_used,
                    l.gas_used,
                    l.steam_avr %s
                """ % groupby

        return '%s (SELECT %s FROM %s WHERE l.id IS NOT NULL GROUP BY %s)' % (with_, select_, from_, groupby_)

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))
