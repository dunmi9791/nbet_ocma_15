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
    us_cpi = fields.Float(
        string='US Cpi (index)',
        required=False,)
    old_tlf = fields.Float(
        string='Old TLF',
        required=False, )
    new_tlf = fields.Float(
        string='New TLF',
        required=False, )
    us_cpi_cur = fields.Float(
        string='US Cpi (index)',
        required=False,)
    fixed_o_m = fields.Float(
        string='Fixed O & M(n/mw/hr)',
        required=False, )
    fixed_o_m_cur = fields.Float(
        string='Fixed O & M(n/mw/hr)',
        required=False, compute='_fix_om_cur')
    variable_o_m = fields.Float(string='Variable O & M(n/mw/hr)', required=False, )
    variable_o_m_cur = fields.Float(string='Variable O & M(n/mw/hr)', required=False, compute='_variable_om_cur')
    fixed_o_m_dollar = fields.Float(
        string='Fixed O & M($/mw/hr)',
        required=False, )
    variable_o_m_dollar = fields.Float(
        string='Variable O & M($/mw/hr)',
        required=False, )

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
    gas_fuel_price = fields.Float(
        string='Gas Fuel Price($/mmbtu)',
        required=False, )
    vfcr = fields.Float(
        string='VFCR(n/mwh)',
        required=False)
    ncpi = fields.Float(
        string='NCPI(index)',
        required=False)
    us_ppi = fields.Float(
        string='US PPI(Index)',
        required=False, )
    investment_dollar = fields.Float(
        string='Investment($/kw/month)',
        required=False, )
    general_expenses_dollar = fields.Float(
        string='General Expenses($/kw/month)',
        required=False, )
    insurance_dollar = fields.Float(
        string='Insurance($/kw/month)',
        required=False)
    fuel_dollar = fields.Float(
        string='Wholesale charge($/mw/hr)',
        required=False)
    investment_naira = fields.Float(
        string='Investment(n/kw/month)',
        required=False)
    general_expenses_naira = fields.Float(
        string='General Expenses(n/kw/month)',
        required=False)
    insurance_naira = fields.Float(
        string='Insurance(n/kw/month)',
        required=False)
    fuel_naira = fields.Float(
        string='Wholesale charge(n/mw/hr)',
        required=False)
    billing_circle = fields.Many2one(
        comodel_name='billing.cycle',
        string='Billing cycle',
        required=False)

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

    @api.depends('fixed_o_m', 'usd_fx_cbn_cur', 'us_cpi_cur', 'usd_fx_cbn', 'us_cpi')
    def _fix_om_cur(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type == 'hydros':
                    record.fixed_o_m_cur = record.fixed_o_m * (record.usd_fx_cbn_cur / record.usd_fx_cbn) * (record.us_cpi_cur / record.us_cpi)
                elif record.calculation_type in ['successor_gencos', 'fipl', 'fiplo']:
                    record.capacity_charge = record.capital_recovery + record.fixed_o_m
                else:
                    pass

    @api.depends('variable_o_m', 'usd_fx_cbn_cur', 'us_cpi_cur', 'usd_fx_cbn', 'us_cpi')
    def _variable_om_cur(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type == 'hydros':
                    record.variable_o_m_cur = record.variable_o_m * (record.usd_fx_cbn_cur / record.usd_fx_cbn) * (
                                record.us_cpi_cur / record.us_cpi)
                elif record.calculation_type in ['successor_gencos', 'fipl', 'fiplo']:
                    record.capacity_charge = record.capital_recovery + record.fixed_o_m
                else:
                    pass

    @api.depends('capital_recovery', 'usd_fx_cbn_cur', 'usd_fx_cbn',)
    def _capital_recovery_cur(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type == 'hydros':
                    record.capital_recovery_cur = record.capital_recovery * (record.usd_fx_cbn_cur / record.usd_fx_cbn)
                elif record.calculation_type in ['successor_gencos', 'fipl', 'fiplo']:
                    record.capacity_charge = record.capital_recovery + record.fixed_o_m
                else:
                    pass

    @api.depends('variable_o_m_cur' )
    def _energy_charge_cur(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type == 'hydros':
                    record.energy_charge_cur = record.variable_o_m_cur
                elif record.calculation_type in ['successor_gencos', 'fipl', 'fiplo']:
                    record.capacity_charge = record.capital_recovery + record.fixed_o_m
                else:
                    pass

    @api.depends('energy_charge_cur')
    def _energy_charge_tlf(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type == 'hydros':
                    record.energy_charge_tlf = record.energy_charge_cur - record.wholesale_charge_cur * (1-((100-record.old_tlf) / (100-record.new_tlf)))
                elif record.calculation_type in ['successor_gencos', 'fipl', 'fiplo']:
                    record.capacity_charge = record.capital_recovery + record.fixed_o_m
                else:
                    pass

    @api.depends('capital_recovery_cur', 'fixed_o_m_cur')
    def _capacity_charge_cur(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type == 'hydros':
                    record.capacity_charge_cur = record.capital_recovery_cur + record.fixed_o_m_cur
                elif record.calculation_type in ['successor_gencos', 'fipl', 'fiplo']:
                    record.capacity_charge = record.capital_recovery + record.fixed_o_m
                else:
                    pass

    @api.depends('capacity_charge_cur', 'energy_charge_cur')
    def _wholesale_charge_cur(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type == 'hydros':
                    record.wholesale_charge_cur = record.capacity_charge_cur + record.energy_charge_cur
                elif record.calculation_type in ['successor_gencos', 'fipl', 'fiplo']:
                    record.capacity_charge = record.capital_recovery + record.fixed_o_m
                else:
                    pass

