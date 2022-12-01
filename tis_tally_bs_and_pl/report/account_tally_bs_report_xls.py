# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2019. All rights reserved.

from datetime import datetime
from odoo import models


class PayslipXlsx(models.AbstractModel):
    _name = 'report.tis_tally_bs_and_pl.report_tally_bs_xls.xslx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, wizard_obj):
        account_lines = self.env['report.accounting_pdf_reports.report_financial'].get_account_lines(data['form'])
        start_date = ''
        end_date = ''
        if data['form'].get('date_from'):
            start_date = datetime.strptime(data['form'].get('date_from'), '%Y-%m-%d').strftime(
                "%d-%m-%Y")
        if data['form'].get('date_to'):
            end_date = datetime.strptime(data['form'].get('date_to'), '%Y-%m-%d').strftime(
                "%d-%m-%Y")
        worksheet = workbook.add_worksheet('Report')
        format4 = workbook.add_format({'bold': True, 'align': 'left'})
        format0 = workbook.add_format({'font_size': 12, 'align': 'left', 'bottom': 1, 'right': 1, })
        text = workbook.add_format({'font_size': 12, 'align': 'left'})
        format3 = workbook.add_format({'font_size': 12, 'align': 'right'})
        format1 = workbook.add_format({'font_size': 12, 'align': 'left', 'bottom': 1, 'bold': True, })
        format5 = workbook.add_format({'font_size': 12, 'align': 'right', 'bottom': 1})
        format5_l = workbook.add_format({'font_size': 12, 'align': 'right', 'bottom': 1, 'right': 1})
        format6 = workbook.add_format({'font_size': 12, 'align': 'right', 'right': 1})
        format6_r = workbook.add_format({'font_size': 12, 'align': 'right', })
        format_7 = workbook.add_format(
            {'font_size': 12, 'bold': True, 'align': 'left', 'left': 1, 'top': 1, 'bottom': 1})
        format_8 = workbook.add_format(
            {'font_size': 12, 'bold': True, 'align': 'right', 'right': 1, 'top': 1, 'bottom': 1})
        format_8_r = workbook.add_format(
            {'font_size': 12, 'bold': True, 'align': 'right', 'top': 1, 'bottom': 1})
        format_9 = workbook.add_format(
            {'top': 1, 'bottom': 1})
        title = workbook.add_format({'font_size': 13, 'align': 'left', 'top': 1, 'right': 1, 'bold': True})
        format_10 = workbook.add_format({'top': 1})
        format_11 = workbook.add_format({'right': 1})
        worksheet.set_column(1, 2, 12)
        worksheet.set_column(0, 0, 25)
        worksheet.set_column(3, 3, 25)
        worksheet.set_column(4, 5, 12)
        worksheet.set_column(17, 21, 18)
        worksheet.set_column(16, 16, 38)
        worksheet.set_row(5, 20)
        worksheet.merge_range(1, 0, 1, 2, data['form']['account_report_id'][1], title)
        if start_date and end_date:
            worksheet.merge_range(2, 0, 2, 2, start_date + ' ' + 'to' + ' ' + end_date, format0)
        elif start_date:
            worksheet.merge_range(2, 0, 2, 2, 'from' + ' ' + start_date, format0)
        elif end_date:
            worksheet.merge_range(2, 0, 2, 2, 'till' + ' ' + end_date, format0)
        worksheet.write(3, 3, '', format_10)
        worksheet.write(3, 4, '', format_10)
        worksheet.write(3, 5, '', format_10)
        worksheet.write(3, 2, '', format_11)
        row = 4
        col = 0
        flag = 0
        row_n = 4
        for account in account_lines:
            if account.get('level') == 1:
                flag += 1
                if flag < 2:
                    worksheet.write(row, col, account.get('name'), format1)
                    if end_date:
                        worksheet.merge_range(row, col + 1, row, col + 2, 'as at' + ' ' + end_date, format5_l)
                    else:
                        worksheet.merge_range(row, col + 1, row, col + 2, '', format5_l)
                    worksheet.write(row + 1, col, account.get('name'), format4)
                    worksheet.write(row + 1, col + 2, account.get('balance'), format6)
                    row = row + 1
                elif flag == 2:
                    worksheet.write(row_n, col + 3, account.get('name'), format1)
                    if end_date:
                        worksheet.merge_range(row_n, col + 4, row_n, col + 5, 'as at' + ' ' + end_date, format5)
                    else:
                        worksheet.merge_range(row_n, col + 4, row_n, col + 5, '', format5)
                    worksheet.write(row_n + 1, col + 3, account.get('name'), format4)
                    worksheet.write(row_n + 1, col + 5, account.get('balance'), format6_r)
                    row_n = row_n + 1
            worksheet.write(row + 1, col + 2, '', format_11)

            if account.get('level') >= 2:
                if flag < 2:
                    worksheet.write(row + 1, col, ''.join([i for i in account.get('name') if not i.isdigit()]), text)
                    worksheet.write(row + 1, col + 1, account.get('balance'), format3)
                    row = row + 1
                elif flag == 2:
                    worksheet.write(row_n + 1, col + 3, ''.join([i for i in account.get('name') if not i.isdigit()]),
                                    text)
                    worksheet.write(row_n + 1, col + 4, account.get('balance'), format3)
                    row_n = row_n + 1
        flag_t = 0
        for line in account_lines:
            if line.get('level') == 1:
                flag_t += 1
                if flag_t < 2:
                    worksheet.write(max(row, row_n) + 1, 0, 'Total', format_7)
                    worksheet.write(max(row, row_n) + 1, 1, '', format_9)
                    worksheet.write(max(row, row_n) + 1, 2, abs(line.get('balance')), format_8)
                elif flag_t == 2:
                    worksheet.write(max(row, row_n) + 1, 3, 'Total', format_7)
                    worksheet.write(max(row, row_n) + 1, 4, '', format_9)
                    worksheet.write(max(row, row_n) + 1, 5, abs(line.get('balance')), format_8_r)
