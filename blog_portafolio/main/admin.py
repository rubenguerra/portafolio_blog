from django.contrib import admin

from .models import (
    Testimonial,
    Media,
    Portfolio,
    Certificado,
)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'es_activo')


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'es_activo')
    readonly_fields = ('slug',)


@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
