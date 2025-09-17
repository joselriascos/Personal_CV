from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
from supabase import create_client
import boto3
from django.conf import settings


# Create your models here.
class Tecnologia(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        verbose_name = "Tecnologia"
        verbose_name_plural = "Tecnologias"

    def __str__(self):
        return self.nombre


class Proyecto(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=1000)
    imagen = models.ImageField(upload_to="Proyectos", null=False, blank=False)
    tecnologias = models.ManyToManyField(Tecnologia, blank=False)
    link = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "proyecto"
        verbose_name_plural = "proyectos"

    def __str__(self):
        return self.titulo


supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


@receiver(post_delete, sender=Proyecto)
def eliminar_imagen_supabase(sender, instance, **kwargs):
    if instance.imagen:
        path = instance.imagen.name
        try:
            supabase.storage.from_(settings.SUPABASE_BUCKET_NAME).remove([path])
        except Exception as e:
            # opcional: loggear error; no romper la eliminación del registro
            print("Error borrando en Supabase:", e)


class Institucion_educativa(models.Model):
    nombre = models.CharField(max_length=100)
    titulo_obtenido = models.CharField(max_length=100)
    fecha = models.CharField(max_length=30)

    class Meta:
        verbose_name = "institucion_educativa"
        verbose_name_plural = "instituciones_educativas"

    def __str__(self):
        return self.nombre


class Experiencia_laboral(models.Model):
    empresa = models.CharField(max_length=100)
    periodo_tiempo = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)

    class Meta:
        verbose_name = "experiencia_laboral"
        verbose_name_plural = "experiencias_laborales"

    def __str__(self):
        return self.empresa


class Referencia(models.Model):
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    empresa = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.PositiveBigIntegerField()

    class Meta:
        verbose_name = "referencia"
        verbose_name_plural = "referencias"

    def __str__(self):
        return self.nombre
