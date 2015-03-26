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

    working_hours_on_day = fields.Float(compute='_working_hours_on_day', string='Planned Hours')
    get_working_hours = fields.Float(compute='_get_working_hours', string='Worked in schedule (h)')
    over_hours = fields.Float(compute='_over_hours', string='Over time (h)')
    last_signin = fields.Datetime(compute='_last_signin')

class hr_employee(models.Model):
    _inherit = 'hr.employee'

class EmployeeReport(models.AbstractModel):
    _name = 'report.hr_employercert.report_employeereport'

    @api.multi
    def render_html(self, data=None):
        _logger.info("Reporting")
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('hr_employercert.report_employeereport')
        for emp in self.env['hr.employee'].browse(self._ids):
            attendance = emp.env['hr.attendance'].search([('employee_id', '=', emp.id)])
            contract = emp.contract_ids[0] if emp.contract_ids else False
            report_table_first = []
            report_table_last = []
            if contract.date_end:
                year_begin = datetime.strptime(contract.date_start + ' 00:00:00', tools.DEFAULT_SERVER_DATETIME_FORMAT).year
                year_end = datetime.strptime(contract.date_end + ' 00:00:00', tools.DEFAULT_SERVER_DATETIME_FORMAT).year
                if year_begin == fields.datetime.today().year or year_begin == year_end:
                    last_year = year_begin
                    first_year = year_begin
                elif year_end <= fields.datetime.today().year:
                    last_year = year_end
                    first_year = last_year - 1
                elif year_end > fields.datetime.today().year and year_begin < fields.datetime.today().year:
                    last_year = fields.datetime.today().year
                    first_year = last_year - 1
                else:   # if both begin date and end date are after this year
                    first_year = fields.datetime.today().year
                    last_year = fields.datetime.today().year
            else:
                year_begin = datetime.strptime(contract.date_start + ' 00:00:00', tools.DEFAULT_SERVER_DATETIME_FORMAT).year
                if year_begin == fields.datetime.today().year:
                    last_year = year_begin
                    first_year = year_begin
                elif year_begin < fields.datetime.today().year:
                    last_year = fields.datetime.today().year
                    first_year = last_year - 1
                else:   # if begin date is after this year
                    first_year = fields.datetime.today().year
                    last_year = fields.datetime.today().year
                
            for year in [first_year]:
                for day in [('Jan','-01-01 00:00:00','-01-31 23:59:59'),('Feb','-02-01 00:00:00','-03-01 23:59:59'),
                            ('Mar','-03-01 00:00:00','-03-31 23:59:59'),('Apr','-04-01 00:00:00','-04-30 23:59:59'),
                            ('May','-05-01 00:00:00','-05-31 23:59:59'),('Jun','-06-01 00:00:00','-06-30 23:59:59'),
                            ('Jul','-07-01 00:00:00','-07-31 23:59:59'),('Aug','-08-01 00:00:00','-08-31 23:59:59'),
                            ('Sep','-09-01 00:00:00','-09-30 23:59:59'),('Oct','-10-01 00:00:00','-10-31 23:59:59'),
                            ('Nov','-11-01 00:00:00','-11-30 23:59:59'),('Dec','-12-01 00:00:00','-12-31 23:59:59'),
                            ]:
                    start_day = str(year) + day[1]
                    if day[0] == _('Feb'):
                        end_day = '%s-02-%s 23:59:59' % (year, (datetime(year, 3, 1) - timedelta(days = 1)).day)
                    else:
                        end_day = str(year) + day[2]
                    _logger.info('start_day: %s end_day: %s' % (start_day, end_day))
                    worked_hours = 0.0
                    over_hours = 0.0
                    for a in emp.env['hr.attendance'].search([('employee_id', '=', emp.id),
                                                                ('name','>=',start_day),
                                                                ('name','<=',end_day)]):
                        worked_hours += a.worked_hours
                        over_hours += a.over_hours
                        
                    planned_ids = contract.working_hours.get_working_hours(fields.Datetime.from_string(start_day), fields.Datetime.from_string(end_day)),
                    for p in planned_ids:
                        planned_hours = p[0]
                    _logger.info('planned_hours: %s worked_hours: %s' % (planned_hours, worked_hours))
                    report_table_first.append({
                        'label': day[0],
                        'planned_hours': planned_hours,
                        'worked_hours': '%.2f' % worked_hours,
                        'over_hours': '%.2f' % over_hours,
                        'absent_hours': '%.2f' % (planned_hours - worked_hours),
                    })
                    
            for year in [last_year]:
                for day in [('Jan','-01-01 00:00:00','-01-31 23:59:59'),('Feb','-02-01 00:00:00','-03-01 23:59:59'),
                            ('Mar','-03-01 00:00:00','-03-31 23:59:59'),('Apr','-04-01 00:00:00','-04-30 23:59:59'),
                            ('May','-05-01 00:00:00','-05-31 23:59:59'),('Jun','-06-01 00:00:00','-06-30 23:59:59'),
                            ('Jul','-07-01 00:00:00','-07-31 23:59:59'),('Aug','-08-01 00:00:00','-08-31 23:59:59'),
                            ('Sep','-09-01 00:00:00','-09-30 23:59:59'),('Oct','-10-01 00:00:00','-10-31 23:59:59'),
                            ('Nov','-11-01 00:00:00','-11-30 23:59:59'),('Dec','-12-01 00:00:00','-12-31 23:59:59'),
                            ]:
                    start_day = str(year) + day[1]
                    if day[0] == _('Feb'):
                        end_day = '%s-02-%s 23:59:59' % (year, (datetime(year, 3, 1) - timedelta(days = 1)).day)
                    else:
                        end_day = str(year) + day[2]
                    _logger.info('start_day: %s end_day: %s' % (start_day, end_day))
                    worked_hours = 0.0
                    over_hours = 0.0
                    for a in emp.env['hr.attendance'].search([('employee_id', '=', emp.id),
                                                                ('name','>=',start_day),
                                                                ('name','<=',end_day)]):
                        worked_hours += a.worked_hours
                        over_hours += a.over_hours
                        
                    planned_ids = contract.working_hours.get_working_hours(fields.Datetime.from_string(start_day), fields.Datetime.from_string(end_day)),
                    for p in planned_ids:
                        planned_hours = p[0]
                    _logger.info('planned_hours: %s worked_hours: %s' % (planned_hours, worked_hours))
                    report_table_last.append({
                        'label': day[0],
                        'planned_hours': planned_hours,
                        'worked_hours': '%.2f' % worked_hours,
                        'over_hours': '%.2f' % over_hours,
                        'absent_hours': '%.2f' % (planned_hours - worked_hours),
                    })

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self.env['hr.employee'].browse(self._ids),
            'report_table_first': report_table_first,
            'report_table_last': report_table_last,
        }
        return report_obj.render('hr_employercert.report_employeereport', docargs)
