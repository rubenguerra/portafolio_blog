from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class ModeloBase(models.Model):
    id = models.AutoField(primary_key=True)
    estado = models.BooleanField('Estado', default=True)
    fecha_creacion = models.DateField('Fecha de Creación', auto_now=False, auto_now_add=True)
    fecha_modificacion = models.DateField('Fecha de Modificación', auto_now=True, auto_now_add=False)
    fecha_eliminacion = models.DateField('Fecha de Eliminación', auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True


class Habilidad(models.Model):
    class Meta:
        verbose_name_plural = 'Habilidades'
        verbose_name = 'Habilidad'

    nombre = models.CharField(max_length=50, blank=True, null=True)
    score = models.IntegerField(default=80, blank=True, null=True)
    imagen = models.FileField(blank=True, null=True, upload_to='habilidades')
    is_key_skill = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class UserProfile(models.Model):
    class Meta:
        verbose_name_plural = 'Perfiles de Usuarios'
        verbose_name = 'Perfil de Usuario'

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, null=True, upload_to='avatar')
    titulo = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField('Correo Electrónico', max_length=200)
    bio = models.TextField(blank=True, null=True)
    habilidades = models.ManyToManyField(Habilidad, blank=True)
    facebook = models.URLField('Facebook', null=True, blank=True)
    twitter = models.URLField('Twitter', null=True, blank=True)
    instagram = models.URLField('Instagram', null=True, blank=True)
    cv = models.FileField(blank=True, null=True, upload_to='cv/')

    def __str__(self):
        return f'{self.usuario}'


class Categoria(ModeloBase):
    nombre = models.CharField('Nombre de la Categoría', max_length=100, unique=True)
    imagen_referencial = models.ImageField('Imagen Referencial', upload_to='categoria/')
    objects = models.Manager()  # Puedo eliminar...

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre


class AdminPublicado(models.Manager):  # Revisar aqui
    def get_queryset(self):
        return super(AdminPublicado, self).get_queryset().filter(estado=True, publicado=True)


class Post(ModeloBase):
    titulo = models.CharField('Título del Post', max_length=150, unique=True)
    slug = models.SlugField('Slug', max_length=250, unique=True, null=False, unique_for_date='fecha_publicacion')
    descripcion = models.TextField('Descripción')
    autor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='blog_posts')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    contenido = RichTextUploadingField(verbose_name='Contenido')
    imagen_referencial = models.ImageField('Imagen Referencial', upload_to='imagenes/', max_length=255)
    publicado = models.BooleanField('Publicado / No Publicado', default=False)
    fecha_publicacion = models.DateTimeField('Fecha de Publicación', default=timezone.now)
    objects = models.Manager()  # El administrador por defecto
    publico = AdminPublicado()  # Administrador construido
    tags = TaggableManager()  # Permite usar palabras clave en nuestros posts.

    """
    Vamos a definir una ruta absoluta para los posts
    """

    def get_absolute_url(self):
        return reverse('blog:detalle_post', args=[self.slug])

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('-fecha_publicacion',)

    def __str__(self):
        return self.titulo


class Web(ModeloBase):
    nosotros = models.TextField('Nosotros')
    telefono = models.CharField('Teléfono', max_length=10)
    email = models.EmailField('Correo Electrónico', max_length=200)
    direccion = models.CharField('Dirección', max_length=200)

    class Meta:
        verbose_name = 'Web'
        verbose_name_plural = 'Webs'

    def __str__(self):
        return self.nosotros


class RedesSociales(ModeloBase):
    facebook = models.URLField('Facebook')
    twitter = models.URLField('Twitter')
    instagram = models.URLField('Instagram')

    class Meta:
        verbose_name = 'Red Social'
        verbose_name_plural = 'Redes Sociales'

    def __str__(self):
        return self.facebook


class Contacto(ModeloBase):
    nombre = models.CharField(max_length=100)  # Formulario que recoge los datos de quien nos está contactando
    correo = models.EmailField(max_length=250)
    asunto = models.CharField(max_length=100)
    mensaje = models.TextField('Mensaje')

    # timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
        # ordering = ['timestamp']

    def __str__(self):
        return self.asunto


class Suscriptores(ModeloBase):
    correo = models.EmailField(unique=True, max_length=200)

    class Meta:
        verbose_name = 'Suscriptor'
        verbose_name_plural = 'Suscriptores'

    def __str__(self):
        return self.correo


class Comentario(ModeloBase):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    nombre = models.CharField(max_length=80)
    email = models.EmailField()
    contenido = models.CharField(max_length=1000)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ('creado',)
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return f'Comentado por {self.nombre} a {self.post}'
