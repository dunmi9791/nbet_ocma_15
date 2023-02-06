from odoo import models, fields, api, _
from calendar import monthrange
from datetime import date

from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import UserError


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






