from django.contrib import admin
from .models import Proyecto, Institucion_educativa, Experiencia_laboral, Referencia
from .models import Tecnologia

# Register your models here.
class Proyecto_admin(admin.ModelAdmin):
    readonly_fields=("created","updated")
    list_display=("titulo",)
    search_fields=("titulo","descripcion")

class Institucion_educativa_admin(admin.ModelAdmin):
    list_display=("nombre","titulo_obtenido")
    search_fields=("nombre",)

class Experiencia_laboral_admin(admin.ModelAdmin):
    list_display=("empresa",)
    search_fields=("empresa",)

class Referencias_admin(admin.ModelAdmin):
    list_display=("nombre",)
    search_fields=("nombre",)

class Tecnologia_admin(admin.ModelAdmin):
    list_display=("nombre",)
    search_fields=("nombre",)

admin.site.register(Proyecto, Proyecto_admin)
admin.site.register(Institucion_educativa, Institucion_educativa_admin)
admin.site.register(Experiencia_laboral, Experiencia_laboral_admin)
admin.site.register(Referencia, Referencias_admin)
admin.site.register(Tecnologia, Tecnologia_admin)