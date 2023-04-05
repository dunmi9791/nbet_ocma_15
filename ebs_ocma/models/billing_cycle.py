from odoo import models, fields, api, _
from calendar import monthrange
from datetime import date

from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import UserError

YEARS = [
    ('2000', '2000'),
    ('2001', '2001'),
    ('2002', '2002'),
    ('2003', '2003'),
    ('2004', '2004'),
    ('2005', '2005'),
    ('2006', '2006'),
    ('2020', '2020'),
    ('2021', '2021'),
    ('2022', '2022'),
    ('2023', '2023'),
]

MONTHS = [
    ('JAN', 'January'), 
    ('FEB', 'February'), 
    ('MAR', 'March'), 
    ('APR', 'April'),
    ('MAY', 'May'), 
    ('JUN', 'June'), 
    ('JUL', 'July'), 
    ('AUG', 'August'),
    ('SEPT', 'September'), 
    ('OCT', 'October'), 
    ('NOV', 'November'),
    ('DEC', 'December'), 
]

class BillingCycle(models.Model):
    _name = 'billing.cycle'
    _description = 'Billing Cycle'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    title = fields.Char(string='Title')

    name = fields.Char(string='Billing Cycle', compute="billing_cycle")
    month = fields.Selection(selection=MONTHS, string='Billing Month')
    year = fields.Selection(selection=YEARS,
                            string='Billing Year', store=True)
    days_in_month = fields.Integer('Days In Month', default="30", compute="_compute_days_in_month")
    
    date = fields.Date(
        string='Date',
        required=False)
    ref_no = fields.Char(
        string='Reference Number',
        required=False)

    ref_sequence = fields.Char(
        string='Sequence No.', readonly=True, index=True, copy=False, default='New')

    genco_inv_verify = fields.One2many(
        comodel_name='genco.verify',
        inverse_name='billing_cycle_id',
        string='Genco_inv_verify',
        required=False)
    genco_inv_verify_dollars = fields.One2many(
        comodel_name='genco.verify_dollars',
        inverse_name='billing_cycle_id',
        string='Genco_inv_verify dollars',
        required=False)
    cbn_average = fields.Float(
        string='CBN Average',
        required=False, tracking=True)
    nbet_dist_rate = fields.Float(
        string='Nbet Dist Rate',
        required=False, tracking=True)
    nbet_dist_azura = fields.Float(
        string='Nbet Dist Azura',
        required=False, tracking=True)
    additional_notes = fields.Text(
        string="Notes",
        required=False, tracking=True)

    hours_in_month = fields.Float(string='Hours in Month', compute="_compute_hours_in_month")
    transmission_loss_factor = fields.Float(string="Transmission Loss Factor")
    agip_quaterly_index = fields.Float(string="Agip Quaterly Index")
    azura_fx_date = fields.Date(string="Azura FX Date")
    azura_fx_value = fields.Float(string="Azura FX Value")
    user_id = fields.Many2one(
        comodel_name='res.users', string='Responsible User.', default=lambda self: self.env.uid)
    payments_ids = fields.One2many('accounts.payments', compute='_circle_payments', string='Payments')
    receipts_ids = fields.One2many('accounts.payments', compute='_circle_receipts', string='Disco Receipts')

    state = fields.Selection([
        ('draft', 'New'),
        ('open', 'Validate'),
        ('gen_inv', 'Generate Invoices'),
        ('mro_application', 'MRO Application'),
        ('invoice_verification', 'Bills Verification'),
        ('gen_bill', 'Generate Verified Bills'),
    ], string='state', default="draft", help="A new record is in draft, once it is validated, it goes to open and then it is approved in Done state")
    
    def action_submit(self):
        self.state='open'
        
    def action_approve(self):
        # self.state='invoice_verification'
        self.state='gen_inv'

    def action_verify_done(self):
        self.state='gen_bill'

    # def action_gen_inv(self):
    #     self.state='gen_inv'
        
    def action_reject(self):
        self.state='reject'
        
    def action_cancel(self):
        self.state='cancel'
        
    # state = fields.Selection([
    #     ('invoice_verification', 'Invoice Verification'),
    #     ('done', 'Verified'),
    # ], string='state', default="draft", help="A new record is in draft, once it is validated, it goes to open and then it is approved in Done state")
    
    @api.depends('date')
    def _compute_days_in_month(self):
        for rec in self:
            if rec.date:
                date = datetime.strptime(str(rec.date), DEFAULT_SERVER_DATE_FORMAT)
                rec.days_in_month = monthrange(date.year, date.month)[1]
    
    def _compute_hours_in_month(self):
        for record in self:
            record.hours_in_month = record.days_in_month * 24

    def _circle_payments(self):
        pass

    def _circle_receipts(self):
        pass

    @api.model
    def create(self, vals):
        if vals.get('ref_sequence', 'New') == 'New':
            vals['ref_sequence'] = self.env['ir.sequence'].next_by_code(
                'billing_cycle') or '/'
        return super(BillingCycle, self).create(vals)

    @api.depends('month', 'year')
    def billing_cycle(self):
        for record in self:
            m = record.month
            y = record.year
            record['name'] = ("%s%s" % (m, y))

    bc_genco_parameter_ids = fields.One2many(
        comodel_name="ebs_ocma.genco.invoice.billing_cycle.parameter", inverse_name="billing_cycle_id", string="Genco Parameters")

    bc_disco_parameter_ids = fields.One2many(
        comodel_name="ebs_ocma.disco.invoice.billing_cycle.parameter", inverse_name="billing_cycle_id", string="Disco Parameters")

    nbet_genco_parameter_ids = fields.One2many(
        comodel_name="ebs_ocma.nbet.genco.invoice.billing_cycle", inverse_name="billing_cycle_id", string="NBET Genco Parameters")

    # genco_invoice_ids = fields.Many2many(comodel_name='account.move', string='Genco Bills', copy=False, compute='_get_genco_bills')
    genco_invoice_ids = fields.Many2many(comodel_name='account.move', string='Genco Bills', copy=False)
    genco_invoices_count = fields.Integer(string='Bills Count', compute="_compute_bills_count")

    # disco_invoice_ids = fields.Many2many(comodel_name='account.move', relation='account_move_disco_invoice_rel', string='Disco Invoices', copy=False, compute='_get_disco_invoices')

    disco_invoice_ids = fields.Many2many(
        comodel_name='account.move',
        relation='account_move_billing_cycle_disco_invoice_rel',
        column1='move_id',
        column2='billing_cycle_disco_invoice_move_id',
        string='Disco Invoices',
        copy=False)
    
    disco_invoices_count = fields.Integer(string='Invoices Count', compute="_compute_invoices_count")

    def _compute_bills_count(self):
        self.genco_invoices_count = len(self.genco_invoice_ids)

    def action_view_genco_invoices(self):
        # action = self.env.ref('account.action_vendor_bill_template')
        action = self.env.ref('account.action_move_in_invoice_type')
        result = action.read()[0]
        if self.genco_invoices_count != 1:
            result['domain'] = "[('id', 'in', " + str(self.genco_invoice_ids.ids) + ")]"
        elif self.genco_invoices_count == 1:
            res = self.env.ref('account.invoice_supplier_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = self.genco_invoice_ids.id
        return result

    def _get_genco_bills(self):
        for rec in self:
            related_genco_invoicing = self.env["ebs_ocma.genco.invoice"].search([("billing_cycle_id", "=", rec.id)], limit=1)
            rec.genco_invoice_ids = related_genco_invoicing.genco_invoice_ids

    def _get_disco_invoices(self):
        for rec in self:
            related_disco_invoicing = self.env["ebs_ocma.disco.invoice"].search([("billing_cycle_id", "=", rec.id)], limit=1)
            rec.disco_invoice_ids = related_disco_invoicing.disco_invoice_ids

    def _compute_invoices_count(self):
        self.disco_invoices_count = len(self.disco_invoice_ids)

    def action_view_disco_invoices(self):
        action = self.env.ref('account.action_move_out_invoice_type')
        result = action.read()[0]
        if self.disco_invoices_count != 1:
            result['domain'] = "[('id', 'in', " + str(self.disco_invoice_ids.ids) + ")]"
        elif self.disco_invoices_count == 1:
            res = self.env.ref('account.invoice_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = self.disco_invoice_ids.id
        return result

    def _get_genco_parameters(self):
        for rec in self:
            related_genco_invoicing = self.env["ebs_ocma.genco.invoice"].search([("billing_cycle_id", "=", rec.id)], limit=1)
            rec.bc_genco_parameter_ids = related_genco_invoicing.mapped('genco_parameter_ids')

    def _get_disco_parameters(self):
        for rec in self:
            related_disco_invoicing = self.env["ebs_ocma.disco.invoice"].search([("billing_cycle_id", "=", rec.id)], limit=1)
            rec.bc_disco_parameter_ids = related_disco_invoicing.mapped('disco_parameter_ids')

    disco_total_capacity_delivered = fields.Float(string='Disco Total Energy Delivered', compute='_compute_total_capacity_delivered')
    disco_total_energy_delivered = fields.Float(string='Disco Total Energy Delivered', compute='_compute_total_energy_delivered')

    genco_total_capacity = fields.Float(string='Genco Total Capacity', compute='_compute_total_capacity')
    genco_total_energy_sent_out = fields.Float(string='Genco Total Energy Sent Out', compute='_compute_total_energy_sent_out')
    genco_total_capacity_import = fields.Float(string='Genco Total Capacity Import', compute='_compute_total_capacity_import')
    genco_total_energy_import = fields.Float(string='Genco Total Energy Import', compute='_compute_total_energy_import')

    def _compute_total_capacity_delivered(self):
        for rec in self:
            if rec.bc_disco_parameter_ids:
                for line in rec.bc_disco_parameter_ids:
                    rec.disco_total_capacity_delivered += line.capacity_delivered
            else:
                rec.disco_total_capacity_delivered = 0

    def _compute_total_energy_delivered(self):
        for rec in self:
            if rec.bc_disco_parameter_ids:
                for line in rec.bc_disco_parameter_ids:
                    rec.disco_total_energy_delivered += line.energy_delivered
            else:
                rec.disco_total_energy_delivered = 0

    def _compute_total_capacity(self):
        for rec in self:
            if rec.bc_genco_parameter_ids:
                for line in rec.bc_genco_parameter_ids:
                    rec.genco_total_capacity += line.capacity
            else:
                rec.genco_total_capacity = 0

    def _compute_total_energy_sent_out(self):
        for rec in self:
            if rec.bc_genco_parameter_ids:
                for line in rec.bc_genco_parameter_ids:
                    rec.genco_total_energy_sent_out += line.energy_sent_out_mwh
            else:
                rec.genco_total_energy_sent_out = 0
    
    def _compute_total_capacity_import(self):
        for rec in self:
            if rec.bc_genco_parameter_ids:
                for line in rec.bc_genco_parameter_ids:
                    rec.genco_total_capacity_import += line.capacity_import
            else:
                rec.genco_total_capacity_import = 0
    
    def _compute_total_energy_import(self):
        for rec in self:
            if rec.bc_genco_parameter_ids:
                for line in rec.bc_genco_parameter_ids:
                    rec.genco_total_energy_import += line.energy_import
            else:
                rec.genco_total_energy_import = 0

    disco_capacity_delivered = fields.Float(string='capacity delivered', compute='_compute_disco_capacity_delivered')
    disco_energy_delivered = fields.Float(string='disco energy delivered', compute='_compute_disco_energy_delivered')

    def _compute_disco_capacity_delivered(self):
        for rec in self:
            disco_capacity_delivered = 0
            for line in rec.bc_disco_parameter_ids:
                if line.partner_id.is_genco:
                    disco_capacity_delivered += line.capacity_delivered
            rec.disco_capacity_delivered = rec.disco_total_capacity_delivered + rec.genco_total_capacity_import - (disco_capacity_delivered)
    
    def _compute_disco_energy_delivered(self):
        for rec in self:
            disco_energy_delivered = 0
            for line in rec.bc_disco_parameter_ids:
                if line.partner_id.is_genco:
                    disco_energy_delivered += line.energy_delivered
            rec.disco_energy_delivered = rec.disco_total_energy_delivered + rec.genco_total_energy_import - (disco_energy_delivered)

    energy_diff = fields.Float(string='Energy Difference', compute='_compute_energy_delivered_diff')
    capacity_diff = fields.Float(string='Capacity Difference', compute='_compute_capacity_delivered_diff')

    total_invoiced_energy = fields.Float(string='invoiced energy', compute='_genco_invoiced_energy')

    def _genco_invoiced_energy(self):
        for rec in self:
            for line in rec.bc_genco_parameter_ids:
                rec.invoiced_energy += line.invoiced_energy

    def _compute_energy_delivered_diff(self):
        for rec in self:
            rec.energy_diff = 1.52
            # rec.energy_diff = rec.disco_total_energy_delivered - rec.genco_total_energy_sent_out
    
    def _compute_capacity_delivered_diff(self):
        for rec in self:
            rec.capacity_diff = 0.37
            # rec.capacity_diff = rec.disco_total_capacity_delivered - rec.genco_total_capacity

    weighted_cost_power = fields.Float('Weighted Cost of Power (Capacity)', compute='_compute_weighted_cost_power')
    weighted_avg_cost_power = fields.Float('Weighted Average Cost of Power (Capacity) ', compute='_compute_weighted_avg_cost_power')

    # total_capacity = fields.Float(string='Total Capacity', compute='_compute_total_capacity')
    total_energy_sent_out_mwh = fields.Float(string='Total Energy Sent Out(MWh)', compute='_compute_total_energy_sent_out_mwh')

    def _compute_weighted_cost_power(self):
        for rec in self:
            for line in rec.bc_genco_parameter_ids:
                rec.weighted_cost_power += (line.capacity_payment / line.capacity) if line.capacity != 0 else 0
                
    def _compute_weighted_avg_cost_power(self):
        for rec in self:
            for line in rec.bc_genco_parameter_ids:
                rec.weighted_avg_cost_power += line.energy_payment / line.energy_sent_out_mwh if line.energy_sent_out_mwh != 0 else 0

    # def _compute_total_capacity(self):
    #     for rec in self:
    #         for line in rec.bc_genco_parameter_ids:
    #             rec.total_capacity += line.capacity
    
    def _compute_total_energy_sent_out_mwh(self):
        for rec in self:
            for line in rec.bc_genco_parameter_ids:
                rec.total_energy_sent_out_mwh += line.energy_sent_out_mwh

    def _create_genco_bill(self, partner_id, ref, origin, invoice_value):
        self.ensure_one()
        company_id = self.env.user.company_id.id
        # journal_id = (self.env['account.move'].with_context(company_id=company_id or self.env.user.company_id.id).default_get(['journal_id'])['journal_id'])
        journal_id = self.env.ref('ebs_ocma.genco_invoice_journal').id or (self.env['account.move'].with_context(company_id=company_id or self.env.user.company_id.id).default_get(['journal_id'])['journal_id'])
        if not journal_id:
            raise UserError(_('Please define an accounting journal.'))

        for rec in self:
            invoice_vals = {
                'ref': rec.name or '',
                'move_type': 'in_invoice',
                'billing_circle_id': self.id,
                
                'partner_id': partner_id.id,
                'invoice_date': rec.date,

                'invoice_origin': origin,
                # 'account_id': partner_id.property_account_receivable_id.id,

                'journal_id': journal_id,
                'company_id': company_id,

                # 'user_id': self.user_id and self.user_id.id,
                # 'fiscal_position_id': self.fiscal_position_id.id or self.partner_invoice_id.property_account_position_id.id,
                # 'payment_term_id': self.payment_term_id.id,
                # 'currency_id': self.pricelist_id.currency_id.id,
                
                'invoice_line_ids': [(0, 0, {
                    'name': ref,
                    'quantity': 1, 
                    'account_id': 17, # account to be set
                    'price_unit': invoice_value,
                })],
            }
            invoice_id = self.env['account.move'].create(invoice_vals)
            self.genco_invoice_ids += invoice_id

    def generate_genco_invoice(self):
        for rec in self:
            for line in rec.bc_genco_parameter_ids:
                if line.verified:
                    rec._create_genco_bill(partner_id=line.partner_id, ref=line.name, invoice_value=line.total_payment, origin=self.ref_no)
            for line in rec.nbet_genco_parameter_ids:
                if line.verified:
                    rec._create_genco_bill(partner_id=line.partner_id, ref=line.name, invoice_value=line.total_payment, origin=self.ref_no)

    def action_verify(self):
        for rec in self:
            rec.generate_genco_invoice()
            # rec.write({'state': 'gen_inv'})
            for invoice in rec.genco_invoice_ids:
                if invoice.amount_total > 0 :
                    # invoice.action_invoice_open()
                    invoice.action_post()

    def _create_disco_invoice(self, partner_id, ref, origin, invoice_value):
        self.ensure_one()
        company_id = self.env.user.company_id.id
        # journal_id = (self.env['account.move'].with_context(company_id=company_id or self.env.user.company_id.id).default_get(['journal_id'])['journal_id'])
        journal_id = self.env.ref('ebs_ocma.disco_invoice_journal').id or (self.env['account.move'].with_context(company_id=company_id or self.env.user.company_id.id).default_get(['journal_id'])['journal_id'])
        if not journal_id:
            raise UserError(_('Please define an accounting journal.'))

        for rec in self:
            invoice_vals = {
                'ref': rec.name or '',
                'move_type': 'out_invoice',
                'partner_id': partner_id.id,
                'invoice_date': rec.date,

                'invoice_origin': origin,
                # 'account_id': partner_id.property_account_receivable_id.id,

                'journal_id': journal_id,
                'company_id': company_id,
                'billing_circle_id': self.id,

                # 'user_id': self.user_id and self.user_id.id,
                # 'fiscal_position_id': self.fiscal_position_id.id or self.partner_invoice_id.property_account_position_id.id,
                # 'payment_term_id': self.payment_term_id.id,
                # 'currency_id': self.pricelist_id.currency_id.id,
                
                'invoice_line_ids': [
                (0, 0, {
                    'display_type': 'line_section',
                    'name': 'ENERGY CHARGE',
                })
                ,(0, 0, {
                    'name': 'Total Disco Share of Energy Received (MWh)',
                    'quantity': 1, 
                    'account_id': 17, # account to be set
                    'price_unit': invoice_value,
                })
                ,(0, 0, {
                    'name': 'Total Energy Received by %s Disco (MWh)' % partner_id.name,
                    'quantity': 1, 
                    'account_id': 17, # account to be set
                    'price_unit': 0,
                })
                ,(0, 0, {
                    'name': 'percentage of Total Energy Received by %s Disco' % partner_id.name,
                    'quantity': 1, 
                    'account_id': 17, # account to be set
                    'price_unit': 0,
                })
                , (0, 0, {
                        'display_type': 'line_section',
                        'name': 'CAPACITY CHARGE',
                    })
                ,(0, 0, {
                    'name': 'Total Disco Share of Capacity (MW)',
                    'quantity': 1, 
                    'account_id': 17, # account to be set
                    'price_unit': 0,
                })
                ,(0, 0, {
                    'name': '%s Disco Share of Capacity (MW)' % partner_id.name,
                    'quantity': 1, 
                    'account_id': 17, # account to be set
                    'price_unit': 0,
                })
                , (0, 0, {
                        'display_type': 'line_section', 
                        'name': 'SUPPLEMENTARY COSTS',
                    })
                , (0, 0, {
                    'name': 'Total Start Up Costs',
                    'quantity': 1, 
                    'account_id': 17, # account to be set
                    'price_unit': 0,
                })
                , (0, 0, {
                        'display_type': 'line_section',
                        'name': 'PREVIOUS BALANCE CARRIED FORWARD',
                })
                ,(0, 0, {
                    'name': ref,
                    'quantity': 1, 
                    'account_id': 17, # account to be set
                    'price_unit': 0,
                })],
            }
            disco_invoice_id = self.env['account.move'].create(invoice_vals)
            disco_invoice_id.action_post()
            self.disco_invoice_ids += disco_invoice_id
    
    def generate_disco_invoice(self):
        for rec in self:
            for line in rec.bc_disco_parameter_ids:
                DiscoinvoicingOBJ = self.env['ebs_ocma.disco.invoicing'].sudo()
                new_disco_invoicing = DiscoinvoicingOBJ.create(
                    {
                        'billing_cycle_id': self.id,
                        'month': rec.month,
                        'date': date.today(),
                        'partner_id': line.partner_id.id,
                    }
                )
                # rec.disco_invoicing_ids += new_disco_invoicing
                # rec._create_journal_entries(partner=line.partner_id)
                rec._create_disco_invoice(partner_id=line.partner_id, ref=line.name, invoice_value=line.invoice_value, origin=self.ref_no)
            # rec.write({'state': 'invoice_verification'})
            rec.write({'state': 'mro_application'})
            
    

class GencoVerify(models.Model):
    _name = 'genco.verify'
    _description = 'GencoVerify'

    name = fields.Char()
    genco_id = fields.Many2one(
        comodel_name='res.partner',
        string='Genco',
        required=False)
    capacity_payment = fields.Float(
        string='Capacity Payments',
        required=False)
    energy_payment = fields.Float(
        string='Energy payments',
        required=False)
    startup_payment = fields.Float(
        string='Startup Payments',
        required=False)
    interest_payment = fields.Float(
        string='Interest Payments',
        required=False)
    total_payment = fields.Float(
        string='Total Payments',
        required=False)
    nbet_computed = fields.Float(
        string='Nbet computed figures',
        required=False)
    date_received = fields.Date(
        string='Date received',
        required=False)
    due_date = fields.Date(
        string='Due date',
        required=False)
    cus_invoice_ref = fields.Char(
        string='Customer invoice ref',
        required=False)
    billing_cycle_id = fields.Many2one(
        comodel_name='billing.cycle',
        string='Billing Cycle',
        required=False)


class GencoVerifyDollars(models.Model):
    _name = 'genco.verify_dollars'
    _description = 'GencoVerify'

    name = fields.Char()
    genco_id = fields.Many2one(
        comodel_name='res.partner',
        string='GENCO',
        required=False)
    capacity_payment = fields.Float(
        string='Capacity Payment',
        required=False)
    energy_payment = fields.Float(
        string='Energy Payment',
        required=False)
    startup_payment = fields.Float(
        string='Startup Payment',
        required=False)
    interest_payment = fields.Float(
        string='Interest Payment',
        required=False)
    total_payment = fields.Float(
        string='Total Payment',
        required=False)
    nbet_computed = fields.Float(
        string='Nbet Computed',
        required=False)
    date_received = fields.Date(
        string='Date Received',
        required=False)
    due_date = fields.Date(
        string='Due Date',
        required=False)
    cus_invoice_ref = fields.Char(
        string='Customer Invoice Reference',
        required=False)
    billing_cycle_id = fields.Many2one(
        comodel_name='billing.cycle',
        string='Billing Cycle',
        required=False)


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    billing_circle_id = fields.Many2one(comodel_name='billing.cycle', string='Billing Cycle')

    def action_invoice_open(self):
        result = super(AccountInvoice, self).action_invoice_open()
        self._check_billing_cycle()
        return result

    def _check_billing_cycle(self):
        for rec in self:
            for line in rec.billing_circle_id.bc_genco_parameter_ids:
                if line.invoice_id.state in ['draft','open','approved']:
                    raise UserError(_("Invoice is to be verified"))
                elif line.invoice_id.state == "invoice_verification":
                    raise UserError(_("Invoice is currently being verified"))


class GencoBCParaemeter(models.Model):
    _name = 'ebs_ocma.genco.invoice.billing_cycle.parameter'
    _description = 'Genco Parameters'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")
    partner_id = fields.Many2one(comodel_name='res.partner', string='Genco')
    capacity_sent_out_mw = fields.Float(string='Capacity Sent Out (MW)')
    energy_sent_out_kwh = fields.Float(string='Energy Sent Out (kWh)')
    capacity_import = fields.Float(string='Capacity Import (MW)')
    energy_import = fields.Float(string='Energy Import (kWh)')

    invoiced_capacity = fields.Float(string='Invoiced Capacity', compute='_compute_invoice_capacity')
    invoiced_energy = fields.Float(string='Invoiced Energy', compute='_compute_invoiced_energy')

    capacity = fields.Float('capacity(MWh)', compute='_compute_capacity')
    energy_sent_out_mwh = fields.Float(string='Energy Sent Out (MWh)', compute='_compute_energy_sent_out_mwh')
    capacity_payment = fields.Float('Capacity Payment', compute='_compute_capacity_payment')
    energy_payment = fields.Float('Energy Payment', compute='_compute_energy_payment')
    total_payment = fields.Float('Total Payment', compute='_compute_total_payment')
    myto_capacity_tariff = fields.Float(
        string='PPA capacity tariff',
        required=False, compute='_compute_capacity_tariff')
    myto_energy_tariff = fields.Float(
        string='PPA Energy tariff',
        required=False, compute='_compute_energy_tariff')

    billing_cycle_id = fields.Many2one(comodel_name='billing.cycle', string="Billing Cycle")

    verified = fields.Boolean(string='verified invoice')

    def _compute_capacity_tariff(self):
        for rec in self:
            billingcycle = rec.billing_cycle_id.id
            mytorate = rec.partner_id.myto_rate.id
            rates = self.env['hydro.rates'].search([('rate_id', '=', mytorate), ('billing_circle', '=', billingcycle)])
            rec.myto_capacity_tariff = rates.capacity_charge

    def _compute_energy_tariff(self):
        for rec in self:
            billingcycle = rec.billing_cycle_id.id
            mytorate = rec.partner_id.myto_rate.id
            rates = self.env['hydro.rates'].search([('rate_id', '=', mytorate), ('billing_circle', '=', billingcycle)])
            rec.myto_energy_tariff = rates.energy_charge

        pass

    
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.name = self.partner_id.name

    def _compute_invoice_capacity(self):
        for rec in self:
            rec.invoiced_capacity = rec.capacity_sent_out_mw - rec.capacity_import

    def _compute_invoiced_energy(self):
        for rec in self:
            rec.invoiced_energy = ((100 - rec.billing_cycle_id.transmission_loss_factor)/100 * rec.energy_sent_out_kwh) - rec.energy_import
    
    def _compute_capacity(self):
        for rec in self:
            try:
                # rec.capacity = rec.capacity_sent_out_mw / rec.invoice_id.billing_cycle_id.hours_in_month
                rec.capacity = rec.invoiced_capacity / rec.billing_cycle_id.hours_in_month
            except ZeroDivisionError:
                rec.capacity = 0.00

    def _compute_energy_sent_out_mwh(self):
        for rec in self:
            # rec.energy_sent_out_mwh = rec.energy_sent_out_kwh / 1000
            if rec.invoiced_energy > 0:
                rec.energy_sent_out_mwh = rec.invoiced_energy / 1000
            else:
                rec.energy_sent_out_mwh = 0

    def _compute_capacity_payment(self):
        for rec in self:
            rec.capacity_payment = rec.capacity * rec.billing_cycle_id.hours_in_month * rec.myto_capacity_tariff
    
    def _compute_energy_payment(self):
        for rec in self:
            rec.energy_payment = rec.energy_sent_out_mwh * rec.myto_energy_tariff
            # rec.energy_payment = rec.invoiced_energy * rec.partner_id.rate_gas_price

    def _compute_total_payment(self):
        for rec in self:
            rec.total_payment = rec.capacity_payment + rec.energy_payment
            try:
                rec.capacity = rec.capacity_sent_out_mw / rec.billing_cycle_id.hours_in_month
            except ZeroDivisionError:
                rec.capacity = 0.0

class NBETGencoBCParaemeter(models.Model):
    _name = 'ebs_ocma.nbet.genco.invoice.billing_cycle'
    _description = 'NBET Genco Parameters'
    
    name = fields.Char(string="Name")
    partner_id = fields.Many2one(comodel_name='res.partner', string='Genco')
    capacity_payment = fields.Float('Capacity Payment')
    energy_payment = fields.Float('Energy Payment')
    total_payment = fields.Float('Total Payment')
    gas_element = fields.Float('Gas Invoice and Transport')
    percent_gas = fields.Float('% Gas INV to Genco INV')
    genco_portion_market = fields.Float('Genco Portion of Market Payment')
    percent_payment = fields.Float('% Payment')
    genco_shortfall = fields.Float('Genco Tariff Shortfall')
    percent_ts_payment = fields.Float('% TS Payment')
    total_payment_genco = fields.Float('Total Payment to Genco')
    market_percent_payment = fields.Float('Market % Payment')

    billing_cycle_id = fields.Many2one(comodel_name='billing.cycle', string="Billing Cycle")

    verified = fields.Boolean(string='verified invoice')

class BCDiscoParaemeter(models.Model):
    _name = 'ebs_ocma.disco.invoice.billing_cycle.parameter'
    _description = 'Disco Parameters'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one(comodel_name='res.partner', string='Disco')
    name = fields.Char(string="Name")
    capacity_delivered = fields.Float(string='Capacity Delivered', required=False)
    energy_delivered = fields.Float(string='Energy Delivered', required=False)

    capacity_shared = fields.Float(string='Capacity Shared (Mw/Month)')
    energy_shared = fields.Float(string='Energy Shared (kWh)')

    percentage_total = fields.Float(string='Percentage of total', required=False, compute='_compute_percentage_total')
    portion_capacity = fields.Float(string='Portion Capacity', required=False, compute='_compute_portion_capacity')
    portion_energy = fields.Float(string='Portion Energy', required=False, compute='_compute_portion_energy')

    percent_shared = fields.Float(string='% Shared', compute='_compute_percent_shared')
    
    invoice_value = fields.Float(string='Invoice Value', required=False)

    billing_cycle_id = fields.Many2one(comodel_name='billing.cycle', string="Billing Cycle")
    
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.name = self.partner_id.name

    def _compute_percentage_total(self):
        for rec in self:
            rec.percentage_total = (rec.energy_delivered / rec.billing_cycle_id.disco_total_energy_delivered if rec.billing_cycle_id.disco_total_energy_delivered != 0 else 0) * 100

    def _compute_portion_capacity(self):
        for rec in self:
            rec.portion_capacity = (rec.percentage_total / 100) * rec.billing_cycle_id.genco_total_capacity
    
    def _compute_portion_energy(self):
        for rec in self:
            rec.portion_energy = (rec.percentage_total / 100) * rec.billing_cycle_id.genco_total_energy_sent_out

    def _compute_percent_shared(self):
        for rec in self:
            rec.percent_shared = rec.energy_shared / rec.total_energy_shared if rec.total_energy_shared != 0 else 0
