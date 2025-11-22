from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from datetime import date
from decimal import Decimal
from .models import Usuario
from .forms import RegistroCompradorForm, LoginForm, UsuarioUpdateForm
from .estructura import Pila, TablaHash
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.db import OperationalError, ProgrammingError

# Tabla hash para verificar DNIs y correos únicos
# Uso: verificador_datos.insertar(clave, valor) y verificador_datos.buscar(clave)
# - Actualmente se usa en `registro_comprador` para evitar duplicados de dni/email.
verificador_datos = TablaHash()

# Diccionario para almacenar el historial de compras de cada usuario
# Estructura: { user.id: Pila() }
# Uso en este proyecto:
# - Al registrar una compra: historiales_compra[user.id].apilar(compra_dict)
# - Al mostrar perfil: historiales_compra[user.id].obtener_historial()  (tope primero)
historiales_compra = {}

def cargar_estructuras_desde_bd():
    """Carga verificador_datos y historiales_compra desde la base de datos.
    - Inserta dni/email de cada Usuario en `verificador_datos` (TablaHash).
    - Crea una `Pila` por usuario y apila todas las compras desde `Compra`.
    """
    global verificador_datos, historiales_compra
    try:
        from .models import Usuario, Compra

        # Reiniciar estructuras
        verificador_datos = TablaHash()
        historiales_compra = {}

        # Registrar usuarios en la tabla hash y crear pilas vacías
        for u in Usuario.objects.all():
            if u.dni:
                verificador_datos.insertar(u.dni, u.id)
            if u.email:
                verificador_datos.insertar(u.email, u.id)
            historiales_compra[u.id] = Pila()

        # Poblar pilas con compras (orden ascendente para que el tope sea la última compra)
        for c in Compra.objects.select_related('usuario').order_by('creado'):
            uid = c.usuario_id
            if uid not in historiales_compra:
                historiales_compra[uid] = Pila()
            compra_dict = {
                'fecha': c.fecha.isoformat() if c.fecha else c.creado.date().isoformat(),
                'producto': c.producto,
                'monto': float(c.monto),
            }
            historiales_compra[uid].apilar(compra_dict)

    except (OperationalError, ProgrammingError):
        # Tablas no creadas aún o DB inaccesible; no cargar estructuras
        return

def es_organizador(user):
    return user.es_organizador()

def es_validador(user):
    return user.es_validador()

def registro_comprador(request):
    if request.method == 'POST':
        form = RegistroCompradorForm(request.POST)
        if form.is_valid():
            # Verificar DNI y correo únicos usando TablaHash (verificador_datos)

            # Verificación actual en memoria:
            dni = form.cleaned_data['dni']
            email = form.cleaned_data['email']
            
            if verificador_datos.buscar(dni) or verificador_datos.buscar(email):
                messages.error(request, 'El DNI o correo ya están registrados')
                return render(request, 'usuarios/registro.html', {'form': form})
            
            # Crear nuevo usuario
            usuario = form.save(commit=False)
            usuario.tipo = 'COMPRADOR'
            usuario.password = make_password(form.cleaned_data['password1'])
            usuario.save()
            
            # Registrar DNI y correo en la tabla hash (en memoria)
            verificador_datos.insertar(dni, usuario.id)
            verificador_datos.insertar(email, usuario.id)

            # Inicializar historial de compras en memoria usando Pila
            # - Cada usuario tiene su propia Pila donde se apilan compras.
            # - Alternativa persistente: crear un modelo `Compra` con FK a Usuario.
            historiales_compra[usuario.id] = Pila()
            
            login(request, usuario)
            return redirect('perfil')
    else:
        form = RegistroCompradorForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = Usuario.objects.get(email=email)
                user = authenticate(username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    if user.es_organizador():
                        return redirect('admin_usuarios')
                    elif user.es_validador():
                        return redirect('validador_dashboard')
                    else:
                        return redirect('perfil')
                else:
                    messages.error(request, 'Contraseña incorrecta')
            except Usuario.DoesNotExist:
                messages.error(request, 'No existe un usuario con ese correo')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.es_comprador())
def agregar_compra(request):
    """Registrar una nueva compra y apilarla en la Pila del usuario."""
    if request.method == 'POST':
        producto = request.POST.get('producto')
        monto = request.POST.get('monto')
        fecha = request.POST.get('fecha') or date.today().isoformat()

        compra = {
            'fecha': fecha,
            'producto': producto,
            'monto': monto,
        }

        # Obtener o inicializar la Pila del usuario
        pila = historiales_compra.get(request.user.id)
        if not pila:
            # Si no existe la Pila en el diccionario, crear una nueva Pila
            # y asignarla al usuario. Esto mantiene el historial en memoria
            # para la sesión del proceso actual.
            pila = Pila()
            historiales_compra[request.user.id] = pila

        # Apilar la compra (LIFO): la última compra quedará en el tope
        pila.apilar(compra)

        # Persistir la compra en la base de datos para mantener histórico
        try:
            from .models import Compra
            Compra.objects.create(
                usuario=request.user,
                producto=producto,
                monto=Decimal(monto),
                fecha=fecha if fecha else None,
            )
        except Exception:
            # No bloquear la UX si la persistencia falla; ya existe la entrada en memoria
            pass

        messages.success(request, 'Compra registrada correctamente')
        return redirect('perfil')

    return render(request, 'usuarios/comprar.html')

def cerrar_sesion(request):
    logout(request)
    return redirect('login')

@login_required
def perfil(request):
    # Obtener historial de compras si existe
    historial = None
    if request.user.id in historiales_compra:
        historial = historiales_compra[request.user.id].obtener_historial()
    return render(request, 'usuarios/perfil.html', {
        'usuario': request.user,
        'historial': historial
    })

@login_required
@user_passes_test(es_organizador)
def admin_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/admin_usuarios.html', {'usuarios': usuarios})

@login_required
@user_passes_test(es_organizador)
def modificar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    # Guardar valores previos para mantener TablaHash consistente si cambian
    old_dni = usuario.dni
    old_email = usuario.email

    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, instance=usuario)
        if form.is_valid():
            actualizado = form.save()

            # Actualizar TablaHash en memoria si DNI o email cambiaron
            try:
                new_dni = actualizado.dni
                new_email = actualizado.email
                if old_dni and old_dni != new_dni:
                    verificador_datos.eliminar(old_dni)
                if old_email and old_email != new_email:
                    verificador_datos.eliminar(old_email)
                if new_dni:
                    verificador_datos.insertar(new_dni, actualizado.id)
                if new_email:
                    verificador_datos.insertar(new_email, actualizado.id)
            except Exception:
                # No bloquear si la estructura en memoria no se puede actualizar
                pass

            messages.success(request, 'Usuario actualizado correctamente')
            return redirect('admin_usuarios')
        else:
            messages.error(request, 'Revisa los errores del formulario')
    else:
        form = UsuarioUpdateForm(instance=usuario)

    return render(request, 'usuarios/modificar_usuario.html', {
        'form': form,
        'usuario': usuario,
    })

@login_required
@user_passes_test(es_validador)
def validador_dashboard(request):
    return render(request, 'usuarios/validador_dashboard.html')

@login_required
def catalogo_eventos(request):
    from events.models import Event
    eventos = Event.objects.all().order_by('date')
    return render(request, 'usuarios/catalogo_eventos.html', {'eventos': eventos})