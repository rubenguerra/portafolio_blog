from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemaps(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.publico.all()

    def lastmod(self, obj):
        return obj.fecha_modificacion
