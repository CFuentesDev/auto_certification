import logging
from odoo import models, api

_logger = logging.getLogger(__name__)

class SlideChannel(models.Model):
    _inherit = 'slide.channel'

    def _check_and_generate_auto_certification(self, slide, partner):
        print(f"AutoCertification: Checking requirements for partner {partner.name} (ID: {partner.id}) on slide {slide.id}", flush=True)
    def _check_and_generate_auto_certification(self, slide, partner):
        """Lógica interna de validación y marcado de certificación automática"""
        print(f"AutoCertification: Checking requirements for partner {partner.name} (ID: {partner.id}) on slide {slide.id}", flush=True)
        
        # 1. Obtener slides requeridas (publicadas, no secciones, no la certificación misma)
        # Usamos sudo() para asegurar acceso a slides que podrían estar restringidas
        required_slides = self.sudo().slide_ids.filtered(
            lambda s: s.is_published and not s.is_category and s.id != slide.id
        )
        
        if not required_slides:
            print("AutoCertification: No required slides found for this channel.", flush=True)
            return

        # 2. Verificar completitud
        completed_count = self.env['slide.slide.partner'].sudo().search_count([
            ('partner_id', '=', partner.id),
            ('slide_id', 'in', required_slides.ids),
            ('completed', '=', True)
        ])
        
        print(f"AutoCertification: Required: {len(required_slides)} | Completed: {completed_count}", flush=True)

        # 3. Si terminó todo lo demás, forzamos el éxito
        if completed_count >= len(required_slides):
            print(f"AutoCertification: Requirements met. Generating certification for {partner.name}", flush=True)
            
            # Crear respuesta de encuesta si no existe una exitosa
            existing = self.env['survey.user_input'].sudo().search([
                ('survey_id', '=', slide.survey_id.id),
                ('partner_id', '=', partner.id),
                ('scoring_success', '=', True)
            ], limit=1)

            if not existing:
                import uuid
                user_input = self.env['survey.user_input'].sudo().create({
                    'survey_id': slide.survey_id.id,
                    'partner_id': partner.id,
                    'email': partner.email,
                    'nickname': partner.name,
                    'state': 'done',
                    'access_token': str(uuid.uuid4()),
                    'deadline': self.env.cr.now(),
                })
                # Forzamos los valores para evitar sobreescritura por computes de Odoo
                user_input.sudo().write({
                    'scoring_success': True,
                    'scoring_percentage': 100.0,
                })
                print(f"AutoCertification: Created user_input {user_input.id} with token", flush=True)
            else:
                user_input = existing
                print(f"AutoCertification: Using existing successful user_input {user_input.id}", flush=True)

            # 4. Actualizar relación slide-partner para marcar completado y habilitar descarga
            lp = self.env['slide.slide.partner'].sudo().search([
                ('slide_id', '=', slide.id),
                ('partner_id', '=', partner.id)
            ], limit=1)
            
            vals = {
                'completed': True,
                'survey_scoring_success': True
            }

            if lp:
                lp.sudo().write(vals)
                print(f"AutoCertification: Updated slide_partner {lp.id}", flush=True)
            else:
                vals.update({
                    'slide_id': slide.id,
                    'partner_id': partner.id,
                    'channel_id': self.id,
                })
                lp = self.env['slide.slide.partner'].sudo().create(vals)
                print(f"AutoCertification: Created slide_partner {lp.id}", flush=True)

            # Vincular el user_input al slide_partner (Importante para que el botón de descarga funcione)
            if user_input.slide_partner_id != lp:
                user_input.sudo().write({'slide_partner_id': lp.id})