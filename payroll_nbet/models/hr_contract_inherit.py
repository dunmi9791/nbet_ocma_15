from odoo import api, fields, models


class GradeRank(models.Model):
    _inherit = 'rank.rank'

    salary = fields.Float(string='Salary')


class HrContractInherit(models.Model):
    _inherit = 'hr.contract'

    wage = fields.Float(compute='_compute_wage')

    @api.depends('employee_id.rank_id.salary_range')  # Add the fields that the wage depends on.
    def _compute_wage(self):
        for record in self:
            # Add your computation logic here.
            record.wage = record.employee_id.rank_id.salary_range / 12
