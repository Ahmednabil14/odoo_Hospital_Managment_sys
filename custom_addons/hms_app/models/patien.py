from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
from dateutil.relativedelta import relativedelta



class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'
    _rec_name = 'first_name'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-')
    ])
    pcr = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ])
    image = fields.Image()
    address = fields.Text()
    age = fields.Integer(compute='_compute_age', store=True)
    email = fields.Char()
    department_id = fields.Many2one('hms.department', domain="[('is_opened', '=', 'True')]")
    doctor_id = fields.Many2one('hms.doctor')

    history_ids = fields.One2many('hms.history',
                                  'patient_id')
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], default='undetermined')

    def undetermined_action(self):
        self.state = 'undetermined'

    def good_action(self):
        self.state = 'good'

    def fair_action(self):
        self.state = 'fair'

    def serious_action(self):
        self.state = 'serious'

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                record.age = relativedelta(fields.Date.today(), record.birth_date).year


    @api.model
    def write(self, vals):
        if 'state' in vals:
            self.env['hms.history'].create({
                'description': f"State changed to {vals['state']}",
                'patient_id': self.id
            }
            )
        res = super(Patient, self).write(vals)
        return res

    @api.model
    def create(self, vals):
        if vals.get('pcr') == 'yes' and not vals.get('cr_ratio'):
            raise ValidationError('CR Ratio is required when PCR is checked.')
        res = super(Patient, self).create(vals)
        return res


    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id:
            return {'domain': {'doctor_id': [('department_id', '=', self.department_id.id)]}}

    # @api.onchange('department_id')
    # def _onchange_department_id(self):
    #     if self.department_id:
    #         # return {'search_params': {'domain': [], 'fields': ['name']}}
    #         return {'search_params': {'domain': [('department_id', '=', self.department_id.id)],
    #                                   'fields': ['doctor_ids']}}

    def action_add_log_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('hms_app.add_log_action')
        action['context'] = {
            'default_patient_id': self.id
        }
        return action

    @api.onchange('email')
    def _onchange_valid_email(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            email = self.env['hms.patient'].search([('email', '=', self.email)])
            if not match:
                raise ValidationError('Not a valid E-mail ID')
            if email:
                raise  ValidationError('This email used before')

class History(models.Model):
    _name = 'hms.history'
    _description = 'History'

    date = fields.Date(default=fields.Date.today())
    description = fields.Text()
    patient_id = fields.Many2one('hms.patient')


