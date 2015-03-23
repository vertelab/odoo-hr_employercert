import datetime
import time
from openerp import api, models
import logging
from openerp.osv import osv
from openerp.report import report_sxw
_logger = logging.getLogger(__name__)

class employee_report_print(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(employee_report_print, self).__init__(cr, uid, name, context=context)
        report_table = []
        for month in [('Jan','0101','0131'),('Feb','0201','0229'),('Mar','0301','0331')]:
            for attendance in self.env['hr.attendance'].search([('employee_id', '=', self.id),('name','>=',month[1]),('name','<=',month[2])]):
                self.worked_hours += attendance.worked_hours
                self.over_hours += attendance.over_hours
            report_table.append({
                'label': month[0],
                'working_hours_on_day': self.env['resource.calendar'].working_hours_on_day(self.env.cr, self.env.uid, contract.working_hours, fields.Datetime.from_string(self.name)),
                'worked_hours': self.worked_hours,
                'over_hours': self.over_hours,
                'absent_hours': self.working_hours_on_day - self.worked_hours,
            })
        self.localcontext.update({
            'time': time,
            'get_employees':self._get_employees,
            'report_table': report_table,
        })

    def _get_employees(self, emp_ids):
        emp_obj_list = self.pool.get('hr_employercert.report_employeereport').browse(self.cr, self.uid, emp_ids)
        return emp_obj_list


class report_hr_employeereport(osv.AbstractModel):
    _name = 'report.hr_employercert.report_employeereport'
    _inherit = 'report.abstract_report'
    _template = 'hr_employercert.report_employeereport'
    _wrapped_report_class = employee_report_print

#~ class report_hr_employeereport(models.AbstractModel):
    #~ _name = 'report.hr_employercert.report_employeereport'
    #~ _inherit = 'report.abstract_report'
    #~ _template = 'hr_employercert.report_employeereport'
    #~ _wrapped_report_class = employee_report_print


#~ class AbstractReport(models.AbstractModel):
    #~ _name = 'report.hr_employercert.report_employeereport'
    #~ _inherit = 'report.abstract_report'
#~ 
    #~ @api.multi
    #~ def render_html(self, data=None):
        #~ _logger.info("What the hell is going on here??")
        #~ report_obj = self.env['report']
        #~ report = report_obj._get_report_from_name('hr_employercert.report_employeereport')
        #~ attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id)])
        #~ report_table = []
        #~ for month in [('Jan','0101','0131'),('Feb','0201','0229'),('Mar','0301','0331')]:
            #~ for attendance in self.env['hr.attendance'].search([('employee_id', '=', self.id),('name','>=',month[1]),('name','<=',month[2])]):
                #~ self.worked_hours += attendance.worked_hours
                #~ self.over_hours += attendance.over_hours
            #~ report_table.append({
                #~ 'label': month[0],
                #~ 'working_hours_on_day': self.env['resource.calendar'].working_hours_on_day(self.env.cr, self.env.uid, contract.working_hours, fields.Datetime.from_string(self.name)),
                #~ 'worked_hours': self.worked_hours,
                #~ 'over_hours': self.over_hours,
                #~ 'absent_hours': self.working_hours_on_day - self.worked_hours,
            #~ })
        #~ docargs = {
            #~ 'doc_ids': self._ids,
            #~ 'doc_model': report.model,
            #~ 'docs': self,
            #~ 'report_table': report_table
        #~ }
        #~ return report_obj.render('hr_employercert.report_employeereport', docargs)
