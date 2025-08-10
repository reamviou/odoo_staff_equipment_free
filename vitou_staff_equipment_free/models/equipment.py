
# -*- coding: utf-8 -*-
###############################################################################
#
#    Copyright (C) 2024-TODAY,
#    Author: REAM Vitou (reamvitou@yahoo.com)
#    Tel: +855 17 82 66 82
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from .lic.globals import msg_sep,func_mod



class VitouEquEquipment(models.Model):
    _name = 'vitouequ.equipment'
    _description = 'Staff Equipment List'
    # _auto = False
    _inherit = ['mail.thread']
    _order = 'name desc'
    _sql_constraints = [
        ('equipment_no_unique', 'unique(equipment_no)', "Equipment No is duplicated!"),
    ]

    name = fields.Char(string='Equipment Name', required=True, tracking=True)
    equipment_no = fields.Char(string='Equipment No')
    model = fields.Char(string='Model')
    serial = fields.Char(string='Serial')
    cost = fields.Float(string='Cost', default=0.0)
    date_buy = fields.Datetime(string='Date Buy', default= fields.Datetime.now())
    date_use = fields.Datetime(string='Date Use', default= fields.Datetime.now())
    location_use_id = fields.Many2one(comodel_name='vitouequ.location.use', string='Location Use', store=True)
    location_use_name = fields.Char(related='location_use_id.name', store=True)
    employee_id = fields.Many2one(comodel_name='hr.employee' ,string='Employee', store=True)
    employee_name = fields.Char(related='employee_id.name' ,string='Employee Name', store=True)
    position = fields.Char(related='employee_id.job_id.name', string='Position', store=True , translate=False)
    department_id = fields.Integer(related='employee_id.department_id.id', string='Department', store=True)
    department = fields.Char(related='employee_id.department_id.name', string='Department Name', store=True,  translate=False)
    company_id = fields.Many2one(comodel_name='res.company', string='Company', store=True)
    company = fields.Char(related='company_id.name', string='Company Name', store=True,  translate=False)

    state = fields.Selection(
        string='State', selection=[
            ('posted','Posted'),
            ('done','Done')
        ], default='posted', required=True)

    # status = fields.Selection(
    #     string='Status', selection=[
    #         ('stock', 'In Stock'),
    #         ('staff', 'At Staff'),
    #         ('other', 'Other')
    #     ], default='stock', required=True)
    # who_where = fields.Char(string='Who and Where', default=None)
    image = fields.Binary(string='Image')
    note = fields.Text(string='Note')

    line_ids = fields.One2many("vitouequ.equipment.line",
                                    "equipment_id", string="Child Id",
                                    help="Equipment Id History")


    # done
    done_uid = fields.Many2one(comodel_name='res.users', string="Done UID", store=True)
    done_uname = fields.Char(string="Done Uname")
    done_staff = fields.Char(string="Done Staff")
    done_date = fields.Datetime(string="Done Date", default=None)

    # undodone
    undodone_uid = fields.Many2one(comodel_name='res.users', string="Posted UID", store=True)
    undodone_uname = fields.Char(string="Undo Done Uname")
    undodone_staff = fields.Char(string="Undo Done Staff")
    undodone_date = fields.Datetime(string="Undo Done Date", default=None)

    color = fields.Integer(string='Color', default=0, compute='_change_colore_on_kanban', store=True)
    color_text = fields.Char(string='Color Text', default='text-warning', store=True)

    @api.depends("name", "state")
    def _change_colore_on_kanban(self):

        for rec in self:
            state = rec.state
            color = self.env['vitouequ.color'].get_color_by_state(state)
            for c in color:
                rec.color = c['color_code']
                rec.color_text = c['color_text']

    @api.onchange('company_id')
    def action_update_equipment_no(self):
        for rec in self:
            company = rec.company
            if rec.company:
                pre = self.env[func_mod].get_prefix(company)
                # print(self.id,'=',self._origin.id)
                if self._origin and self._origin.id:
                    rec.equipment_no = str(pre) +'-' + str(self._origin.id)
                else:
                    rec.equipment_no = None
            else:
                if self._origin and self._origin.id:
                    rec.equipment_no = str(self._origin.id)
                else:
                    rec.equipment_no = None

    def action_done(self):

        for rec in self:
            if rec.state == 'posted':
                rec.state = 'done'
                rec.done_uid = self.get_uid()
                rec.done_uname = self.get_uname()
                rec.done_staff = self.get_staff()
                rec.done_date = self.get_date()
                self.action_transfer()
            else:
                return self.info('Invalid State!!', 'warning')
                # raise ValidationError(_('Invalid Function!'))

    def action_undo_done(self):

        for rec in self:
            if rec.state == 'done':
                rec.state = 'posted'
                rec.undodone_uid = self.get_uid()
                rec.undodone_uname = self.get_uname()
                rec.undodone_staff = self.get_staff()
                rec.undodone_date = self.get_date()
            else:
                return self.info('Invalid State!!', 'warning')
                # raise ValidationError(_('Invalid Function!'))

    def action_transfer(self):
        equ_mod = self.env['vitouequ.equipment.line']
        for rec in self:
            # print('=', rec.line_ids)
            equipment_id = rec.id
            date_use = rec.date_use
            employee_id = rec.employee_id.id
            location_use_id = rec.location_use_id.id
            if equipment_id:
                equ_has = equ_mod.sudo().search([('equipment_id','=', equipment_id),('date_use','=',date_use),('employee_id','=',employee_id),('location_use_id','=',location_use_id)])

                if len(equ_has)>0:
                    return self.info('This already save for transfer', 'warning')
                else:
                    equ_has.create({
                    'equipment_id': rec.id,
                    'date_use': rec.date_use,
                    'location_use_id': rec.location_use_id.id,
                    'employee_id': rec.employee_id.id,
                    })
                    # self.action_reload()
                    # return self.info('Successful Transferred', 'success')
            else:
                return self.info('Nothing to transfer', 'warning')


    def info(self, message, type):
        return self.env[func_mod].myinfo(message,type)
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



