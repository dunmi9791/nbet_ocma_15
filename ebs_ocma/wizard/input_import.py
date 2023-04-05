# -*- coding:utf-8 -*-

import base64
import csv
import xlrd
from xlrd import open_workbook
import datetime
from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
from openerp.exceptions import UserError
import openpyxl
from openpyxl import load_workbook
import base64
from io import BytesIO
from odoo.exceptions import UserError
import pandas as pd

class ImportBudgetLineWizard(models.TransientModel):
    _name = "import.input.line.wizard"

    files = fields.Binary(
        string="Import Excel File",
    )
    datas_fname = fields.Char(
        string='Import File Name'
    )
    billing_cycle_id = fields.Many2one(
        comodel_name='billing.cycle',
        string='Billing_cycle_id',
        required=False)

    def input_file(self):
        for record in self:
            try:
                # Get the billing cycle ID.
                cycle_id = record.billing_cycle_id

                # Get the data from the Excel file.
                data_file = record.files
                file_name = record.datas_fname or 'data.xlsx'

                # Read the Excel file using pandas.
                workbook = load_workbook(filename=BytesIO(data_file), read_only=True, data_only=True)
                sheet = workbook.active

                # df = pd.read_excel(data_file, sheet_name='Sheet1')

                # Get the column indices of the relevant fields.
                name_col = 2  # Replace with the correct column index.
                genco_col = 1  # Replace with the correct column index.

                # Create new records in the target model.
                inputs = self.env['ebs_ocma.genco.invoice.billing_cycle.parameter']
                genco = self.env['res.partner']
                for row in sheet.iter_rows(min_row=2):
                    try:
                        genco_name = row[genco_col - 1].value
                        genco = genco.search([('name', '=', genco_name)], limit=1)
                        if not genco:
                            raise ValueError('Partner not found: {}'.format(genco_name))
                    except Exception as e:
                        raise UserError('Error on row {}: {}'.format(row[0].row, str(e)))
                    # Create a new record for each row in the file.
                    input_vals = {
                        'partner_id': genco.id if genco else False,
                        'billing_cycle_id': cycle_id.id,
                        'name': row[name_col - 1].value,  # Replace with the correct column index.
                        # Add any additional fields that you want to create.
                    }
                    inputs.create(input_vals)

            except Exception as e:
                raise UserError('Error during import: {}'.format(str(e)))
# class ImportBudgetLineWizard(models.TransientModel):
#     _name = "import.input.line.wizard"
#
#     files = fields.Binary(
#         string="Import Excel File",
#     )
#     datas_fname = fields.Char(
#         string = 'Import File Name'
#     )
#
#     # @api.multi
#     # @api.onchange('files')
#     def input_file(self):
#         for record in self:
#             active_id = self._context.get('active_id')
#             cycle_id = self.env['billing.cycle'].browse(active_id)
#
#             try:
#                 inputx = StringIO()
#                 inputx.write(base64.decodestring(self.files))
#                 workbook = open_workbook(file_contents=inputx.getvalue())
#                 # workbook = xlrd.open_workbook(file_contents = base64.decodestring(record.files))
#             except:
#                 raise ValidationError("Please select .xls/xlsx file.")
#             sheet_name = workbook.sheet_names()
#             sheet = workbook.sheet_by_name(sheet_name[0])
#             number_of_rows = sheet.nrows
#             row = 1
#             while(row < number_of_rows):
#                 # general_input_id = self.env['account.budget.post'].search([('name','=',sheet.cell(row,0).value)])
#                 # if not general_budget_id:
#                 #     raise ValidationError('Budgetory Position not found for Budgetory Position :%s at row number %s '%(sheet.cell(row,0).value,row+1))
#                 genco_id = self.env['res.partner'].search([('name','=',sheet.cell(row,1).value)])
#                 if not genco_id:
#                     raise ValidationError('Genco not found :%s at row number %s '%(sheet.cell(row,1).value,row+1))
#
#                 try:
#                     capacity_sent_out = sheet.cell(row,3).value
#                 except:
#                     raise ValidationError('Capacity Sent out not found for Planned Amount :%s at row number %s '%(sheet.cell(row,3).value,row+1))
#                 row = row + 1
#                 vals = {
#                     'billing_cycle_id': cycle_id.id,
#                     'partner_id': genco_id.id,
#                     'capacity_sent_out_mw': capacity_sent_out
#
#                     }
#                 self.env['ebs_ocma.genco.invoice.billing_cycle.parameter'].create(vals)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: