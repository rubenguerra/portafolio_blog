from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post


class LatestPostsFeed(Feed):
    title = 'Inteligencia Artificial'
    link = reverse_lazy('blog:index')
    description = 'Nuevos posts en el blog.'

    def items(self):
        return Post.publico.all()[:5]

    def item_title(self, item):
        return item.titulo

    def item_description(self, item):
        return truncatewords(item.descripcion, 30)  # Podría ser contenido en vez de descripción.
