from odoo import models, fields, api

class Doctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Doctor'
    _rec_name = 'full_name'

    first_name = fields.Char()
    last_name = fields.Char()
    full_name = fields.Char(compute='_compute_full_name', store=True)
    image = fields.Image()
    patient_ids = fields.One2many('hms.patient', 'doctor_id')
    department_id = fields.Many2one('hms.department')

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for record in self:
            record.full_name = f"{record.first_name} {record.last_name}"
