from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'

    def ready(self):
        # Cargar estructuras en memoria desde la base de datos cuando la app está lista.
        # Se hace aquí para evitar consultas prematuras a la DB antes de que Django
        # haya inicializado las conexiones.
        try:
            from . import views
            # Llamada segura: views.cargar_estructuras_desde_bd atrapa errores si
            # las tablas no existen (p.ej. durante migrate)
            views.cargar_estructuras_desde_bd()
        except Exception:
            # No fallar el arranque si algo sale mal; los errores específicos
            # de DB se manejan en la propia función.
            pass
