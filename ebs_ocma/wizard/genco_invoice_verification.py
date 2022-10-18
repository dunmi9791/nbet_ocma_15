# -*- coding: utf-8 -*-

from odoo import models, fields, _

class CreateTransfer(models.TransientModel):
    _name = 'ebs_ocma.genco.invoice.transfer'
    _description = 'Genco Invoice verification'

    def _get_billing_cycle_id(self):
        context = dict(self._context or {})
        active_id = context.get('active_id', []) or []
        if active_id:
            billing_cycle = self.env['billing.cycle'].browse(active_id)
            if billing_cycle:
                return billing_cycle and billing_cycle.id or False
        return False

    billing_cycle_id = fields.Many2one(comodel_name='billing.cycle', string="Billing Cycle", default=_get_billing_cycle_id, readonly=True)
    bc_genco_parameter_ids = fields.One2many(
        comodel_name="ebs_ocma.genco.invoice.billing_cycle.parameter", inverse_name="billing_cycle_id", string="Genco Parameters", related='billing_cycle_id.bc_genco_parameter_ids', readonly=False)

    nbet_genco_parameter_ids = fields.One2many(
        comodel_name="ebs_ocma.nbet.genco.invoice.billing_cycle", inverse_name="billing_cycle_id", string="NBET Genco Parameters", related='billing_cycle_id.nbet_genco_parameter_ids', readonly=False)

    def verify_invoice(self):
        for rec in self:
            return