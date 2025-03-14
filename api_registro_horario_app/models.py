
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.timezone import now



class RegistroHorario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    entrada = models.TimeField(null=True, blank=True)
    salida = models.TimeField(null=True, blank=True)
    pausa_inicio = models.TimeField(null=True, blank=True)
    pausa_fin = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('usuario', 'fecha')
    
    def marcar_entrada(self):
        self.entrada = now().time()
        self.save()

    def marcar_salida(self):
        self.salida = now().time()
        self.save()

    # def clean(self):
    #     if self.entrada and self.salida and self.entrada > self.salida:
    #         raise ValidationError("La hora de salida no puede ser antes de la hora de entrada.")
    #     if self.pausa_inicio and self.pausa_fin and self.pausa_inicio > self.pausa_fin:
    #         raise ValidationError("La pausa de inicio no puede ser después de la pausa de fin.")
    
    def clean(self):
        if self.entrada and self.salida:
            if self.entrada > self.salida:
                raise ValidationError("La hora de salida no puede ser antes de la entrada.")
        
        if self.pausa_inicio and self.pausa_fin:
            if self.pausa_inicio > self.pausa_fin:
                raise ValidationError("La pausa de inicio no puede ser después de la pausa de fin.")
            if self.pausa_inicio < self.entrada:
                raise ValidationError("La pausa no puede comenzar antes de la hora de entrada.")
            if self.pausa_fin > self.salida:
                raise ValidationError("La pausa no puede terminar después de la salida.")
    

    def __str__(self):
        return f"{self.usuario.username} - {self.fecha}"