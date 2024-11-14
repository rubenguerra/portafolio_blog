import random

# from django.conf.global_settings import EMAIL_HOST_USER
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.core.mail import send_mail
from taggit.models import Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages

from django.http import HttpResponse

from .models import *  # RedesSociales, Web
from .utils import *
from .formularios import *


def post_list(request, tag_slug=None):
    object_list = Post.publico.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # Despliega 3 post en cada página
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera del rango devuelve última pagina de resultados
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/lista.html', {'page': page,
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

        try:
            post_linguistica = Post.objects.filter(
                estado=True,
                publicado=True,
                categoria=Categoria.objects.get(nombre='Linguistica')
            ).latest('fecha_publicacion')

        except:
            post_linguistica = None

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
            'post_linguistica': post_linguistica,
            # 'sociales': obtenerRedes(),
            # 'web': obtenerWeb(),
        }

        return render(request, 'blog/inicio.html', contexto)

"""
class Inicio(ListView):
    def get(self, request, *args, **kwargs):
        # Get all active and published posts in a single query
        active_posts = Post.objects.filter(
            estado=True,
            publicado=True
        )

        # Get random posts for featured section
        random_posts = self._get_random_posts(active_posts)
        if not random_posts:
            return render(request, 'blog/inicio.html', {'error': 'No posts available'})

        # Get latest posts by category in a single query
        latest_category_posts = self._get_latest_category_posts()

        contexto = {
            'principal': random_posts['principal'],
            'post1': random_posts['posts'][0],
            'post2': random_posts['posts'][1],
            'post3': random_posts['posts'][2],
            'post4': random_posts['posts'][3],
            **latest_category_posts
        }

        return render(request, 'blog/inicio.html', contexto)

    def _get_random_posts(self, queryset):
        Get random posts for featured section
        posts_ids = list(queryset.values_list('id', flat=True))
        if len(posts_ids) < 5:  # We need at least 5 posts
            return None

        # Get random posts in a more efficient way
        random.shuffle(posts_ids)

        
        return {
            'principal': selected_posts[0],
            'posts': [consulta(post) for post in selected_posts[1:5]]
        }

    def _get_latest_category_posts(self):
        Get latest post for each category in a single query
        categories = {
            'General': 'post_general',
            'Machine Learning': 'post_machine_learning',
            'Deep Learning': 'post_deep_learning',
            'Programacion': 'post_programacion',
            'Linguistica': 'post_linguistica'
        }

        # Get all categories in one query
        category_objects = Categoria.objects.filter(nombre__in=categories.keys())
        
        # Get latest posts for all categories in one query
        latest_posts = Post.objects.filter(
            estado=True,
            publicado=True,
            categoria__in=category_objects
        ).order_by('categoria', '-fecha_publicacion').distinct('categoria')
        # distinct('categoria') funciona con PostgreSQL.
        # Create dictionary with latest posts
        result = {categories[post.categoria.nombre]: post for post in latest_posts}
        
        # Fill in None for categories without posts
        for category_name, context_key in categories.items():
            if context_key not in result:
                result[context_key] = None

        return result

"""

class Listado(ListView):

    def get(self, request, nombre_categoria, *args, **kwargs):
        contexto = generarCategoria(request, nombre_categoria)
        return render(request, 'blog/categoria.html', contexto)


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
            return redirect('blog/inicio.html')
        else:
            contexto = {
                'form': form,
            }
            return render(request, 'contacto.html', contexto)


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



class DetallePost(DetailView):
    form_class = ComentarioForm
    template_name = 'comentarios.html'

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug, estado=True)

        # Listado de comentarios para este post
        comentarios = post.comentarios.filter(activo=True)
        comentario_form = ComentarioForm()

        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)  # Excluye el post presente
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publicado')[:4]

        contexto = {'post': post,
                    'comentarios': comentarios,
                    'similar_posts': similar_posts,
                    'comentario_form': comentario_form}

        return render(request, "blog/post.html", contexto)

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug, estado=True)

        # Listado de comentarios para este post
        comentarios = post.comentarios.filter(activo=True)

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

        # Lista de posts similares
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)  # Excluye el post presente
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publicado')[:4]

        contexto = {'post': post,
                    'comentarios': comentarios,
                    'similar_posts': similar_posts,
                    'nuevo_comentario': nuevo_comentario,
                    'comentario_form': comentario_form}

        return render(request, "blog/post.html", contexto)


def post_share(request, post_id):
    """
    Vista para el formulario de compartir post.
    Regresa el post por su id.
    """
    post = get_object_or_404(Post, id=post_id, estado=True, publicado=True)
    enviado = False

    if request.method == 'POST':
        # Formulario que será enviado
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Validación de formulario
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['nombre']} recomienda que leas este post: {post.titulo}"
            mensaje = f"Lee {post.titulo} este interesante post: {post_url}\n\n" \
                      f"de {cd['nombre']}: {cd['comentario']}"
            send_mail(subject, mensaje, [cd['email']], [cd['a']])
            enviado = True

    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', {'post': post, 'form': form, 'sent': enviado})


class ContactView(FormView):
    template_name = "main/contacto.html"
    form_class = ContactForm
    success_url = "/"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Gracias. Estaremos en contacto pronto...")  # Añadir el mensaje en el template
        return super().form_valid(form)


def suscribir(request, pk=None):
    if pk is not None:
        suscriptor = get_object_or_404(Suscriptores, pk=pk)
    else:
        suscriptor = None
    if request.method == "POST":
        form = SuscriptoresForm(request.POST, instance=suscriptor)
        if form.is_valid():
            suscribir_nuevo = form.save()
            if suscriptor is None:
                messages.success(request,
                                 "Te has suscrito a nuestra página. ¡Gracias por tu apoyo!".format(suscribir_nuevo))
                correo = request.POST.get('correo')
                asunto = '¡GRACIAS POR SUSCRIBIRTE!'
                mensaje = 'Te has suscrito exitosamente a nuestro blog. ¡¡Gracias por tu apoyo!!'
                try:
                    send_mail(asunto, mensaje, EMAIL_HOST_USER, [correo])
                except:
                    pass

            return redirect('blog:suscriptor_listo', suscribir_nuevo.pk)
    else:
        form = SuscriptoresForm(instance=suscriptor)
    return render(request, "blog/form_example.html", {"metodo": request.method, "form": form})
