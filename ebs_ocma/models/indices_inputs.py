from odoo import models, fields, api, _


class UsCpiIndices(models.Model):
    _name = 'uscpi.indices'
    _description = 'UsCpiIndices'

    date = fields.Date(
        string='Date',
        required=False)
    us_cpi = fields.Float(
        string='Us CPI',
        required=False)
