# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Survey(models.Model):
    _inherit = 'survey.survey'

    scoring_type = fields.Selection(selection_add=[
        ('auto_pass', 'Aprobación Automática')
    ], ondelete={'auto_pass': 'set default'})

class Slide(models.Model):
    _inherit = 'slide.slide'

    is_auto_pass_certification = fields.Boolean(
        string="Certificación Automática",
        compute="_compute_is_auto_pass_certification",
        store=True,  # Esto guardará el valor en la DB
        readonly=True
    )

    @api.depends('survey_id', 'survey_id.scoring_type')
    def _compute_is_auto_pass_certification(self):
        for slide in self:
            # Sudo es esencial para saltar restricciones de acceso en el cómputo
            is_auto = False
            if slide.slide_type == 'certification' and slide.survey_id:
                if slide.survey_id.sudo().scoring_type == 'auto_pass':
                    is_auto = True
            slide.is_auto_pass_certification = is_auto