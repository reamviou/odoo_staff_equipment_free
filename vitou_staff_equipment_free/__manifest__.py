# -*- coding: utf-8 -*-
###############################################################################
#
#    Copyright (C) 2024-TODAY,
#    Author: REAM Vitou (reamvitou@yahoo.com)
#    Tel: +855 17 82 66 82


###############################################################################

{
    'name': 'Staff Equipments Free',
    'version': '18.0.1.0.1',
    'category': 'Human Resources',
    'summary': "Staff Equipments",
    'description': "This is for control staff equipments",
     'author': 'V Technologies',
    'company': 'V Technologies',
    'maintainer': 'V Technologies',
    'website': 'https://apps.odoo.com/apps/modules/browse?search=vitou',
    # 'price': '30',
    # 'currency': 'USD',
    'module_type': 'official',
    'depends': ['base_setup', 'hr_attendance', 'hr'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'data/cron.xml',

        # data
        'data/developer_default.xml',
        'data/paperformat_landscap.xml',
        'data/paperformat_role_paper.xml',


        # action
        'views/action/open_help.xml',
        'views/action/open_report_equipment_list.xml',


        #report
        # 'report/report_equipment_list.xml',
        # 'report/print_equipment_qrcode.xml',

        # view
        'views/set_location_use.xml',
        'views/equipment.xml',


        'views/menu.xml',

    ],
    'license': 'LGPL-3',
    'installable': True,
    'images': ["static/description/banner.png"],
    'auto_install': False,
    'application': True,
    'sequence': 2
}
