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
    def _planned_hours(self):
        contract = self.employee_id.contract_ids[0] if self.employee_id and self.employee_id.contract_ids else False
        if contract:
            working_hours_on_day = self.pool.get('resource.calendar').working_hours_on_day(self.env.cr, self.env.uid, 
                                                                                            contract.working_hours,
                                                                                            fields.Datetime.from_string(self.name))
        else:
            working_hours_on_day = 0.0
            
    def get_working_hours(self, cr, uid, id, start_dt, end_dt, compute_leaves=False,
                          resource_id=None, default_interval=None, context=None):
        hours = 0.0
        for day in rrule.rrule(rrule.DAILY, dtstart=start_dt,
                               until=(end_dt + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0),
                               byweekday=self.get_weekdays(cr, uid, id, context=context)):
            day_start_dt = day.replace(hour=0, minute=0, second=0)
            if start_dt and day.date() == start_dt.date():
                day_start_dt = start_dt
            day_end_dt = day.replace(hour=23, minute=59, second=59)
            if end_dt and day.date() == end_dt.date():
                day_end_dt = end_dt
            hours += self.get_working_hours_of_date(
                cr, uid, id, start_dt=day_start_dt, end_dt=day_end_dt,
                compute_leaves=compute_leaves, resource_id=resource_id,
                default_interval=default_interval,
                context=context)
        return hours
        
    def _over_hours(self):
        self.over_hours = _working_hours(self) - get_working_hours(self)

    planned_hours = fields.Float(compute='_planned_hours')
    over_hours = fields.Float(default=0.0)
    absent_hours = fields.Float(default=0.0)
