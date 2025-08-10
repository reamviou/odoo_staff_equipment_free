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
from .lic.globals import func_mod


class VitouEquLocationUse(models.Model):
     _name = 'vitouequ.location.use'
     # _inherit = ['mail.thread']
     _description = 'Use Location'
     #_rec_name = "provider"
     _sql_constraints = [
          ('name_unique', 'unique(name)', "Name is duplicated!"),
     ]

     #reference = fields.Char(string="Reference", default = 'New')
     name = fields.Char(string="Location Use", required=True)
     state = fields.Selection(
          selection=[
               ('posted','Posted'),
               ('done','Done')
          ],
          default='posted',
          string="State"
     )
     description = fields.Char(string="Description")

     #done
     done_uid = fields.Many2one(comodel_name='res.users', string="Posted UID", store=True)
     done_uname = fields.Char(string="Done Uname")
     done_staff = fields.Char(string="Done Staff")
     done_date = fields.Datetime(string="Done Date", default=None)

     # undodone
     undodone_uid = fields.Many2one(comodel_name='res.users', string="Posted UID", store=True)
     undodone_uname = fields.Char(string="Undo Done Uname")
     undodone_staff = fields.Char(string="Undo Done Staff")
     undodone_date = fields.Datetime(string="Undo Done Date", default=None)


     def action_done(self):

          for rec in self:
               if rec.state == 'posted':
                    rec.state = 'done'
                    rec.done_uid = self.get_uid()
                    rec.done_uname = self.get_uname()
                    rec.done_staff = self.get_staff()
                    rec.done_date = self.get_date()
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

#
# def unlink(self):
#      for rec in self:
#           domain = [('type_id', '=', rec.id)]
#           found = self.env['ittechnician.type'].sudo().search(domain)
#           if found:
#                raise ValidationError(_("Invalide this provider. \n there are related to this one" % rec.id))
#           return super().unlink()
