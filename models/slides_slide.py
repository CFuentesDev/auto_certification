# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)
# Mensaje de control para verificar en consola que el archivo se ha cargado
print("AutoCertification: slides_slide.py loaded successfully", flush=True)

class Slide(models.Model):
    _inherit = 'slide.slide'

    is_auto_certification = fields.Boolean(compute='_compute_is_auto_certification')

    @api.depends('survey_id.scoring_type')
    def _compute_is_auto_certification(self):
        for slide in self:
            slide.is_auto_certification = slide.survey_id.scoring_type == 'auto_pass'


class SlidePartner(models.Model):
    _inherit = 'slide.slide.partner'

    def write(self, vals):
        res = super(SlidePartner, self).write(vals)
        if vals.get('completed'):
            for record in self:
                # Evitar recursión: si lo que se completó es la certificación misma, no volvemos a evaluar
                if record.slide_id.slide_type == 'certification':
                    continue
                    
                print(f"AutoCertification: SlidePartner write detected completion for slide {record.slide_id.id}", flush=True)
                # CAMBIO: Llamamos directamente a la función del canal para unificar la lógica y los logs
                channel = record.channel_id
                auto_slides = channel.slide_ids.filtered(
                    lambda s: s.slide_type == 'certification' and getattr(s, 'is_auto_pass_certification', False)
                )
                for slide in auto_slides:
                    channel._check_and_generate_auto_certification(slide, record.partner_id)
        return res

    @api.model
    def create(self, vals):
        record = super(SlidePartner, self).create(vals)
        if vals.get('completed'):
            # Evitar recursión: si lo que se completó es la certificación misma, no volvemos a evaluar
            if record.slide_id.slide_type == 'certification':
                return record

            print(f"AutoCertification: SlidePartner create detected completion for slide {record.slide_id.id}", flush=True)
            # CAMBIO: Llamamos directamente a la función del canal
            channel = record.channel_id
            auto_slides = channel.slide_ids.filtered(
                lambda s: s.slide_type == 'certification' and getattr(s, 'is_auto_pass_certification', False)
            )
            for slide in auto_slides:
                channel._check_and_generate_auto_certification(slide, record.partner_id)
        return record