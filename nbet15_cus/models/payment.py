from odoo import models, fields, api
import math
from dateutil import relativedelta
from datetime import datetime
from datetime import date
from odoo.tools.translate import _
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    reviewed_by = fields.Many2one(
        comodel_name='res.users',
        string='Reviewed by',
        required=False)
    approved_by = fields.Many2one(
        comodel_name='res.users',
        string='Approved by',
        required=False)
    prepared_by = fields.Many2one('res.users', string='Prepared By',
                                  copy=False, tracking=True, default=lambda self: self.env.user.id)
    entered_by = fields.Many2one('res.users', string='Entered By',
                                 copy=False, tracking=True, default=lambda self: self.env.user.id)
    audited_by = fields.Many2one('res.users', string='Audited By',
                                 copy=False, tracking=True)
    posted_by = fields.Many2one('res.users', string='Posted By',
                                copy=False, tracking=True)

