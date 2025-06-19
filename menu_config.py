menu_config = {
    "menu_ambar": {
        "type": "link",
        "label": "Ambar",
        "link": "https://culiacan.ambar.tecnm.mx/estudiantes/"
    },
    "menu_asp": {
        "type": "submenu",
        "submenu": [
            {"id": "asp_preinsc", "label": "Sistema de Pre-Inscripciones", "type": "link", "link": "https://www.culiacan.tecnm.mx/preinscripciones-agosto-diciembre-2025/"},
            {"id": "asp_recibos", "label": "Recibos", "type": "link", "link": "https://culiacan.ambar.tecnm.mx/recibos/"},
            {"id": "asp_evaluatec", "label": "EVALUATEC", "type": "submenu", "submenu": [
                {"id": "eval_link1", "label": "Link 1", "type": "link", "link": "https://culiacan.evaluatec.tecnm.mx"}
            ]}
        ]
    },
    "menu_ofe": {
        "type": "submenu",
        "submenu": [
            {
                "id": "ofe_lic",
                "label": "Licenciaturas",
                "type": "submenu",
                "submenu": [
                    {
                        "id": "lic_ambiental",
                        "label": "Ingeniería Ambiental",
                        "type": "submenu",
                        "submenu": [
                            {"id": "ambiental_reticula", "label": "Retícula", "type": "link", "link": "https://..."},
                            {"id": "ambiental_plan", "label": "Plan de estudios", "type": "link", "link": "https://..."},
                            {"id": "ambiental_programas", "label": "Programas de estudios por materia", "type": "link", "link": "https://..."}
                        ]
                    },
                    # ... repite esta estructura para cada carrera
                ]
            },
            {
                "id": "ofe_pos",
                "label": "Posgrados",
                "type": "submenu",
                "submenu": [
                    {
                        "id": "pos_computacion",
                        "label": "Maestría en Ciencias de la Computación",
                        "type": "submenu",
                        "submenu": [
                            {"id": "computacion_plan", "label": "Plan de estudios", "type": "link", "link": "https://..."},
                            {"id": "computacion_requisitos", "label": "Requisitos de ingreso", "type": "link", "link": "https://..."},
                            {"id": "computacion_tutoria", "label": "Tutoría", "type": "link", "link": "https://..."}
                        ]
                    },
                    # ... repite para los otros posgrados
                ]
            },
            {
                "id": "ofe_cle",
                "label": "Coordinación de Lenguas Extranjeras",
                "type": "submenu",
                "submenu": [
                    {"id": "cle_informes", "label": "Informes CLE", "type": "info", "text": "Información sobre CLE..."},
                    {"id": "cle_programa", "label": "Programa e Inscripciones", "type": "info", "text": "Información sobre programa e inscripciones..."},
                    {"id": "cle_facebook", "label": "Página de Facebook", "type": "link", "link": "https://..."}
                ]
            }
        ]
    },
    "menu_est": {
        "type": "submenu",
        "submenu": [
            {
                "id": "est_serv",
                "label": "Servicios Escolares",
                "type": "submenu",
                "submenu": [
                    {"id": "horarios", "label": "Horarios de Atención", "type": "info", "text": "Lunes a Viernes de 8:00 a 14:00 hrs."},
                    {"id": "reglamento", "label": "Reglamento de Estudiantes", "type": "link", "link": "https://..."},
                    {"id": "medicos", "label": "Servicios Médicos", "type": "link", "link": "https://..."},
                    {"id": "thona", "label": "Seguro THONA", "type": "link", "link": "https://..."},
                    {"id": "imss", "label": "Seguro IMSS", "type": "link", "link": "https://..."}
                ]
            },
            {
                "id": "est_fin",
                "label": "Recursos Financieros",
                "type": "submenu",
                "submenu": [
                    {"id": "cuotas", "label": "Cuotas de servicios", "type": "link", "link": "https://..."},
                    {"id": "horarios_fin", "label": "Horarios de atención", "type": "link", "link": "https://..."},
                    {"id": "encuesta", "label": "Encuesta de satisfacción", "type": "link", "link": "https://..."}
                ]
            },
            {
                "id": "est_gest",
                "label": "Gestión Tecnológica y Vinculación",
                "type": "submenu",
                "submenu": [
                    {"id": "residencias", "label": "Residencias Profesionales", "type": "link", "link": "https://..."},
                    {"id": "requisitos", "label": "Requisitos carta presentación", "type": "link", "link": "https://..."},
                    {"id": "formatos", "label": "Descarga de formatos", "type": "link", "link": "https://..."},
                    {"id": "banco_proyectos", "label": "Banco de proyectos", "type": "link", "link": "https://..."}
                ]
            }
        ]
    },
    "menu_map": {
        "type": "image",
        "label": "Mapa de instalaciones",
        "image": "/static/images/mapa.png"
    }
}
