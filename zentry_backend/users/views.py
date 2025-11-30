from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistroSerializer, LoginSerializer, UserProfileSerializer
from .estructuras import indice_usuarios, tabla_login
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny

class RegisterView(APIView):
    permission_classes = [AllowAny]  # Permitir acceso sin autenticar
    def post(self, request):
        dni = request.data.get('dni')

        # 1. VALIDACIÓN CON ESTRUCTURA DE DATOS (BST)
        # Esto es O(log n), mucho más rápido que ir a la BD
        if dni and indice_usuarios.existe(dni):
            return Response(
                {"error": f"El DNI {dni} ya existe (Validado por Árbol Binario)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. PROCESO NORMAL DE DJANGO
        serializer = RegistroSerializer(data=request.data)
        if serializer.is_valid():
            # Guardar en SQL
            nuevo_usuario = serializer.save()

            # 3. ACTUALIZAR ESTRUCTURA DE DATOS
            indice_usuarios.insertar(nuevo_usuario.dni, nuevo_usuario.email)

            # Insertar en Hash Table (Email) para Login O(1)
            tabla_login.insertar(nuevo_usuario.email, nuevo_usuario.id)

            return Response({
                "mensaje": "Usuario creado e indexado en BST.",
                "usuario": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # 1. VALIDACIÓN CON ESTRUCTURA DE DATOS (Hash Table)
        # Búsqueda O(1) - "Fail Fast"
        if not tabla_login.existe(email):
            return Response(
                {"error": "El email no existe (Verificado en Hash Table O(1))."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 2. AUTENTICACIÓN DE CREDENCIALES
        # Usamos Django para comparar el password hasheado (Seguridad)
        user = authenticate(username=email, password=password)

        if user:
            # Generar o recuperar token
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user_id": user.id,
                "role": user.role,
                "message": "Login exitoso vía Hash Table + Auth"
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Contraseña incorrecta."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
class ProfileView(APIView):
    permission_classes = [IsAuthenticated] # Solo usuarios logueados (Token)

    def get(self, request):
        """ VER PERFIL """
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        """ EDITAR PERFIL """
        user = request.user
        old_email = user.email # Guardamos el email viejo por si cambia
        
        serializer = UserProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            # 1. VERIFICACIÓN DE ESTRUCTURA (Si cambia el email)
            new_email = request.data.get('email')
            
            if new_email and new_email != old_email:
                # Verificar que el nuevo email no esté ocupado en la Hash Table
                if tabla_login.existe(new_email):
                    return Response(
                        {"error": "Ese email ya está en uso (Validado por Hash Table)."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # ACTUALIZACIÓN DE ESTRUCTURA DE DATOS (Sincronización)
                # O(1) - Borrar entrada vieja
                tabla_login.eliminar(old_email)
                # O(1) - Insertar entrada nueva
                tabla_login.insertar(new_email, user.id)

            # 2. Guardar en Base de Datos
            serializer.save()
            
            return Response({
                "message": "Perfil actualizado y estructuras sincronizadas.",
                "data": serializer.data
            })
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
