from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
            import sys
            if 'migrate' in sys.argv: return

            try:
                from .models import User
                from .estructuras import indice_usuarios, tabla_login
                
                usuarios = User.objects.all()
                if usuarios.exists():
                    print(f"🔄 Cargando estructuras de datos...")
                    for u in usuarios:
                        # 1. Cargar BST (Por DNI) - PARA REGISTRO
                        if u.dni and u.dni.isdigit():
                            indice_usuarios.insertar(u.dni, u.email)
                        
                        # 2. Cargar Hash Table (Por Email) - PARA LOGIN
                        tabla_login.insertar(u.email, u.id)

                    print(f"⚡ [Hash Table] {usuarios.count()} emails indexados para Login O(1).")
            except Exception as e:
                print(f"Error cargando estructuras: {e}")
