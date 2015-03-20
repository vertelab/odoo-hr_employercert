import datetime
import time
from openerp import api, models

class employee_report_print(models.AbstractModel):
    _name = 'report.hr_employercert.report_employeereport'
    
    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('hr_employercert.report_attendanceerrors')
        docargs = {
            #~ 'doc_ids': self._ids,
            #~ 'doc_model': report.model,
            #~ 'docs': self,
        }
        return report_obj.render('hr_employercert.report_attendanceerrors', docargs)

        
class report_hr_employeereport(osv.AbstractModel):
    _name = 'report.hr_employercert.report_employeereport'
    _inherit = 'report.abstract_report'
    _template = 'hr_employercert.report_attendanceerrors'
    _wrapped_report_class = employee_report_print
