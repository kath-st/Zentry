from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from .estructuras import indice_usuarios
from . import services
from rest_framework.permissions import IsAuthenticated, AllowAny


class RegisterView(APIView):
    permission_classes = [AllowAny]  # Permitir acceso sin autenticar

    def post(self, request):
        dni = request.data.get('dni')

        # Validación con el arbol de busqueda binaria (BST)
        if dni and indice_usuarios.existe(dni):
            return Response(
                {"error": f"El DNI {dni} ya existe."},
                status=status.HTTP_400_BAD_REQUEST
            )

        success, result = services.register_user(request.data)
        if success:
            return Response({"mensaje": "Usuario creado.", "usuario": result}, status=status.HTTP_201_CREATED)

        return Response(result, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        success, result = services.login_user(email, password)# Aca se valida con la tabla hash
        if success:
            payload = result
            payload["message"] = "Login exitoso"
            return Response(payload, status=status.HTTP_200_OK)

        # Diferenciar tipo de error para código HTTP
        error_msg = result.get("error", "") if isinstance(result, dict) else ""
        if "no existe" in error_msg:
            return Response(result, status=status.HTTP_404_NOT_FOUND)

        return Response(result, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios logueados (Token)

    def get(self, request):
        """Ver perfil"""
        return Response(services.get_profile(request.user))

    def patch(self, request):
        """Editar perfil"""
        success, result = services.update_profile(request.user, request.data)
        if success:
            return Response(result)

        # Si hay error de email en uso devolvemos 400
        err = result.get("error") if isinstance(result, dict) else None
        if err and "en uso" in err:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_400_BAD_REQUEST)
