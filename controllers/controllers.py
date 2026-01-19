from odoo import http
from odoo.http import request
from odoo.addons.website_slides.controllers.main import WebsiteSlides

class WebsiteSlidesCustom(WebsiteSlides):

    @http.route()
    def channel(self, channel, category=None, tag=None, search=None, **kw):
        """
        Esta ruta es la que carga la página principal del curso.
        Al intervenir aquí, garantizamos que cuando el HTML llegue al navegador,
        los círculos ya tengan la información de 'completado'.
        """
        print(f"AutoCertification: DEBUG - Controller channel visited for {channel.name} (ID: {channel.id})", flush=True)
        
        if request.env.user and channel.is_member:
            partner = request.env.user.partner_id
            print(f"AutoCertification: User {partner.name} (ID: {partner.id}) is member", flush=True)
            
            # 1. Buscamos el contenido de certificación automática
            auto_slide = channel.slide_ids.filtered(
                lambda s: s.slide_type == 'certification' and getattr(s, 'is_auto_pass_certification', False)
            )
            print(f"AutoCertification: Auto slides found: {auto_slide.ids}", flush=True)

            if auto_slide:
                # Delegamos la verificación al modelo para centralizar la lógica y ver los logs
                channel._check_and_generate_auto_certification(auto_slide[:1], partner)
        else:
            print("AutoCertification: User not logged in or not a member of this channel", flush=True)

        # 4. Retornamos la respuesta original: ahora llevará los datos actualizados
        return super(WebsiteSlidesCustom, self).channel(channel, category=category, tag=tag, search=search, **kw)