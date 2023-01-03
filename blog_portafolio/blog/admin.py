from django.contrib import admin
from .models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'slug', 'autor', 'categoria', 'fecha_publicacion', 'estado')
    list_filter = ('estado', 'fecha_publicacion', 'autor')
    search_fields = ('titulo', 'contenido')
    prepopulated_fields = {'slug': ('titulo',), }


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'email')
    list_filter = ('usuario',)
    search_fields = ('usuario', 'post')


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'post', 'creado', 'activo')
    list_filter = ('activo', 'creado', 'actualizado')
    search_fields = ('nombre', 'email', 'contenido')


@admin.register(Contacto)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'correo', 'asunto', 'mensaje')


@admin.register(Suscriptores)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'correo')


@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'score')


admin.site.register(Categoria)
admin.site.register(Web)
admin.site.register(RedesSociales)
