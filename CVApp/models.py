from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
import boto3
from django.conf import settings

# Create your models here.
class Tecnologia(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        verbose_name = 'Tecnologia'
        verbose_name_plural = 'Tecnologias'

    def __str__(self):
        return self.nombre

class Proyecto(models.Model):
    titulo=models.CharField(max_length=200)
    descripcion=models.CharField(max_length=1000)
    imagen=models.ImageField(upload_to="Proyectos", null=False, blank=False)
    tecnologias=models.ManyToManyField(Tecnologia, blank=False)
    link=models.CharField(max_length=200, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="proyecto"
        verbose_name_plural="proyectos"

    def __str__(self):
        return self.titulo
    
@receiver(post_delete, sender=Proyecto)
def eliminar_imagen_s3(sender, instance, **kwargs):
    if instance.imagen:
        s3 = boto3.client('s3', 
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID, 
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                        region_name=settings.AWS_S3_REGION_NAME)
        s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=str(instance.imagen))

    
class Institucion_educativa(models.Model):
    nombre=models.CharField(max_length=100)
    titulo_obtenido=models.CharField(max_length=100)
    fecha=models.CharField(max_length=30)

    class Meta:
        verbose_name="institucion_educativa"
        verbose_name_plural="instituciones_educativas"

    def __str__(self):
        return self.nombre
    
class Experiencia_laboral(models.Model):
    empresa=models.CharField(max_length=100)
    periodo_tiempo=models.CharField(max_length=100)
    cargo=models.CharField(max_length=100)

    class Meta:
        verbose_name="experiencia_laboral"
        verbose_name_plural="experiencias_laborales"
    
    def __str__(self):
        return self.empresa
    
class Referencia_laboral(models.Model):
    nombre=models.CharField(max_length=100)
    cargo=models.CharField(max_length=100, blank=True, null=True)
    empresa=models.CharField(max_length=100, blank=True, null=True)
    telefono=models.PositiveBigIntegerField()

    class Meta:
        verbose_name="referencia_laboral"
        verbose_name_plural="referencias_laborales"

    def __str__(self):
        return self.nombre
    
class Referencia_personal(models.Model):
    nombre=models.CharField(max_length=100)
    cargo=models.CharField(max_length=100, blank=True, null=True)
    empresa=models.CharField(max_length=100, blank=True, null=True)
    telefono=models.PositiveBigIntegerField()

    class Meta:
        verbose_name="referencia_personal"
        verbose_name_plural="referencias_personales"

    def __str__(self):
        return self.nombre
    
class Referencia_familiar(models.Model):
    nombre=models.CharField(max_length=100)
    cargo=models.CharField(max_length=100, blank=True, null=True)
    empresa=models.CharField(max_length=100, blank=True, null=True)
    telefono=models.PositiveBigIntegerField()

    class Meta:
        verbose_name="referencia_familiar"
        verbose_name_plural="referencias_familiares"

    def __str__(self):
        return self.nombre