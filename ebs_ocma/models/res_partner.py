# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Partner(models.Model):
    _inherit = 'res.partner'

    disco_category = fields.Selection(selection=[
        ('vesting_contract', "Vesting contract"),
        ('no_vesting_contract', "Without Vesting Contract"),
    ], string='Category')
    contract_capacity_share = fields.Float('Contract Capacity Share')
    is_genco = fields.Boolean(string='Genco')
    is_disco = fields.Boolean(string='Disco')
    myto_rate = fields.Many2one(
        comodel_name='ocma.myto.rate',
        string='Myto rate',
        required=False)
    rate_category = fields.Many2one(comodel_name='ebs_ocma.myto.rate.cateogry', string='Rate Category')

    rate = fields.Float(string='Rate (Capacity Tariff)', store=True)
    rate_gas_price = fields.Float(string='Tariff (New gas Price)', store=True)

    disco_short_code = fields.Char(string='Short Code')

    # current_mro = fields.Float(string='Current MRO (%)', tracking=True)
