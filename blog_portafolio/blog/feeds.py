from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post


class LatestPostsFeed(Feed):
    title = 'IA Blog'
    link = reverse_lazy('list')
    description = 'Nuevos posts de mi blog.'

    def items(self):
        return Post.publicado.all()[:5]

    def item_title(self, item):
        return item.titulo

    def item_description(self, item):
        return truncatewords(item.body, 30)
