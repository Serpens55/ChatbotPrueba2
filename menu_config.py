menu_config = {
    "menu_ambar": {
        "type": "link",
        "label": "Ambar",
        "link": "https://www.culiacan.ambar.tecnm.mx/estudiantes/"
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
            {"id": "ofe_lic", "label": "Licenciaturas", "type": "submenu", "submenu": [
                {"id": "lic_reticula", "label": "Retícula", "type": "link", "link": "https://link-reticula.com"},
                {"id": "lic_plan", "label": "Plan de estudios", "type": "link", "link": "https://link-plan.com"},
                {"id": "lic_programas", "label": "Programas de estudios por materia", "type": "link", "link": "https://link-programas.com"}
            ]},
            {"id": "ofe_pos", "label": "Posgrados", "type": "submenu", "submenu": [
                {"id": "pos_plan", "label": "Plan de estudios", "type": "link", "link": "https://link-posplan.com"},
                {"id": "pos_requisitos", "label": "Requisitos de ingreso", "type": "link", "link": "https://link-posrequisitos.com"},
                {"id": "pos_tutoria", "label": "Tutoría", "type": "link", "link": "https://link-postutoria.com"}
            ]},
            {"id": "ofe_cle", "label": "Coordinación de Lenguas Extranjeras", "type": "submenu", "submenu": [
                {"id": "cle_informes", "label": "Informes CLE", "type": "info", "text": "Información sobre CLE..."},
                {"id": "cle_programa", "label": "Programa e Inscripciones", "type": "info", "text": "Información sobre programa e inscripciones..."},
                {"id": "cle_facebook", "label": "Página de Facebook", "type": "link", "link": "https://link-facebook.com"}
            ]}
        ]
    },
    "menu_est": {
        "type": "submenu",
        "submenu": [
            {"id": "est_serv", "label": "Servicios Escolares", "type": "submenu", "submenu": [
                {"id": "horarios", "label": "Horarios de Atención", "type": "info", "text": "Lunes a Viernes de 8:00 a 14:00 hrs."},
                {"id": "reglamento", "label": "Reglamento de Estudiantes", "type": "link", "link": "https://link-reglamento.com"},
                {"id": "medicos", "label": "Servicios Médicos de la Institución", "type": "link", "link": "https://link-medicos.com"},
                {"id": "thona", "label": "Seguro Escolar y Vida THONA", "type": "link", "link": "https://link-thona.com"},
                {"id": "imss", "label": "Seguro Facultativo-IMSS", "type": "link", "link": "https://link-imss.com"}
            ]},
            {"id": "est_fin", "label": "Recursos Financieros", "type": "submenu", "submenu": [
                {"id": "cuotas", "label": "Cuotas de servicios enero-junio de 2025", "type": "link", "link": "https://link-cuotas.com"},
                {"id": "horarios_fin", "label": "Horarios de atención en ventanilla bancaria y en correo electrónico", "type": "link", "link": "https://link-horariosfin.com"},
                {"id": "encuesta", "label": "Encuesta de Satisfacción de Servicios de Recursos Financieros", "type": "link", "link": "https://link-encuesta.com"}
            ]},
            {"id": "est_gest", "label": "Gestión Tecnológica y Vinculación", "type": "submenu", "submenu": [
                {"id": "residencias", "label": "Residencias Profesionales", "type": "link", "link": "https://link-residencias.com"},
                {"id": "requisitos", "label": "Requisitos para solicitar carta de presentación de residencias profesionales", "type": "link", "link": "https://link-requisitos.com"},
                {"id": "formatos", "label": "Descarga de formatos", "type": "link", "link": "https://link-formatos.com"},
                {"id": "banco_proyectos", "label": "Banco de proyectos", "type": "link", "link": "https://link-bancoproyectos.com"}
            ]}
        ]
    },
    "menu_map": {
        "type": "image",
        "label": "Mapa de instalaciones",
        "image": "/static/img/mapa.png"
    }
}