# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date


class RateCoputation(models.TransientModel):
    _name = 'ebs_ocma.rate.computation'
    _description = 'Rate computation '

    calculation_type = fields.Selection([
        ('hydros', 'Hydros'),
        ('successor_gencos', 'Successor Gencos'),
        ('transcorp_ugheli', 'Transcorp Ugheli'),
        ('fipl', 'FIPL (Trans Amadi)'),
        ('fiplo', 'FIPL (Omoku and Rivers)'),
        ('shell', 'SHELL (AFAM VI)'),
        ('agip', 'AGIP (OKPAI)'),
        ('olorunsogo', 'Olorunsogo'),
        ('omotosho', 'Omotosho'),
        ('ibom', 'IBOM POWER'),
        ('nipps', 'NIPPS'),
        ('calabar_nipp', 'CALABAR NIPP'),
        ('gbarain_nipp', 'GBARAIN NIPP'),
        ('mabon', 'MABON (Dadin Kowa Hydro)'),
    ], string='Calculation Type')
    myto_rate_id = fields.Many2one(
        comodel_name='ocma.myto.rate',
        string='Myto_rate_id',
        required=False)

    usd_fx_cbn = fields.Float(
        string='Usd/naira fx CBN',
        required=False,)
    usd_fx_cbn_cur = fields.Float(
        string='Usd/naira fx CBN',
        required=False, )
    us_cpi = fields.Float(string='US Cpi (index)', required=False,)
    us_ppi = fields.Float(string='US ppi (index)', required=False, )
    old_tlf = fields.Float(
        string='Old TLF',
        required=False, )
    new_tlf = fields.Float(
        string='New TLF',
        required=False, )
    us_cpi_cur = fields.Float(string='US Cpi (index)', required=False,)
    us_ppi_cur = fields.Float(string='US ppi (index)', required=False, )
    fixed_o_m = fields.Float(string='Fixed O & M(n/mw/hr)', required=False, )
    fixed_o_m_noncompute = fields.Float(string='Fixed O & M(n/mw/hr)', required=False, )
    fixed_o_m_cur = fields.Float(
        string='Fixed O & M(n/mw/hr)',
        required=False, compute='_fix_om_cur')
    variable_o_m = fields.Float(string='Variable O & M(n/mw/hr)', required=False, )
    variable_o_m_noncompute = fields.Float(string='Variable O & M(n/mw/hr)', required=False, )
    variable_o_m_cur = fields.Float(string='Variable O & M(n/mw/hr)', required=False, compute='_variable_om_cur')
    fixed_o_m_dollar = fields.Float(string='Fixed O & M($/mw/hr)', required=False, )
    fixed_o_m_dollar_cur = fields.Float(string='Fixed O & M($/mw/hr)', required=False, compute='_fixed_om_dollar')
    variable_o_m_dollar = fields.Float(string='Variable O & M($/mw/hr)', required=False, )
    variable_o_m_dollar_cur = fields.Float(string='Variable O & M($/mw/hr)', required=False,
                                           compute='_variable_om_dollar')
    capital_recovery_dollar = fields.Float(string='Capital recovery($/mw/hr)', required=False, )
    capital_recovery_dollar_cur = fields.Float(string='Capital recovery($/mw/hr)', required=False,
                                               compute='_capital_recovery_dollar_cur' )
    capital_recovery = fields.Float(string='Capital recovery(n/mw/hr)', required=False, )
    capital_recovery_cur = fields.Float(string='Capital recovery(n/mw/hr)', required=False,
                                        compute='_capital_recovery_cur')
    energy_charge = fields.Float(string='Energy charge(n/mw/hr)', required=False, )
    energy_charge_cur = fields.Float(string='Energy charge(n/mw/hr)', required=False, compute='_energy_charge_cur')
    energy_charge_tlf = fields.Float(string='Energy charge new TLF(n/mw/hr)', required=False, compute='_energy_charge_tlf')
    capacity_charge = fields.Float(string='Capacity charge(n/mw/hr)', required=False, )
    capacity_charge_cur = fields.Float(string='Capacity charge(n/mw/hr)', required=False, compute='_capacity_charge_cur')
    wholesale_charge = fields.Float(string='Wholesale charge(n/mw/hr)', required=False)
    wholesale_charge_cur = fields.Float(string='Wholesale charge(n/mw/hr)', required=False, compute='_wholesale_charge_cur')
    billing_circle = fields.Many2one(
        comodel_name='billing.cycle',
        string='Billing cycle',
        required=False,)
    gas_fuel_price_dollar = fields.Float(string='Gas Fuel Price($/mmbtu)', required=False, )
    gas_fuel_price_dollar_cur = fields.Float(string='Gas Fuel Price($/mmbtu)', required=False, )
    gas_fuel_price_naira = fields.Float(string='Gas Fuel Price(N/mmbtu)', required=False, compute='_gas_price_naira')
    vfcr = fields.Float(string='VFCR(n/mwh)', required=False)
    vfcr_cur = fields.Float(string='VFCR(n/mwh)', required=False, compute='_vfcr_cur')
    vfcr_dollar = fields.Float(string='VFCR(n/mwh)', required=False)
    vfcr_dollar_cur = fields.Float(string='VFCR(n/mwh)', required=False, compute='_vfcr_cur_dollar')
    ncpi = fields.Float(string='NCPI(index)', required=False)
    ncpi_cur = fields.Float(string='NCPI(index)', required=False)
    us_ppi = fields.Float(
        string='US PPI(Index)',
        required=False, )
    investment_dollar = fields.Float(string='Investment($/kw/month)', required=False, )
    investment_dollar_cur = fields.Float(string='Investment($/kw/month)', required=False,
                                         compute='_investment_dollar_cur')
    general_expenses_dollar = fields.Float(string='General Expenses($/kw/month)', required=False, )
    general_expenses_dollar_cur = fields.Float(string='General Expenses($/kw/month)', required=False,
                                               compute='_expenses_dollar_cur')
    insurance_dollar = fields.Float(string='Insurance($/kw/month)', required=False,)
    insurance_dollar_cur = fields.Float(string='Insurance($/kw/month)', required=False, compute='_insurance_dollar_cur')
    fuel_dollar = fields.Float(string='Wholesale charge($/mw/hr)', required=False)
    fuel_dollar_cur = fields.Float(string='Wholesale charge($/mw/hr)', required=False, compute='_fuel_dollar_cur')
    investment_naira = fields.Float(string='Investment(n/kw/month)', required=False)
    general_expenses_naira = fields.Float(string='General Expenses(n/kw/month)', required=False)
    insurance_naira = fields.Float(string='Insurance(n/kw/month)', required=False)
    fuel_naira = fields.Float(string='Wholesale charge(n/mw/hr)', required=False)
    fuel_naira_cur = fields.Float(string='Wholesale charge(n/mw/hr)', required=False)
    tax_cost_cur = fields.Float(string='Tax Cost(n/mw/hr)', required=False)
    tax_cost = fields.Float(string='Tax cost(n/mw/hr)', required=False)
    capital_cost = fields.Float(string='Capital cost(n/mw/hr)', required=False)
    capital_cost_cur = fields.Float(string='Capital cost(n/mw/hr)', required=False)
    startup_dollar = fields.Float(string='Startup dollar', required=False)
    startup_dollar_cur = fields.Float(string='Startup dollar', required=False, compute='_startup_dollar_cur')
    startup_naira = fields.Float(string='Startup Naira', required=False, compute='_startup_naira')
    fuel_cost_dollar = fields.Float(string='Fuel cost dollar', required=False, compute='_fuel_cost_cur')
    hhv_to_lhv = fields.Float(string='HHV to LHV Ratio', required=False)
    efficiency = fields.Float(string='Efficiency %', required=False)

    def fix_om_cur(self):
        for record in self:
            rates = self.env['hydro.rates'].create({
                'rate_id': record.myto_rate_id.id,
                'fixed_o_m': record.fixed_o_m_cur,
                'usd_fx_cbn': record.usd_fx_cbn_cur,
                'us_cpi': record.us_cpi_cur,
                'new_tlf': record.new_tlf,
                'variable_o_m': record.variable_o_m_cur,
                'capital_recovery': record.capital_recovery_cur,
                'energy_charge': record.energy_charge_cur,
                'energy_charge_tlf': record.energy_charge_tlf,
                'capacity_charge': record.capacity_charge_cur,
                'wholesale_charge': record.wholesale_charge_cur,
                'billing_circle': record.billing_circle.id,
                })

    def _vfcr_cur(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type in ['successor_gencos', 'transcorp_ugheli' , 'fipl', 'fiplo', 'olorunsogo', 'omotosho']:
                    record.vfcr_cur = record.vfcr * (record.gas_fuel_price_dollar_cur / record.gas_fuel_price_dollar) * \
                                      (record.usd_fx_cbn_cur / record.usd_fx_cbn)
                elif record.calculation_type in ['shell']:
                    record.vfcr_cur = record.vfcr_dollar_cur * record.usd_fx_cbn_cur
                else:
                    pass

    def _vfcr_cur_dollar(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type in ['shell']:
                    record.vfcr_dollar_cur = record.vfcr_dollar * record.us_ppi_cur / record.us_ppi

    def _investment_dollar_cur(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type in ['agip']:
                    record.investment_dollar_cur = record.investment_dollar * record.us_ppi_cur / record.us_ppi

    def _insurance_dollar_cur(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type in ['agip']:
                    record.insurance_dollar_cur = record.insurance_dollar * record.us_ppi_cur / record.us_ppi

    def _expenses_dollar_cur(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type in ['agip']:
                    record.general_expenses_dollar_cur = record.general_expenses_dollar

    def _fuel_dollar_cur(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type in ['agip']:
                    record.fuel_dollar_cur = record.fuel_dollar * record.us_ppi_cur / record.us_ppi

    def _fixed_om_dollar(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type in ['shell']:
                    record.fixed_o_m_dollar_cur = (record.fixed_o_m_dollar * 0.67) + (0.33 * record.fixed_o_m_dollar) * (record.us_ppi_cur/record.us_ppi)
                elif record.calculation_type in ['agip']:
                    record.fixed_o_m_dollar_cur = record.fixed_o_m_dollar * record.us_ppi_cur / record.us_ppi
                else:
                    pass

    def _variable_om_dollar(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type in ['shell', 'agip']:
                    record.variable_o_m_dollar_cur = record.variable_o_m_dollar * record.us_ppi_cur/record.us_ppi
                else:
                    pass

    def _startup_dollar_cur(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type in ['shell', ]:
                    record.startup_dollar_cur = record.startup_dollar * record.us_ppi_cur/record.us_ppi
                else:
                    pass

    def _startup_naira(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type in ['shell', ]:
                    record.startup_naira = record.startup_dollar_cur * record.usd_fx_cbn_cur
                else:
                    pass

    def _fuel_cost_cur(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type in ['ibom']:
                    record.fuel_cost_dollar = record.gas_fuel_price_dollar_cur * record.hhv_to_lhv * 3.412 / record.efficiency
                else:
                    pass

    def _gas_price_naira(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type in ['ibom']:
                    record.gas_fuel_price_naira = record.gas_fuel_price_dollar_cur * record.usd_fx_cbn_cur
                else:
                    pass

    @api.depends('fixed_o_m', 'usd_fx_cbn_cur', 'us_cpi_cur', 'usd_fx_cbn', 'us_cpi')
    def _fix_om_cur(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type in ['hydros','successor_gencos','transcorp_ugheli']:
                    record.fixed_o_m_cur = record.fixed_o_m * (record.usd_fx_cbn_cur / record.usd_fx_cbn) * (record.us_cpi_cur / record.us_cpi)
                elif record.calculation_type in ['fipl', 'fiplo']:
                    record.fixed_o_m_cur = record.fixed_o_m * (record.ncpi_cur/record.ncpi)
                elif record.calculation_type in ['shell', 'agip']:
                    record.fixed_o_m_cur = record.fixed_o_m_dollar_cur * record.usd_fx_cbn_cur
                elif record.calculation_type in ['olorunsogo', 'omotosho']:
                    record.fixed_o_m_cur = record.fixed_o_m * (0.85 * (record.us_cpi_cur/record.us_cpi) + (1-0.85) *
                                                               (record.ncpi_cur/record.ncpi)) + (0.85 * record.fixed_o_m) *\
                                           ((record.usd_fx_cbn_cur / record.usd_fx_cbn) - 1) * (record.us_cpi_cur/record.us_cpi)
                elif record.calculation_type in ['mabon']:
                    record.fixed_o_m_cur = record.fixed_o_m * (0.23 + 0.77 * (record.us_cpi_cur/record.us_cpi) *
                                                               (record.usd_fx_cbn_cur/record.usd_fx_cbn))
                elif record.calculation_type in ['ibom', 'nipps', 'calabar_nipp', 'gbarain_nipp']:
                    record.fixed_o_m_cur = record.fixed_o_m_noncompute

                else:
                    pass

    @api.depends('variable_o_m', 'usd_fx_cbn_cur', 'us_cpi_cur', 'usd_fx_cbn', 'us_cpi')
    def _variable_om_cur(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type in ['hydros', 'successor_gencos', 'transcorp_ugheli']:
                    record.variable_o_m_cur = record.variable_o_m * (record.usd_fx_cbn_cur / record.usd_fx_cbn) * (
                                record.us_cpi_cur / record.us_cpi)
                elif record.calculation_type in ['fipl', 'fiplo']:
                    record.variable_o_m_cur = record.variable_o_m * (record.ncpi_cur/record.ncpi)
                elif record.calculation_type in ['shell']:
                    record.variable_o_m_cur = record.variable_o_m_dollar_cur * record.usd_fx_cbn_cur
                elif record.calculation_type in ['agip']:
                    record.variable_o_m_cur = record.variable_o_m_dollar_cur * record.usd_fx_cbn_cur * 1000
                elif record.calculation_type in ['olorunsogo', 'omotosho']:
                    record.variable_o_m_cur = record.variable_o_m * (0.85 * (record.us_cpi_cur/record.us_cpi)
                                                                     + (1 - 0.85) * (record.ncpi_cur/record.ncpi)) + \
                                              (0.85 * record.variable_o_m) * ((record.usd_fx_cbn_cur/record.usd_fx_cbn)
                                                                              - 1) * record.us_cpi_cur/record.us_cpi
                elif record.calculation_type in ['mabon']:
                    record.variable_o_m_cur = record.variable_o_m
                elif record.calculation_type in ['ibom', 'nipps', 'calabar_nipp', 'gbarain_nipp']:
                    record.variable_o_m_cur = record.variable_o_m_noncompute

                else:
                    pass

    def _capital_recovery_dollar_cur(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type in ['shell', ]:
                    record.capital_recovery_dollar_cur = (record.capital_recovery_dollar * 0.67) + \
                                                         (record.capital_recovery_dollar * 0.33) * (record.us_ppi_cur / record.us_ppi)
                elif record.calculation_type in ['shell']:
                    record.capital_recovery_cur = record.capital_recovery_dollar_cur * record.usd_fx_cbn_cur
                elif record.calculation_type in ['mabon']:
                    record.capital_recovery_cur = record.capital_recovery * (0.25 + 0.75 * (record.usd_fx_cbn_cur/record.usd_fx_cbn))
                else:
                    pass

    @api.depends('capital_recovery', 'usd_fx_cbn_cur', 'usd_fx_cbn',)
    def _capital_recovery_cur(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type in ['hydros', 'successor_gencos', 'transcorp_ugheli', 'fipl', 'fiplo', 'olorunsogo', 'omotosho' ]:
                    record.capital_recovery_cur = record.capital_recovery * (record.usd_fx_cbn_cur / record.usd_fx_cbn)
                elif record.calculation_type in ['shell']:
                    record.capital_recovery_cur = record.capital_recovery_dollar_cur * record.usd_fx_cbn_cur
                elif record.calculation_type in ['mabon']:
                    record.capital_recovery_cur = record.capital_recovery * (0.25 + 0.75 * (record.usd_fx_cbn_cur/record.usd_fx_cbn))
                else:
                    pass

    @api.depends('variable_o_m_cur' )
    def _energy_charge_cur(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type == 'hydros':
                    record.energy_charge_cur = record.variable_o_m_cur
                elif record.calculation_type in ['successor_gencos', 'fipl', 'transcorp_ugheli', 'fiplo', 'shell', 'olorunsogo', 'omotosho']:
                    record.energy_charge_cur = record.vfcr_cur + record.variable_o_m_cur
                elif record.calculation_type in ['agip']:
                    record.energy_charge_cur = record.fuel_naira_cur + record.variable_o_m_cur
                elif record.calculation_type in ['ibom', 'nipps', 'calabar_nipp', 'gbarain_nipp' ]:
                    record.energy_charge_cur = record.fuel_naira_cur + record.variable_o_m_cur + \
                                               record.trans_loss_cost_cur + (1/3 * record.tax_cost_cur)
                elif record.calculation_type in ['mabon']:
                    record.energy_charge_cur = record.energy_charge
                else:
                    pass

    @api.depends('energy_charge_cur')
    def _energy_charge_tlf(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type == 'hydros':
                    record.energy_charge_tlf = record.energy_charge_cur - record.wholesale_charge_cur * (1-((100-record.old_tlf) / (100-record.new_tlf)))
                elif record.calculation_type in ['successor_gencos', 'fipl', 'fiplo']:
                    record.capacity_charge = record.capital_recovery_cur + record.fixed_o_m_cur
                else:
                    pass

    @api.depends('capital_recovery_cur', 'fixed_o_m_cur')
    def _capacity_charge_cur(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type in ['hydros', 'successor_gencos', 'transcorp_ugheli', 'fipl', 'fiplo', "shell", 'olorunsogo', 'omotosho', 'mabon']:
                    record.capacity_charge_cur = record.capital_recovery_cur + record.fixed_o_m_cur
                elif record.calculation_type in ['agip']:
                    record.capacity_charge_cur = record.investment_naira + record.fixed_o_m_cur + record.insurance_naira \
                                                 + record.general_expenses_naira
                elif record.calculation_type in ['ibom', 'nipps', 'calabar_nipp', 'gbarain_nipp']:
                    record.capacity_charge_cur = record.fixed_o_m_cur + record.capital_cost_cur + (0.666 * record.tax_cost_cur)
                else:
                    pass

    @api.depends('capacity_charge_cur', 'energy_charge_cur')
    def _wholesale_charge_cur(self):
        for record in self:
            if record.calculation_type:
                record.wholesale_charge_cur = record.capacity_charge_cur + record.energy_charge_cur




