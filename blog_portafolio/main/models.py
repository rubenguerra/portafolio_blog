from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField


class Habilidad(models.Model):
    class Meta:
        verbose_name_plural = 'Habilidades'
        verbose_name = 'Habilidad'

    nombre = models.CharField(max_length=20, blank=True, null=True)
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
    bio = models.TextField(blank=True, null=True)
    habilidades = models.ManyToManyField(Habilidad, blank=True)
    cv = models.FileField(blank=True, null=True, upload_to='cv')

    def __str__(self):
        return f'{self.usuario}'


class ContactProfile(models.Model):
    class Meta:
        verbose_name_plural = 'Perfiles de contactos'
        verbose_name = 'Perfil de contacto'
        ordering = ['timestamp']

    timestamp = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=100)
    email = models.EmailField(verbose_name='Email')

    mensaje = models.TextField(verbose_name='Message')

    def __str__(self):
        return f'{self.nombre}'


class Testimonial(models.Model):
    class Meta:
        verbose_name_plural = 'Testimonials'
        verbose_name = 'Testimonial'

    thumbnail = models.ImageField(blank=True, null=True, upload_to='testimonio')
    nombre = models.CharField(max_length=200, blank=True, null=True)
    rol = models.CharField(max_length=200, blank=True, null=True)
    cita = models.CharField(max_length=500, blank=True, null=True)
    es_activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Media(models.Model):
    class Meta:
        verbose_name_plural = 'Archivos Media'
        verbose_name = 'Media'
        ordering = ['nombre']

    imagen = models.ImageField(blank=True, null=True, upload_to='media')
    url = models.URLField(blank=True, null=True)
    nombre = models.CharField(max_length=200, blank=True, null=True)
    es_imagen = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.url:
            self.es_imagen = False
        super(Media, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Portfolio(models.Model):
    class Meta:
        verbose_name_plural = 'Perfiles de Portafolio'
        verbose_name = 'Portafolio'
        ordering = ['nombre']

    fecha = models.DateTimeField(blank=True, null=True)
    nombre = models.CharField(max_length=200, blank=True, null=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    texto = RichTextField(blank=True, null=True)
    imagen = models.ImageField(blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    es_activo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.nombre)
        super(Portfolio, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return f"/portfolio/{self.slug}"


class Blog(models.Model):
    class Meta:
        verbose_name_plural = 'Perfiles de Blog'
        verbose_name = 'Blog'
        ordering = ['timestamp']

    timestamp = models.DateTimeField(auto_now_add=True)
    autor = models.CharField(max_length=200, blank=True, null=True)
    nombre = models.CharField(max_length=200, blank=True, null=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    contenido = RichTextField(blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    es_activo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.nombre)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return f"/blog/{self.slug}"


class Certificado(models.Model):
    class Meta:
        verbose_name_plural = 'Certificados'
        verbose_name = 'Certificado'

    fecha = models.DateTimeField(blank=True, null=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    titulo = models.CharField(max_length=200, blank=True, null=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    es_activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
