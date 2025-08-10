# -*- coding: utf-8 -*-
###############################################################################
#
#    Copyright (C) 2024-TODAY,
#    Author: REAM Vitou (reamvitou@yahoo.com)
#    Tel: +855 17 82 66 82
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

import datetime
from ..lic.globals import func_mod
# from datetime import datetime, timedelta, time
# from collections import defaultdict
# import pytz

# import numpy as np


class VitouEquOpenReportEquipmentList(models.TransientModel):
    _name = 'vitouequ.open.report.equipment'
    _description = 'Open Equipment List Report'
    # _inherit = ['mail.thread']
    # _rec_name = "provider"
    # _sql_constraints = [
    #      ('name_unique', 'unique(name)', "Currency Code is duplicated!"),
    # ]

    # date = fields.Date(string="Date in Month", default=fields.Date.today())
    company_id = fields.Many2one(comodel_name='res.company', string='Company')
    department_id = fields.Many2one(comodel_name='hr.department', string='Department')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', domain="[('department_id','=', department_id)]")
    location_use_id = fields.Many2one('vitouequ.location.use', string='Location Use')

    # date_to = fields.Date(string="Date To", default=fields.Date.today())



    # @api.onchange('department_id')
    # def _get_employee(self):
    #     domain = []
    #     if self.department_id:
    #         domain.append(('department_id', '=', self.department_id.id))
    #         return domain


    def action_open_report(self):

        raise ValidationError(_('Available in paid version'))


    def get_first_two_words(text):
        return ' '.join(text.split()[:2])

    def info(self, info, type):
        return self.env[func_mod].myinfo(info, type)

    def action_reload(self):
        self.env[func_mod].reload()

    def action_close(self):
        self.env[func_mod].close_popup()





