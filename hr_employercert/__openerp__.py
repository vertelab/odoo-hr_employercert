# -*- coding: utf-8 -*-
##############################################################################
#
#   www.vertel.se
#
##############################################################################

{
    'name': 'Employment Certificates',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """
Manage your employee.
=========================================================================================================
    """,
    'author': 'Vertel AB',
    'website': 'http://www.vertel.se',
    'depends': ['hr_attendance', 'hr_timesheet', 'hr_contract', 'hr_payroll', 'hr_holidays', 'resource', 'mail'],
    'data': ['hr_employercert_view.xml',
       ],
    #'demo': [''],
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
