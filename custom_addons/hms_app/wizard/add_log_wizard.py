from odoo import models, fields, api

class PatientHistoryWizard(models.TransientModel):
    _name = 'hms.wizard'
    _description = 'Patient History Wizard'

    description = fields.Text(string='Description', required=True)
    patient_id = fields.Many2one('hms.patient')
    date = fields.Date(default=fields.Date.today())

    def action_add_history(self):
        self.ensure_one()

        self.env['hms.history'].create({
            'description': self.description,
            'patient_id': self.patient_id.id,
        })
