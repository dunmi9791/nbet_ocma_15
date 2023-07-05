# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class RankRank(models.Model):
    _name = "rank.rank"
    _description = "Rank"

    name = fields.Char()
    description = fields.Text()
    salary_range = fields.Float(string="Salary", required=True)
    active = fields.Boolean('Active',default=True)
    grade_id = fields.Many2one("grade.grade", "Grade", required=True)



class GradeGrade(models.Model):
    _name = "grade.grade"
    _description = "Grade"

    name = fields.Char()
    description = fields.Text()
    rank_ids = fields.One2many("rank.rank", "grade_id", "Rank")
    active = fields.Boolean('Active',default=True)


class HrEmployee(models.Model):

    _inherit = "hr.employee"

    grade_id = fields.Many2one("grade.grade", "Grade")
    rank_id = fields.Many2one("rank.rank", "Rank")
    

    @api.onchange("grade_id")
    def _onchange_grade(self):
        res = {}
        if self.grade_id:
            self.rank_id = False
            res["domain"] = {"rank_id": [
                ("id", "in", self.grade_id.rank_ids.ids)]}
        return res
