import random

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, FormView

from django.core.mail import send_mail
from taggit.models import Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
# from blog_portafolio.settings import EMAIL_HOST_USER
# from .formularios import FormBuscar, ContactoForm

from .models import *  # RedesSociales, Web
from .utils import *
from .formularios import *


def post_list(request, tag_slug=None):
    object_list = Post.publico.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'list.html', {'page': page,
                                         'posts': posts,
                                         'tag': tag})


class Inicio(ListView):

    def get(self, request, *args, **kwargs):
        posts = list(Post.objects.filter(
            estado=True,
            publicado=True
        ).values_list('id', flat=True))
        principal = random.choice(posts)
        posts.remove(principal)
        principal = Post.objects.get(id=principal)

        post1 = random.choice(posts)
        posts.remove(post1)
        post2 = random.choice(posts)
        posts.remove(post2)
        post3 = random.choice(posts)
        posts.remove(post3)
        post4 = random.choice(posts)
        posts.remove(post4)

        try:
            post_general = Post.objects.filter(
                estado=True,
                publicado=True,
                categoria=Categoria.objects.get(nombre='General')
            ).latest('fecha_publicacion')

        except:
            post_general = None

        try:
            post_machine_learning = Post.objects.filter(
                estado=True,
                publicado=True,
                categoria=Categoria.objects.get(nombre='Machine Learning')
            ).latest('fecha_publicacion')

        except:
            post_machine_learning = None

        try:
            post_deep_learning = Post.objects.filter(
                estado=True,
                publicado=True,
                categoria=Categoria.objects.get(nombre='Deep Learning')
            ).latest('fecha_publicacion')

        except:
            post_deep_learning = None

        try:
            post_programacion = Post.objects.filter(
                estado=True,
                publicado=True,
                categoria=Categoria.objects.get(nombre='Programacion')
            ).latest('fecha_publicacion')

        except:
            post_programacion = None

        contexto = {
            'principal': principal,
            'post1': consulta(post1),
            'post2': consulta(post2),
            'post3': consulta(post3),
            'post4': consulta(post4),
            'post_general': post_general,
            'post_machine_learning': post_machine_learning,
            'post_deep_learning': post_deep_learning,
            'post_programacion': post_programacion,
            # 'sociales': obtenerRedes(),
            # 'web': obtenerWeb(),
        }

        return render(request, 'inicio.html', contexto)


class Listado(ListView):

    def get(self, request, nombre_categoria, *args, **kwargs):
        contexto = generarCategoria(request, nombre_categoria)
        return render(request, 'categoria.html', contexto)




"""


class FormularioContacto(View):
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        contexto = {
            'form': form
        }
        return render(request, 'contacto.html', contexto)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:index.html')
        else:
            contexto = {
                'form': form,
            }
            return render(request, 'contacto', contexto)
"""


def buscar_post(request):
    texto_buscado = request.GET.get("buscar", "")
    form = FormBuscar(request.GET)

    posts = set()

    if form.is_valid() and form.cleaned_data["buscar"]:
        buscar = form.cleaned_data["buscar"]
        buscar_en = form.cleaned_data.get("buscar_en") or "titulo"
        if buscar_en == "titulo":
            posts = Post.objects.filter(titulo__icontains=buscar)
        else:
            nombre_autor = User.objects.filter(nombre__icontains=buscar)

            for autor in nombre_autor:
                for post in autor.post_set.all():
                    posts.add(post)

            apellido_autor = User.objects.filter(apellidos__icontains=buscar)

            for autor in apellido_autor:
                for post in autor.post_set.all():
                    posts.add(post)

    return render(request, "buscar.html", {"form": form, "texto_buscado": texto_buscado, "posts": posts})


def detalles_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Listado de comentarios para este post
    comentarios = post.comentarios.filter(estado=True)  # Agregar un publicado = True

    nuevo_comentario = None

    if request.method == 'POST':
        # Un comentario fue realizado
        comentario_form = ComentarioForm(data=request.POST)
        if comentario_form.is_valid():
            # Se crea el comentario pero no se guarda en la base de datos aun
            nuevo_comentario = comentario_form.save(commit=False)
            # Se asigna al post el comentario
            nuevo_comentario.post = post
            # Guarda el comentario en la base de datos
            nuevo_comentario.save()
    else:
        comentario_form = ComentarioForm()

    contexto = {'post': post,
                'comentarios': comentarios,
                'nuevo_comentario': nuevo_comentario,
                'comentario_form': comentario_form}
    return render(request, "detalles_post.html", contexto)


"""
Estas dos funciones a continuación son una prueba para listar y detallar los posts usando el administrador
construido por nosotros AdminPublicado()
"""


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             estado=True,
                             fecha_publicacion__year=year,
                             fecha_publicacion__month=month,
                             fecha_publicacion__day=day)

    # Listado de comentarios para este post
    comentarios = post.comentarios.filter(estado=True)

    nuevo_comentario = None

    if request.method == 'POST':
        # Un comentario fue realizado
        comentario_form = ComentarioForm(data=request.POST)
        if comentario_form.is_valid():
            # Se crea el comentario pero no se guarda en la base de datos aun
            nuevo_comentario = comentario_form.save(commit=False)
            # Se asigna al post el comentario
            nuevo_comentario.post = post
            # Guarda el comentario en la base de datos
            nuevo_comentario.save()
    else:
        comentario_form = ComentarioForm()

    contexto = {'post': post,
                'comentarios': comentarios,
                'nuevo_comentario': nuevo_comentario,
                'comentario_form': comentario_form}

    return render(request, 'post.html', contexto)


"""
class DetallePost(DetailView):
    def get(self, request, slug, *args, **kwargs):
        try:
            post = Post.objects.get(slug=slug)
        except:
            post = None

        contexto = {
            'post': post,
        }
        return render(request, 'post.html', contexto)

"""


class DetallePost(DetailView):
    def get(self, request, slug, *args, **kwargs):
        try:
            post = get_object_or_404(Post, slug=slug)
        except:
            post = None

        # Listado de comentarios para este post
        comentarios = post.comentarios.filter(estado=True)

        nuevo_comentario = None

        if request.method == 'POST':
            # Un comentario fue realizado
            comentario_form = ComentarioForm(data=request.POST)
            if comentario_form.is_valid():
                # Se crea el comentario pero no se guarda en la base de datos aun
                nuevo_comentario = comentario_form.save(commit=False)
                # Se asigna al post el comentario
                nuevo_comentario.post = post
                # Guarda el comentario en la base de datos
                nuevo_comentario.save()
        else:
            comentario_form = ComentarioForm()

        contexto = {'post': post,
                    'comentarios': comentarios,
                    'nuevo_comentario': nuevo_comentario,
                    'comentario_form': comentario_form}
        return render(request, "post.html", contexto)


class Suscribir(View):
    def post(self, request, *args, **kwargs):
        correo = request.POST.get('correo')
        Suscriptores.objects.create(correo=correo)
        asunto = '¡GRACIAS POR SUSCRIBIRTE A NUESTRO BLOG!'
        mensaje = 'Te has suscrito exitosamente a nuestro blog. ¡¡Gracias por tu apoyo!!'
        try:
            send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [correo])
        except:
            pass

        return redirect('blog:index')  # Corregir


def post_share(request, post_id):
    """
    Vista para el formulario de compartir post
    """
    # Regresa el post por su id
    post = get_object_or_404(Post, id=post_id, estado=True, publicado=True)
    sent = False

    if request.method == 'POST':
        # Formulario que será enviado
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Validacion de formulario
            cd = form.cleaned_data
    else:
        form = EmailPostForm()
    return render(request, 'share.html', {'post': post, 'form': form})


class ContactView(FormView):
    template_name = "main/contacto.html"
    form_class = ContactForm
    success_url = "/"

    def form_valid(self, form):
        form.save()
        # messages.success(self.request, "Gracias. Estaremos en contacto pronto...")
        return super().form_valid(form)
