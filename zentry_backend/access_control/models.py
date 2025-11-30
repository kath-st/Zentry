from django.db import models
from django.conf import settings

class ScanLog(models.Model):
    OUTCOMES = (
        ('SUCCESS', 'Exitoso'),      # Verde
        ('DUPLICATE', 'Duplicado'),  # Amarillo
        ('INVALID', 'Inválido'),     # Rojo
    )

    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    scanned_code = models.CharField(max_length=50)
    outcome = models.CharField(max_length=20, choices=OUTCOMES)
    
    def __str__(self):
        return f"{self.scanned_code} - {self.outcome}"