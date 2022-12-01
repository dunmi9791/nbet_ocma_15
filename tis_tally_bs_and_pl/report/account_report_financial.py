# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2019. All rights reserved.

from odoo import models, _


class ReportFinancialTally(models.AbstractModel):
    _name = 'report.tis_tally_bs_and_pl.report_tally_bs'
    _inherit = 'report.accounting_pdf_reports.report_financial'
