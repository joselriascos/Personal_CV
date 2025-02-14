from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="Home"),
    path("proyectos/", views.proyectos, name="Proyectos"),
    path("contacto/", views.contacto, name="Contacto"),
    path("proyecto/<int:id>", views.detalle_proyecto, name="Detalle_proyecto")
]