from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableAdminBase
from .models import (
    Proyecto,
    Institucion_educativa,
    Experiencia_laboral,
    Referencia,
    Tecnologia,
)


# Register your models here.
@admin.register(Proyecto)
class Proyecto_admin(admin.ModelAdmin):
    readonly_fields = ("created", "updated")
    list_display = ("titulo",)
    search_fields = ("titulo", "descripcion")


@admin.register(Institucion_educativa)
class Institucion_educativa_admin(admin.ModelAdmin):
    list_display = ("nombre", "titulo_obtenido")
    search_fields = ("nombre",)


@admin.register(Experiencia_laboral)
class Experiencia_laboral_admin(admin.ModelAdmin):
    list_display = ("empresa",)
    search_fields = ("empresa",)


@admin.register(Referencia)
class Referencia_admin(SortableAdminBase, admin.ModelAdmin):
    list_display = ("nombre", "orden")
    list_editable = ("orden",)
    ordering = ("orden",)


@admin.register(Tecnologia)
class Tecnologia_admin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)
