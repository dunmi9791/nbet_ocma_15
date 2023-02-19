from odoo import models, fields, api, _
from calendar import monthrange
from datetime import date

from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import UserError


class MytoRates(models.Model):
    _name = 'ocma.myto.rate'
    _description = 'Myto Rate'
    _order = 'create_date desc'

    name = fields.Char('Description')
    approved_by = fields.Many2one(comodel_name="hr.employee", string="Approved by")
    line_ids = fields.One2many(comodel_name="hydro.rates", inverse_name="rate_id", string="Rates")
    state = fields.Selection([
        ('draft', 'New'),
        ('open', 'To Approve'),
        ('approve', 'Approved'),
        ('reject', 'Rejected'),
        ('cancel', 'Cancelled'),
    ], string='state', default="draft", readonly=True)
    active = fields.Boolean(string='Active', default=True)
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

    usd_fx_cbn = fields.Float(
        string='Usd/naira fx CBN',
        required=False)
    us_cpi = fields.Float(
        string='US Cpi (index)',
        required=False)
    old_tlf = fields.Float(
        string='Old TLF',
        required=False)
    fixed_o_m = fields.Float(
        string='Fixed O & M(n/mw/hr)',
        required=False)
    variable_o_m = fields.Float(
        string='Variable O & M(n/mw/hr)',
        required=False)
    fixed_o_m_dollar = fields.Float(
        string='Fixed O & M($/mw/hr)',
        required=False)
    variable_o_m_dollar = fields.Float(
        string='Variable O & M($/mw/hr)',
        required=False)

    capital_recovery = fields.Float(
        string='Capital recovery(n/mw/hr)',
        required=False)
    energy_charge = fields.Float(string='Energy charge(n/mw/hr)', required=False, compute="_energy_charge")
    capacity_charge = fields.Float(string='Capacity charge(n/mw/hr)', required=False, compute="_capacity_charge")
    wholesale_charge = fields.Float(string='Wholesale charge(n/mw/hr)', required=False, compute="_wholesale_charge")
    billing_circle = fields.Many2one(
        comodel_name='billing.cycle',
        string='Billing cycle',
        required=False)
    gas_fuel_price = fields.Float(
        string='Gas Fuel Price($/mmbtu)',
        required=False)
    vfcr = fields.Float(
        string='VFCR(n/mwh)',
        required=False)
    ncpi = fields.Float(
        string='NCPI(index)',
        required=False)
    us_ppi = fields.Float(
        string='US PPI(Index)',
        required=False)
    investment_dollar = fields.Float(
        string='Investment($/kw/month)',
        required=False)
    general_expenses_dollar = fields.Float(
        string='General Expenses($/kw/month)',
        required=False)
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

    def action_submit(self):
        self.state = 'open'

    def action_approve(self):
        self.state = 'approve'

    def action_reject(self):
        self.state = 'reject'

    def action_cancel(self):
        self.state = 'cancel'

    # @api.depends('')
    def _capacity_charge(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type == 'hydros':
                    record.capacity_charge = record.capital_recovery + record.fixed_o_m
                if record.calculation_type == 'successor_gencos':
                    record.capacity_charge = record.capital_recovery + record.fixed_o_m
                if record.calculation_type == 'fipl':
                    record.capacity_charge = record.capital_recovery + record.fixed_o_m
                if record.calculation_type == 'fiplo':
                    record.capacity_charge = record.capital_recovery + record.fixed_o_m
                else:
                    pass

    def _energy_charge(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type == 'hydros':
                    record.energy_charge = record.variable_o_m
                if record.calculation_type == 'successor_gencos':
                    record.energy_charge = record.vfcr + record.variable_o_m
                if record.calculation_type == 'fipl':
                    record.energy_charge = record.vfcr + record.variable_o_m
                if record.calculation_type == 'fiplo':
                    record.energy_charge = record.vfcr + record.variable_o_m
                else:
                    pass

    def _wholesale_charge(self):
        for record in self:
            if record.calculation_type:
                if record.calculation_type == 'hydros':
                    record.wholesale_charge = record.capacity_charge + record.energy_charge
                if record.calculation_type == 'successor_gencos':
                    record.wholesale_charge = record.capacity_charge + record.energy_charge
                if record.calculation_type == 'fipl':
                    record.wholesale_charge = record.capacity_charge + record.energy_charge
                if record.calculation_type == 'fiplo':
                    record.wholesale_charge = record.capacity_charge + record.energy_charge
                else:
                    pass


class HydroRates(models.Model):
    _name = 'hydro.rates'
    _description = 'Hydro Rates'

    name = fields.Char()
    # rates_category = fields.Many2one(
    #     comodel_name='rate.category',
    #     string='Rates category',
    #     required=False)
    usd_fx_cbn = fields.Float(
        string='Usd/naira fx CBN',
        required=False)
    us_cpi = fields.Float(
        string='US Cpi (index)',
        required=False)
    new_tlf = fields.Float(
        string='New TLF (index)',
        required=False)
    rate_id = fields.Many2one(
        comodel_name='ocma.myto.rate',
        string='Rate_id',
        required=False)
    fixed_o_m = fields.Float(
        string='Fixed O & M(n/mw/hr)',
        required=False)
    variable_o_m = fields.Float(
        string='Variable O & M(n/mw/hr)',
        required=False)
    fixed_o_m_dollar = fields.Float(
        string='Fixed O & M($/mw/hr)',
        required=False)
    variable_o_m_dollar = fields.Float(
        string='Variable O & M($/mw/hr)',
        required=False)

    capital_recovery = fields.Float(
        string='Capital recovery(n/mw/hr)',
        required=False)
    energy_charge = fields.Float(
        string='Energy charge(n/mw/hr)',
        required=False)
    energy_charge_tlf = fields.Float(
        string='Energy charge new TLF(n/mw/hr)',
        required=False)
    capacity_charge = fields.Float(
        string='Capacity charge(n/mw/hr)',
        required=False)
    wholesale_charge = fields.Float(
        string='Wholesale charge(n/mw/hr)',
        required=False)
    billing_circle = fields.Many2one(
        comodel_name='billing.cycle',
        string='Billing cycle',
        required=False)
    gas_fuel_price = fields.Float(
        string='Gas Fuel Price($/mmbtu)',
        required=False)
    vfcr = fields.Float(
        string='VFCR(n/mwh)',
        required=False)
    ncpi = fields.Float(
        string='NCPI(index)',
        required=False)
    us_ppi = fields.Float(
        string='US PPI(Index)',
        required=False)
    investment_dollar = fields.Float(
        string='Investment($/kw/month)',
        required=False)
    general_expenses_dollar = fields.Float(
        string='General Expenses($/kw/month)',
        required=False)
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
    # wholesale_charge = fields.Float(
    #     string='Wholesale charge(n/mw/hr)',
    #     required=False)
    # wholesale_charge = fields.Float(
    #     string='Wholesale charge(n/mw/hr)',
    #     required=False)
    # wholesale_charge = fields.Float(
    #     string='Wholesale charge(n/mw/hr)',
    #     required=False)
    # wholesale_charge = fields.Float(
    #     string='Wholesale charge(n/mw/hr)',
    #     required=False)
    # wholesale_charge = fields.Float(
    #     string='Wholesale charge(n/mw/hr)',
    #     required=False)
    # wholesale_charge = fields.Float(
    #     string='Wholesale charge(n/mw/hr)',
    #     required=False)






