from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # ROLES
    CLIENTE = 'CLIENTE'
    EMPLEADO = 'EMPLEADO'
    ADMIN = 'ADMIN'
    ROLE_CHOICES = [
        (CLIENTE, 'Cliente'),
        (EMPLEADO, 'Empleado'),
        (ADMIN, 'Administrador'),
    ]

    # CAMPOS PERSONALIZADOS
    dni = models.CharField(max_length=20, unique=True, verbose_name="DNI")
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=CLIENTE)
    card_number = models.CharField(max_length=16, blank=True, null=True, help_text="Simulación")
    
    # Hacemos que el email sea el identificador principal en lugar del username
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'dni']

    def __str__(self):
        return f"{self.first_name} - {self.dni}"