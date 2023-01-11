from odoo import api, fields, models, _
from logging import getLogger

_logger = getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.payment"

    amount_to_text = fields.Char(compute='_compute_amount_to_text')

    def _compute_amount_to_text(self):
        for rec in self:
            rec.amount_to_text = rec.currency_id.amount_to_text(rec.amount)


    approved_by = fields.Many2one('res.users', string='Approved By',
                                  copy=False, tracking=True)
    prepared_by = fields.Many2one('res.users', string='Prepared By',
                                  copy=False, tracking=True, default=lambda self: self.env.user.id)
    entered_by = fields.Many2one('res.users', string='Entered By',
                                 copy=False, tracking=True, default=lambda self: self.env.user.id)
    audited_by = fields.Many2one('res.users', string='Audited By',
                                 copy=False, tracking=True)
    posted_by = fields.Many2one('res.users', string='Posted By',
                                copy=False, tracking=True)