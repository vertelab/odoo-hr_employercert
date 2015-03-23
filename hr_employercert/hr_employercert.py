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
    def _working_hours_on_day(self): # working hours on the contract
        contract = self.employee_id.contract_ids[0] if self.employee_id and self.employee_id.contract_ids else False
        if contract and self.action == 'sign_out':
            self.working_hours_on_day = self.pool.get('resource.calendar').working_hours_on_day(self.env.cr, self.env.uid,
                contract.working_hours, fields.Datetime.from_string(self.name))
        else:
            self.working_hours_on_day = 0.0

    @api.one
    def _get_working_hours(self): # worked hours in schedule
        contract = self.employee_id.contract_ids[0] if self.employee_id and self.employee_id.contract_ids else False
        if contract and self.action == 'sign_out':
            _logger.info("get_working_hours %s" % self.pool.get('resource.calendar').get_working_hours(
                self.env.cr, self.env.uid,
                self.employee_id.contract_ids[0].working_hours.id, datetime.strptime(
                self._last_signin()[0], tools.DEFAULT_SERVER_DATETIME_FORMAT),
                datetime.strptime(self.name, tools.DEFAULT_SERVER_DATETIME_FORMAT)))
            self.get_working_hours = self.pool.get('resource.calendar').get_working_hours(self.env.cr, self.env.uid,
                self.employee_id.contract_ids[0].working_hours.id,
                datetime.strptime(self._last_signin()[0], tools.DEFAULT_SERVER_DATETIME_FORMAT),
                datetime.strptime(self.name, tools.DEFAULT_SERVER_DATETIME_FORMAT))
        else:
            self.get_working_hours = False

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
        else:
            pass

    #~ @api.one
    #~ def _in_schedule_hours(self):    # worked hours in schedule
        #~ contract = self.employee_id.contract_ids[0] if self.employee_id and self.employee_id.contract_ids else False
        #~ if contract and self.action == 'sign_out':
            #~ _logger.info("get_working_intervals_of_day %s" % self.pool.get('resource.calendar').get_working_intervals_of_day(
                #~ self.env.cr, self.env.uid,
                #~ self.employee_id.contract_ids[0].working_hours.id, datetime.strptime(
                #~ self._last_signin()[0], tools.DEFAULT_SERVER_DATETIME_FORMAT),
                #~ datetime.strptime(self.name, tools.DEFAULT_SERVER_DATETIME_FORMAT)))
            #~ self.in_schedule_hours = 0.0
            #~ for t in self.pool.get('resource.calendar').get_working_intervals_of_day(
                #~ self.env.cr, self.env.uid,
                #~ self.employee_id.contract_ids[0].working_hours.id,
                #~ datetime.strptime(self._last_signin()[0], tools.DEFAULT_SERVER_DATETIME_FORMAT),
                #~ datetime.strptime(self.name, tools.DEFAULT_SERVER_DATETIME_FORMAT)):
                #~ self.in_schedule_hours += (t[1] - t[0]).seconds / 3600.0
        #~ else:
            #~ self.in_schedule_hours = False
                
    @api.one
    def _over_hours(self):    # overtime hours
        contract = self.employee_id.contract_ids[0] if self.employee_id and self.employee_id.contract_ids else False
        if contract and self.action == 'sign_out':
            t = self.pool.get('resource.calendar').get_working_intervals_of_day(
                self.env.cr, self.env.uid,
                self.employee_id.contract_ids[0].working_hours.id)
            if len(t) > 0:
                if datetime.strptime(self._last_signin()[0], tools.DEFAULT_SERVER_DATETIME_FORMAT) < t[0][0]:
                    self.over_hours += (t[0][0] - datetime.strptime(self._last_signin()[0], tools.DEFAULT_SERVER_DATETIME_FORMAT)).seconds / 3600.0
                if datetime.strptime(self.name, tools.DEFAULT_SERVER_DATETIME_FORMAT) > t[-1][1]:
                    self.over_hours += (datetime.strptime(self.name, tools.DEFAULT_SERVER_DATETIME_FORMAT) - t[-1][1]).seconds / 3600.0
            else:
                self.over_hours = False
        else:
            self.over_hours = False
            
    #~ @api.one
    #~ def _absent_hours(self):    # absent hours
        #~ contract = self.employee_id.contract_ids[0] if self.employee_id and self.employee_id.contract_ids else False
        #~ if contract and self.action == 'sign_out':
            #~ _logger.info("get_working_hours %s" % self.pool.get('resource.calendar').get_working_intervals_of_day(
                #~ self.env.cr, self.env.uid,
                #~ self.employee_id.contract_ids[0].working_hours.id,
                #~ datetime.strptime(self._last_signin()[0], tools.DEFAULT_SERVER_DATETIME_FORMAT),
                #~ datetime.strptime(self.name, tools.DEFAULT_SERVER_DATETIME_FORMAT)))
            #~ t = self.pool.get('resource.calendar').get_working_intervals_of_day(
                #~ self.env.cr, self.env.uid,
                #~ self.employee_id.contract_ids[0].working_hours.id,
                #~ datetime.strptime(self._last_signin()[0], tools.DEFAULT_SERVER_DATETIME_FORMAT),
                #~ datetime.strptime(self.name, tools.DEFAULT_SERVER_DATETIME_FORMAT))
            #~ if len(t) > 0:
                #~ if datetime.strptime(self._last_signin()[0], tools.DEFAULT_SERVER_DATETIME_FORMAT) > t[0][0]:
                    #~ self.absent_hours += (datetime.strptime(self._last_signin()[0], tools.DEFAULT_SERVER_DATETIME_FORMAT) - t[0][0]).seconds / 3600.0
                #~ if datetime.strptime(self.name, tools.DEFAULT_SERVER_DATETIME_FORMAT) < t[-1][1]:
                    #~ self.absent_hours += (t[-1][1] - datetime.strptime(self.name, tools.DEFAULT_SERVER_DATETIME_FORMAT)).seconds / 3600.0
            #~ else:
                #~ self.absent_hours = False
        #~ else:
            #~ self.absent_hours = False

    working_hours_on_day = fields.Float(compute='_working_hours_on_day', string='Planned Hours')
    get_working_hours = fields.Float(compute='_get_working_hours', string='Worked in schedule (h)')
    #in_schedule_hours = fields.Float(compute='_in_schedule_hours', string='Worked in schedule (h)')
    over_hours = fields.Float(compute='_over_hours', string='Over time (h)')
    #absent_hours = fields.Float(compute='_absent_hours', string='Absent time (h)')
    last_signin = fields.Datetime(compute='_last_signin')

class hr_employee(models.Model):
    _inherit = 'hr.employee'


class ParticularReport(models.AbstractModel):
    _name = 'report.hr_employercert.report_employeereport'
    @api.multi
    def render_html(self, data=None):
        _logger.info("Yee im in report")
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('hr_employercert.report_employeereport')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self.env['hr.employee'].search([]),
            'hr_attendance': self.env['hr.attendance'].search([]),
        }
        return report_obj.render('hr_employercert.report_employeereport', docargs)
