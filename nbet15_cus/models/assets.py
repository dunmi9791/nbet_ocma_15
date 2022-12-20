# -*- coding: utf-8 -*-

from odoo import models, fields, api
import math
from dateutil import relativedelta
from datetime import datetime
from datetime import date
from odoo.tools.translate import _
from odoo.exceptions import UserError, ValidationError


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    assigned_to = fields.Many2one(
        comodel_name='res.users',
        string='Assigned to',
        required=False, track_visibility=True, trace_visibility='onchange',)
    source_of_fund = fields.Char(
        string='Source of fund',
        required=False, track_visibility=True, trace_visibility='onchange',)
    asset_number = fields.Char(string="Asset Number ",
                       default=lambda self: _('New'),
                       requires=False, readonly=True,)
    tag_number = fields.Char(string="Tag Number", required=False, track_visibility=True, trace_visibility='onchange',)
    location = fields.Many2one(
        comodel_name='location.ebs',
        string='Location',
        required=False, track_visibility=True, trace_visibility='onchange',)
    serial_num = fields.Char(string="Serial Number", required=False, track_visibility=True, trace_visibility='onchange', )
    manufacturer = fields.Char(string="Manufacturer", required=False, track_visibility=True, trace_visibility='onchange',)
    warranty_start = fields.Date(
        string='Warranty Start Date', required=False, track_visibility=True, trace_visibility='onchange',)
    warranty_end = fields.Date(
        string='Warranty End Date', required=False, track_visibility=True, trace_visibility='onchange', )
    model = fields.Char(string="Model", required=False, track_visibility=True, trace_visibility='onchange',)


    @api.model
    def create(self, vals):
        if vals.get('asset_number', _('New')) == _('New'):
            vals['asset_number'] = self.env['ir.sequence'].next_by_code('increment_assets') or _('New')
        result = super(AccountAsset, self).create(vals)
        return result

class LocationEbs(models.Model):
    _name = 'location.ebs'
    _description = 'LocationEbs'

    name = fields.Char(string="Location Name", required=False, track_visibility=True, trace_visibility='onchange',)
    description = fields.Text(
        string="Description",
        required=False)