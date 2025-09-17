from django.shortcuts import render, redirect, get_object_or_404
from .models import Proyecto, Institucion_educativa, Experiencia_laboral, Referencia
from django.core.mail import EmailMessage
from django.contrib import messages
from django.core.paginator import Paginator


# Create your views here.
def home(request):
    instituciones = Institucion_educativa.objects.all()
    experiencias_laborales = Experiencia_laboral.objects.all()
    referencias = Referencia.objects.all()
    return render(
        request,
        "CVApp/home.html",
        {
            "instituciones": instituciones,
            "experiencias": experiencias_laborales,
            "referencias": referencias,
        },
    )


def proyectos(request):
    proyectos = Proyecto.objects.all().order_by("-updated")
    paginator = Paginator(proyectos, 9)  # Limita a 9 proyectos por página
    numero_pagina = request.GET.get("page", 1)  # Página actual, por defecto 1
    proyectos_paginados = paginator.get_page(
        numero_pagina
    )  # Proyectos para esta página

    # Cálculo de rango de páginas a mostrar
    paginas_a_mostrar = 5
    pagina_actual = proyectos_paginados.number
    rango_paginas = list(paginator.page_range)

    minimo = max(0, pagina_actual - 3)
    maximo = min(paginator.num_pages, minimo + paginas_a_mostrar)
    rango_paginas = rango_paginas[minimo:maximo]

    return render(
        request,
        "CVApp/proyectos.html",
        {"proyectos": proyectos_paginados, "rango_paginas": rango_paginas},
    )


def detalle_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    return render(request, "CVApp/detalle_proyecto.html", {"proyecto": proyecto})


def contacto(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        correo = request.POST.get("correo")
        mensaje = request.POST.get("mensaje")

        mail = EmailMessage(
            "Mensaje desde portafolio",
            "El usuario {} con la dirección de correo {} escribe lo siguiente:\n\n {}".format(
                nombre, correo, mensaje
            ),
            "",
            ["joseluis.riascos10@gmail.com"],
            reply_to=[correo],
        )

        try:
            mail.send()
        except:
            messages.error(request, "Algo salió mal, inténtalo nuevamente")
        else:
            messages.success(request, "Mensaje enviado correctamente")
        finally:
            return redirect("Contacto")

    return render(request, "CVApp/contacto.html")
