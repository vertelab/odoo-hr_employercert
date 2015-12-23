# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015- Vertel AB (<http://www.vertel.se>).
#
#    This progrupdateam is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

        
class hr_contract(models.Model):
    _inherit = "hr.contract"

    training_program = fields.Char(string="Training program")
    work_description = fields.Text(string="Work Description",help="brief description of the example tasks, organizational placement, powers, special assignments and projects")
    work_skills = fields.Text(string="Skills",help="the required skills such as proficiency, experience and training as well as the personal qualities required in this position such as accuracy, speed, responsibility, ability to organize, prioritize, decide, plan, communicate, motivate staff, follow up as well as creative skills")
    work_performance = fields.Text(string="Performance",help="description of tasks performed and how well the skills requirements (see above) have been met. Short description of the personal qualities and skills that are relevant to the work")
        

