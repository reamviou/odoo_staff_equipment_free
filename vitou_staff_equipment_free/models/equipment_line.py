# -*- coding: utf-8 -*-
###############################################################################
#
#    Copyright (C) 2024-TODAY,
#    Author: REAM Vitou (reamvitou@yahoo.com)
#    Tel: +855 17 82 66 82

###############################################################################
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from .lic.globals import func_mod


class VitouEquEquipmentLine(models.Model):
    """Model that handles the room booking form"""
    _name = "vitouequ.equipment.line"
    _description = "Hotel Folio Line"
    # _rec_name = 'room_id'



    equipment_id = fields.Many2one("vitouequ.equipment", string="Equipment Id",help="Equipment Id link to parent", ondelete="cascade")
    name = fields.Char(related='equipment_id.name', string="Equipment Name", store=True)

    equipment_no = fields.Char(related='equipment_id.equipment_no', string="Equipment No", store=True)
    model = fields.Char(related='equipment_id.model', string="Model", store=True)
    serial = fields.Char(related='equipment_id.serial', string="Serail", store=True)
    cost = fields.Float(related='equipment_id.cost', string="Cost", store=True)
    date_buy = fields.Datetime(related='equipment_id.date_buy', string="Date Buy", store=True)

    state = fields.Selection(related='equipment_id.state',
                             string="State", store=True)

    #not related
    date_use = fields.Datetime(string='Date Use', default=fields.Datetime.now())
    location_use_id = fields.Many2one(comodel_name='vitouequ.location.use', string='Location Use', store=True)
    location_use_name = fields.Char(related='location_use_id.name', store=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', store=True)
    employee_name = fields.Char(related='employee_id.name', string='Employee Name', store=True)
    position = fields.Char(related='employee_id.job_id.name', string='Position', store=True, translate=False)
    department = fields.Char(related='employee_id.department_id.name', string='Department', store=True, translate=False)
    company_id = fields.Many2one(related='equipment_id.company_id', string='Company Id', store=True)
    company = fields.Char(related='equipment_id.company', string='Company Name', store=True, translate=False)

    status = fields.Selection(
                            selection=[
                                ('posted','Posted'),
                                ('confirmed','Confirmed')
                            ],
                             string="Status", require=True, default='posted')

    # confirm
    confirmed_uid = fields.Many2one(comodel_name='res.users', string="Confirmed UID", store=True)
    confirmed_uname = fields.Char(string="Confirmed Uname")
    confirmed_staff = fields.Char(string="Confirmed Staff")
    confirmed_date = fields.Datetime(string="Confirmed Date", default=None)

    # confirm
    unconfirmed_uid = fields.Many2one(comodel_name='res.users', string="UnConfirmed UID", store=True)
    unconfirmed_uname = fields.Char(string="UnConfirmed Uname")
    unconfirmed_staff = fields.Char(string="UnConfirmed Staff")
    unconfirmed_date = fields.Datetime(string="UnConfirmed Date", default=None)


    def action_confirmed(self):

        for rec in self:
            if rec.status == 'posted':
                rec.status = 'confirmed'
                rec.confirmed_uid = self.get_uid()
                rec.confirmed_uname = self.get_uname()
                rec.confirmed_staff = self.get_staff()
                rec.confirmed_date = self.get_date()
            else:
                return self.info('Invalid State!!', 'warning')
                # raise ValidationError(_('Invalid Function!'))

    def action_unconfirmed(self):

        for rec in self:
            if rec.status == 'confirmed':
                rec.status = 'posted'
                rec.unconfirmed_uid = self.get_uid()
                rec.unconfirmed_uname = self.get_uname()
                rec.unconfirmed_staff = self.get_staff()
                rec.unconfirmed_date = self.get_date()
            else:
                return self.info('Invalid State!!', 'warning')
                # raise ValidationError(_('Invalid Function!'))

    def unlink(self):
        for rec in self:
            if rec.status =='confirmed':
                raise ValidationError(_('Cannot delete for status was confirmed'))
        return super().unlink()

    def info(self, message, type):
        return self.env[func_mod].myinfo(message, type)

    def get_uid(self):
        return self.env.user.id

    def get_uname(self):
        return self.env.user.login

    def get_date(self):
        return fields.Datetime.now()

    def get_staff(self):
        return self.env[func_mod].get_staff(self.get_uid())

    def action_reload(self):
        self.env[func_mod].reload()