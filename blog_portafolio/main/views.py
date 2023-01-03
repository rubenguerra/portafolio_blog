from django.views import generic
from blog.models import Habilidad
from .models import (
    Portfolio,
    Testimonial,
    Certificado
)


class IndexView(generic.TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        testimonials = Testimonial.objects.filter(es_activo=True)
        certificados = Certificado.objects.filter(es_activo=True)
        portfolio = Portfolio.objects.filter(es_activo=True)
        habilidades = Habilidad.objects.filter(is_key_skill=True)

        context['testimonials'] = testimonials
        context['certificados'] = certificados
        context['portfolio'] = portfolio
        context['habilidades'] = habilidades
        return context
