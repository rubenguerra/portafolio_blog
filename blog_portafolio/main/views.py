from django.shortcuts import render
from django.contrib import messages
from .models import (
    UserProfile,
    Blog,
    Portfolio,
    Testimonial,
    Certificado
)

from django.views import generic
from .forms import ContactForm


class IndexView(generic.TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        testimonials = Testimonial.objects.filter(es_activo=True)
        certificados = Certificado.objects.filter(es_activo=True)
        blogs = Blog.objects.filter(es_activo=True)
        portfolio = Portfolio.objects.filter(es_activo=True)

        context['testimonials'] = testimonials
        context['certificados'] = certificados
        context['blogs'] = blogs
        context['portfolio'] = portfolio
        return context


class ContactView(generic.FormView):
    template_name = "main/contacto.html"
    form_class = ContactForm
    success_url = "/"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Gracias. Estaremos en contacto pronto...")
        return super().form_valid(form)


class PortfolioView(generic.TemplateView):
    modelo = Portfolio
    template_name = "main/portfolio.html"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(es_activo=True)


class PortfolioDetailView(generic.DetailView):
    modelo = Portfolio
    template_name = "main/portfolio-detalle.html"


class BlogView(generic.ListView):
    modelo = Blog
    template_name = "main/blog.html"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(es_activo=True)


class BlogDetailView(generic.DetailView):
    modelo = Blog
    template_name = "main/blog-detalle.html"
