from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import RegistroSerializer, UserProfileSerializer
from .estructuras import indice_usuarios, tabla_login


def register_user(data):
    """Registra un usuario usando el serializer y sincroniza las estructuras.

    Retorna (True, serializer.data) en caso de éxito o (False, errors) en caso de error.
    """
    serializer = RegistroSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()

        # Actualizamos las estructuras en memoria
        try:
            indice_usuarios.insertar(user.dni, user.email)
        except Exception:
            pass

        try:
            tabla_login.insertar(user.email, user.id)
        except Exception:
            pass

        return True, serializer.data

    return False, serializer.errors


def login_user(email, password):
    """Valida existencia en tabla hash y autentica credenciales.

    Retorna (True, payload) con token y usuario, o (False, error).
    """
    if not tabla_login.existe(email):
        return False, {"error": "El email no existe."}

    user = authenticate(username=email, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        payload = {
            "token": token.key,
            "user_id": user.id,
            "role": getattr(user, "role", None),
        }
        return True, payload

    return False, {"error": "Contraseña incorrecta."}


def get_profile(user):
    """Devuelve los datos del perfil del usuario."""
    serializer = UserProfileSerializer(user)
    return serializer.data


def update_profile(user, data):
    """Actualiza parcialmente el perfil y sincroniza estructuras si cambia el email.

    Retorna (True, payload) o (False, errors).
    """
    old_email = user.email
    serializer = UserProfileSerializer(user, data=data, partial=True)

    if serializer.is_valid():
        new_email = data.get("email")

        if new_email and new_email != old_email:
            if tabla_login.existe(new_email):
                return False, {"error": "El email ya está en uso."}

            try:
                tabla_login.eliminar(old_email)
            except Exception:
                pass

            try:
                tabla_login.insertar(new_email, user.id)
            except Exception:
                pass

        serializer.save()

        return True, {"message": "Perfil actualizado y estructuras sincronizadas.", "data": serializer.data}

    return False, serializer.errors
