from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # Funcion para cargar las estrucuras en memoria al iniciar la app
    def ready(self):
            import sys
            if 'migrate' in sys.argv: return

            try:
                from .models import User
                from .estructuras import indice_usuarios, tabla_login
                
                usuarios = User.objects.all()
                if usuarios.exists():
                    for u in usuarios:
                        # 1. Cargar BST (Por DNI) - PARA REGISTRO
                        if u.dni and u.dni.isdigit():
                            indice_usuarios.insertar(u.dni, u.email)
                        
                        # 2. Cargar Hash Table (Por Email) - PARA LOGIN
                        tabla_login.insertar(u.email, u.id)

            except Exception as e:
                print(f"Error cargando estructuras: {e}")
