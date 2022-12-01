# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2019. All rights reserved.

from odoo import api, fields, models
from datetime import datetime


class AccountingReport(models.TransientModel):
    _inherit = "accounting.report"

    report_type = fields.Selection([('normal', 'Normal'), ('tally', 'Tally')], string='Report Type', default='tally')

    @api.multi
    def print_tally_bs(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'journal_ids', 'target_move', 'company_id'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang') or 'en_US')
        return self.with_context(discard_logo_check=True)._print_bs_report(data)

    def _print_bs_report(self, data):
        data['form'].update(self.read(
            ['date_from_cmp', 'debit_credit', 'date_to_cmp', 'filter_cmp', 'account_report_id', 'enable_filter',
             'label_filter', 'target_move', 'report_type'])[0])
        return self.env.ref('tis_tally_bs_and_pl.action_report_tally_bs').report_action(self, data=data,
                                                                                           config=False)

    @api.multi
    def export_tally_bs(self, context=None):
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read()[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang') or 'en_US')
        return self.env.ref('tis_tally_bs_and_pl.action_report_tally_bs_xls').report_action(self, data=data)

    def account_name(self, name):
        return ''.join([i for i in name if not i.isdigit()])

    def date_format(self, date):
        return datetime.strptime(date, '%Y-%m-%d').strftime(
            "%d-%m-%Y")
