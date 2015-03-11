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

More information:
    """,
    'author': 'Vertel AB',
    'website': 'http://www.vertel.se',
    'depends': ['hr_attendance', 'mail'],
    'data': ['hr_employercert_view.xml',
       ],
    #'demo': ['hr_employercert_demo.xml'],
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
