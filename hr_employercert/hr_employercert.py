# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
import openerp.tools
from datetime import datetime
import time
import re

class hr_attendance(models.Model):
    #_inherit = ['hr.attendance', 'mail.thread']
    _inherit = 'hr.attendance'

    @api.one
    def _working_hours(self):
        contract = self.employee_id.contract_ids[0] if self.employee_id and self.employee_id.contract_ids else False
        if contract:
            self.working_hours_on_day = self.pool.get('resource.calendar').working_hours_on_day(self.env.cr, self.env.uid,
                contract.working_hours, fields.Datetime.from_string(self.name))
        else:
            self.working_hours_on_day = 0.0

    working_hours_on_day = fields.Float(compute='_working_hours', string='Planned Hours')
    over_hours = fields.Float(default=0.0)
    absent_hours = fields.Float(default=0.0)
