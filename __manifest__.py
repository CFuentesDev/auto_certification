# -*- coding: utf-8 -*-
{
    "name": "Auto_Certification",
    "summary": """
        Módulo para certificados automáticos en Elearning.
    """,
    "description": """
        Módulo para generar certificados automáticos al completar cursos en la plataforma de Elearning de Odoo.
    """,
    "author": "Carlos Fuentes (CFuentes.Dev)",
    "website": "",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    "depends": ["survey", "website_slides", "website_slides_survey"],
    # always loaded
    'data': [
        'views/website_slides_templates.xml',
    ],
    "demo": [],
}
