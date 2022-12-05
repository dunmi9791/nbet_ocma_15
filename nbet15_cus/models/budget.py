# -*- coding: utf-8 -*-

from odoo import models, fields, api
import math
from dateutil import relativedelta
from datetime import datetime
from datetime import date
from odoo.tools.translate import _
from odoo.exceptions import UserError, ValidationError


class CrossoveredBudget(models.Model):
    _inherit = 'budget.budget'

    budget_line_count = fields.Integer(string="Budget Lines", compute='get_budget_count', )
    forecast_lines = fields.One2many(
        comodel_name='budget.forecast',
        inverse_name='budget_id',
        string='Forecast lines',
        required=False, ondelete='cascade')
    forecast_done = fields.Binary(string="Forecast Done",  )

    def get_budget_count(self):
        count = self.env['budget.lines'].search_count([('budget_id', '=', self.id)])
        self.budget_line_count = count


    def open_budget_lines(self):
        return {
            'name': _('budget_lines'),
            'domain': [('id', 'in', budget.lines)],
            'view_type': 'form',
            'res_model': 'budget.lines',
            'view_id': 'budget_lines_tree',
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',

        }

    def create_forecast_lines(self):
        if self.forecast_done:
            msg = _('Forecast Lines Already entered')
            raise UserError(msg)
        else:
            for line in self.budget_line:
                forecast_line = {
                    'budget_line': line.analytic_account_id.id,
                    'budget_id': self.id,
                    'planned_amount': line.planned_amount,

                }
                record = self.env['budget.forecast']
                record.create(forecast_line)
                # self.forecast_done = True


class CrossoveredBudgetLines(models.Model):
    _inherit = 'budget.lines'

    released_amount = fields.Monetary(
        string='Released Amount',compute='_compute_released_amount',
        required=False, store=True )
    practical_amount = fields.Monetary(
        compute='_compute_practical_amount', string='Actual Amount', help="Amount really earned/spent.")
    actual_amount = fields.Monetary(
        compute='_compute_actual_amount', string='Amount Utilised', help="Amount really earned/spent.")
    planned_amount = fields.Monetary(
        'Budgeted Amount', required=True,
        help="Amount you plan to earn/spend. Record a positive amount if it is a revenue and a negative amount if it is a cost.")
    percentage = fields.Float(
        compute='_compute_percentage', string='Percentage on Budgeted',
        help="Comparison between practical and planned amount. This measure tells you if you are below or over budget.")
    percentage_released = fields.Float(
        compute='_compute_percentage_released', string='Percentage on Released',
        help="Comparison between practical and released amount. This measure tells you if you are below or over budget.")
    company_id = fields.Many2one('res.company', string='', required=True, readonly=True,
                                 default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one('res.currency', compute='_compute_currency', store=True, string="Currency")


    @api.depends('company_id')
    def _compute_currency(self):
        self.currency_id = self.company_id.currency_id or self.env.user.company_id.currency_id

    # the percentage field was reworked to compute against the planned amount instead of theoretical

    def _compute_percentage(self):
        for line in self:
            if line.planned_amount != 0.00:
                line.percentage = float((line.actual_amount or 0.0) / line.planned_amount)
            else:
                line.percentage = 0.00

    def _compute_percentage_released(self):
        for line in self:
            if line.released_amount != 0.00:
                line.percentage_released = float((line.actual_amount or 0.0) / line.released_amount)
            else:
                line.percentage_released = 0.00

    @api.onchange('practical_amount')
    def _compute_actual_amount(self):
        for line in self:
            if line.practical_amount:
                line.actual_amount = abs(line.practical_amount)

    @api.depends('analytic_account_id.budget_releases')
    def _compute_released_amount(self):
        for line in self:
            if line.analytic_account_id:
                releases = []
                for release in line.analytic_account_id.budget_releases:
                    releases.append(release.amount)
                    line.released_amount = sum(releases)


class BudgetForecast(models.Model):
    _name = 'budget.forecast'
    _description = 'Budget forecast table'

    budget_line = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Budget_line',
        required=False)
    budget_id = fields.Many2one(comodel_name='budget.budget', string="Budget")
    currency_id = fields.Many2one('res.currency', compute='_compute_currency', store=True, string="Currency")
    company_id = fields.Many2one('res.company', string='Branch', required=True, readonly=True,
                                 default=lambda self: self.env.user.company_id)
    planned_amount = fields.Monetary(
        'Budgeted Amount', required=True,
        )
    january = fields.Monetary(
        'January', required=False,
        )
    february = fields.Monetary(
        'February', required=False,
        )
    march = fields.Monetary(
        'March', required=False,
        )
    april = fields.Monetary(
        'April', required=False,
        )
    may = fields.Monetary(
        'May', required=False,
        )
    june = fields.Monetary(
        'june', required=False,
        )
    july = fields.Monetary(
        'July', required=False,
        )
    august = fields.Monetary(
        'August', required=False,
        )
    september = fields.Monetary(
        'September', required=False,
        )
    october = fields.Monetary(
        'October', required=False,
        )
    november = fields.Monetary(
        'November', required=False,
        )
    december = fields.Monetary(
        'December', required=False,
        )

    @api.depends('company_id')
    def _compute_currency(self):
        self.currency_id = self.company_id.currency_id or self.env.user.company_id.currency_id




