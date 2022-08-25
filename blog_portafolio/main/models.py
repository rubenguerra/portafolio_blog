from django.db import models
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify


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


class Certificado(models.Model):
    class Meta:
        verbose_name_plural = 'Certificados'
        verbose_name = 'Certificado'

    fecha = models.DateTimeField(blank=True, null=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    titulo = models.CharField(max_length=200, blank=True, null=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    imagen = models.ImageField(blank=True, null=True)
    es_activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
