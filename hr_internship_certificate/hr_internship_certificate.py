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
    work_description = fields.Text(string="Work Description",help="brief description of the example tasks, organizational placement, powers, special assignments and projects\nYou can use {name} and {gender_he/gender_He/gender_his/gender_His} (he/she,He/She,his/her,His/Her) ")
    work_description_legend = fields.Text(string="Legend",readonly=True, size=100,default=_("""
1. Responsibilities and powers that work includes 
2. Organizational positioning 
3. Short description of the duties
4. Information on where the work was performed 
5. Others, such special assignments as the employee had

Examples of how the job description might look like:
    %(name)s has alone been responsible for planning and scheduling work for the company's five operators. 
    %(gender_he)s has also actively participated in the daily work to manage the XXX in an optimal manner
    to ensure that it has been short response times. %(name)s has during his time at the company thanks 
    several times been named the company's best operator. The work has been based at the company headquarters in XXX.
"""))
    work_skills = fields.Text(string="Skills",help="the required skills such as proficiency, experience and training as well as the personal qualities required in this position such as accuracy, speed, responsibility, ability to organize, prioritize, decide, plan, communicate, motivate staff, follow up as well as creative skills")
    work_skills_legend = fields.Text(string="Legend",readonly=True, size=100,default=_("""
Requirements for service is often three to four sentences long.

     Requirements for the service:
     1. Competence & Qualifications (Includes information about educational requirements and experience requirements)
     2. Requirements for personal characteristics (eg Can be any of the following;
     analytical ability, work capacity, commitment, flexibility, ability to teach, ability to prioritize, initiative, communication skills, contact skills,
     logical thinking, memory, verbal presentation, judgment, order, popularity among clients and colleagues, commitment,
     sammarbetsförmåga, Independence, written expression, stability, stress resistance, structured, behavior,
     stamina, vitality)

Examples of the "requirements" service could look like:
The position requires knowledge of maligned's gear and high stress resistance and an ability to verbal contacts with customers as well as with its own staff.

"""))
    work_performance = fields.Text(string="Performance",help="description of tasks performed and how well the skills requirements (see above) have been met. Short description of the personal qualities and skills that are relevant to the work")
    work_performance_legend = fields.Text(string="Legend",readonly=True, size=100,default=_("""
    
    %(name)s has during %(gender_his)s time at the company has been highly appreciated by clients
    and colleagues alike for his pleasant manner as for %(gender_his)s knowledge of <some skill>. 
    %(name)s has with great accuracy and with great interest in performing %(gender_his)s tasks 
    to our complete satisfaction. %(gender_He)s has been very enterprising and responsible. 
    When %(gender_he)s is also very easy to collaborate with, we want to give %(gender_him)s 
    the our very best recommendations.

    poor:                    We wish %(name)s luck with future tasks.
    better:                  We can leave %(gender_him)s our recommendations.
                             We can leave %(gender_him)s our best recommendations.
                             We can gladly give %(gender_him)s our best recommendations.
    best:                    We can leave %(gender_him)s our very best recommendations.
                             We can gladly give %(gender_him)s our very best recommendations.
"""))
    termination_reason = fields.Text(string="Resason for termination")
    leave_of_absence = fields.Text(string="Leave of absence",help="Longer leave of absence have to be documented")
    
    
    @api.one
    def _get_formatted(self):
        f = {
            'name': self.employee_id.name,
            'gender_He': self.get_he().capitalize(),
            'gender_he': self.get_he(),
            'gender_His': self.get_his().capitalize(),
            'gender_his': self.get_his(),
            'gender_Him': self.get_him().capitalize(),
            'gender_him': self.get_him(),
            'identification_id': self.employee_id.identification_id,
            'date_start': self.trial_date_start if self.trial_date_start else self.date_start,
            'date_end': self.date_end if self.date_end else self.trial_date_end,
            'termination_reason': self.termination_reason,
            'leave_of_absence': self.leave_of_absence,
            'title': self.job_id.name,
            'training_program': self.training_program,
            'working_hours': self.working_hours,
            'work_location': self.employee_id.work_location,
            'company_name': self.employee_id.address_id.company_id.name,
            'company_registry': self.employee_id.address_id.company_id.company_registry,
            'company_description': self.employee_id.address_id.company_id.description,
            'company_department': self.employee_id.department_id.name,
            'coach_title': self.employee_id.coach_id.job_id.name if self.employee_id.coach_id else self.employee_id.parent_id.job_id.name,
            'coach_name': self.employee_id.coach_id.name if self.employee_id.coach_id else self.employee_id.parent_id.name,
            'coach_phone': self.employee_id.coach_id.work_phone if self.employee_id.coach_id else self.employee_id.parent_id.work_phone,
            'coach_mobile': (self.employee_id.coach_id.mobile_phone if self.employee_id.coach_id else self.employee_id.parent_id.mobile_phone) or '',
            'coach_email': self.employee_id.coach_id.work_email if self.employee_id.coach_id else self.employee_id.parent_id.work_email,
        }
        f.update({                
            'work_description': self.work_description % f if self.work_description else '',
            'work_skills': self.work_skills % f if self.work_skills else '',
            'work_performance': self.work_performance % f if self.work_performance else '',
            })
        if self.type_id.certification_letter:
            self.certification_letter = self.type_id.certification_letter % f
        else:
            self.certification_letter = """<h1>Employee Certificate</h1>
<p>%(name)s, %(identification_id)s, have, has been employed
by %(company_name)s from %(date_start)s to %(date_end)s
in the position of %(title)s.
</p>
<p>
During the employment the main duties of %(gender_him)s where %(work_description)s
</p>
<p>
To fullfill this type of work the required skills are %(work_skills)s 
</p>
<p>
%(work_performance)s
</p>
<p>
We take advantage of this oportunity to thank %(name)s for the excellence and quality of the work
%(gender_he)s has accomplished within our company and wish %(gender_him)s all the best for both %(gender_his)s professional and personal future.
</p>
<br />
<br />
<br />
<br />
<br />
<br />
<br />
<br />
%(coach_name)s<br>
%(coach_title)s<br>
%(company_name)s<br>
%(coach_phone)s<br>
%(coach_mobile)s<br>
%(coach_email)s<br>""" % f
        self.certification_letter_short = """<h1>Employee Certificate</h1>
<p>%(name)s, %(identification_id)s, have, has been employed
by %(company_name)s from %(date_start)s to %(date_end)s
in the position of %(title)s.
</p>
<p>
During the employment the main duties of %(gender_him)s where %(work_description)s
</p>
<p>
To fullfill this type of work the required skills are %(work_skills)s 
</p>
<p>
%(work_performance)s
</p>
<p>
We take advantage of this oportunity to thank %(name)s for the excellence and quality of the work
%(gender_he)s has accomplished within our company and wish %(gender_him)s all the best for both %(gender_his)s professional and personal future.
</p>
<br />
<br />
<br />
<br />
<br />
<br />
<br />
<br />
%(coach_name)s<br>
%(coach_title)s<br>
%(company_name)s<br>
%(coach_phone)s<br>
%(coach_mobile)s<br>
%(coach_email)s<br>""" % f
    certification_letter = fields.Text(compute="_get_formatted")
    certification_letter_short = fields.Text(compute="_get_formatted")


    @api.onchange('job_id')
    def change_job(self):
        self.work_description = self.job_id.description
        self.work_skills = self.job_id.requirements

    def get_he(self):
        return  _('he') if not self.employee_id.gender or self.employee_id.gender == 'male' else _('she')
    def get_his(self):
        return  _('his') if not self.employee_id.gender or self.employee_id.gender == 'male' else _('her')
    def get_him(self):
        return  _('him') if not self.employee_id.gender or self.employee_id.gender == 'male' else _('her')
        
class hr_contract_type(models.Model):
    _inherit = "hr.contract.type"
    
    certification_letter = fields.Html(string="Certification Letter",help="This is a employee certification")
    service_record = fields.Html(string="Service record",help="This is a employee certification usually including work_performance")
    
    certificate_legend = fields.Text(string="Legend",readonly=True, size=100,default=_("""You can specify several variables in the letter using the following labels:\n\n

    %(name)s                 Name of employee
    %(identification_id)s    id-number for employee
    %(gender_xxx)s           He/he/His/his prints He or She according to gender
    %(date_xxx)s             start/end date or trial date for the employment
    %(title)s                Job name
    %(training_program)s     Training program from contract (usually in the framework of an internship)
    %(company_xxx)s          name/department/registry/description for company
    %(work_xxx)s             Work description/skills/performance from contract
    %(work_location)s        Work location for employee
    %(coach_xxx)s            Coach / Manager title/name/phone/mobile/email
    
    %(termination_reason)s   Reason for termination of contract
    %(leave_of_absence)s     If there have been any longer leave of absence
    %(working_hours)s        Working hours / full time, half etc

    %(work_description)s     Job description
    %(work_skills)s          Requested skills for the job-title
    %(work_performance)s     Service record

"""))

class res_company(models.Model):
    _inherit = "res.company"
    
    description = fields.Text(string="Short description")

