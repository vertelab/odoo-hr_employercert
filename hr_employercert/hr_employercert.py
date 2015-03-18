# -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
import openerp.tools
from datetime import datetime, timedelta
import time
import re

import logging
_logger = logging.getLogger(__name__)

class hr_attendance(models.Model):
    #_inherit = ['hr.attendance', 'mail.thread']
    _inherit = 'hr.attendance'

    @api.one
    def _compute_working_calendar(self):    # working schadule in contract
        contract = self.employee_id.contract_ids[0] if self.employee_id and self.employee_id.contract_ids else False
        if contract and self.action == 'sign_out':
            self.compute_working_calendar = self.pool.get('resource.resource').compute_working_calendar(self.env.cr, self.env.uid)[3]
        else:
            self.compute_working_calendar = None

    @api.one
    def _working_hours_on_day(self): # working hours on the contract
        contract = self.employee_id.contract_ids[0] if self.employee_id and self.employee_id.contract_ids else False
        if contract and self.action == 'sign_out':
            self.working_hours_on_day = self.pool.get('resource.calendar').working_hours_on_day(self.env.cr, self.env.uid,
                contract.working_hours, fields.Datetime.from_string(self.name))
        else:
            self.working_hours_on_day = 0.0

    @api.one
    def _last_signin(self): # last sign in time
        if self.action == 'sign_in':
            self.last_signin = 0
        elif self.action == 'sign_out':
            last_signin = self.search([
                ('employee_id', '=', self.employee_id.id),
                ('name', '<', self.name), ('action', '=', 'sign_in')
            ], limit=1, order='name DESC')
            if last_signin:
                return last_signin.name

    @api.one
    def _in_schedule_hours(self):    # actually work hours of an employee
        if self.action == 'sign_out':
            contract = self.employee_id.contract_ids[0] if self.employee_id and self.employee_id.contract_ids else False
            _logger.info("get_working_intervals_of_day %s" % self.pool.get('resource.calendar').get_working_intervals_of_day(
                self.env.cr, self.env.uid,
                self.employee_id.contract_ids[0].working_hours.id, datetime.strptime(
                self._last_signin()[0], tools.DEFAULT_SERVER_DATETIME_FORMAT),
                datetime.strptime(self.name, tools.DEFAULT_SERVER_DATETIME_FORMAT)))
            self.in_schedule_hours = 0.0
            for t in self.pool.get('resource.calendar').get_working_intervals_of_day(
                self.env.cr, self.env.uid,
                self.employee_id.contract_ids[0].working_hours.id,
                datetime.strptime(self._last_signin()[0], tools.DEFAULT_SERVER_DATETIME_FORMAT),
                datetime.strptime(self.name, tools.DEFAULT_SERVER_DATETIME_FORMAT)):
                self.in_schedule_hours += (t[1] - t[0]).seconds / 3600.0
                
    
    working_hours_on_day = fields.Float(compute='_working_hours_on_day', string='Planned Hours')
    #compute_working_calendar = fields.Text(compute='_compute_working_calendar', string='compute_working_calendar')
    in_schedule_hours = fields.Float(compute='_in_schedule_hours', string='Worked in schedule (h)')
    over_hours = fields.Float(default=0.0, string='Over time (h)')
    absent_hours = fields.Float(default=0.0, string='Absent time (h)')
    last_signin = fields.Datetime(compute='_last_signin')

