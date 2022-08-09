from django.contrib import admin

from .models import (
    UserProfile,
    ContactProfile,
    Testimonial,
    Media,
    Portfolio,
    Blog,
    Certificado,
    Habilidad
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario')


@admin.register(ContactProfile)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'nombre')


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


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'es_activo')
    readonly_fields = ('slug',)


@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')


@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'score')
