from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.publico.count()


@register.inclusion_tag('blog/ultimo_post.html')
def mostrar_ultimos_posts(count=5):
    ultimos_posts = Post.publico.order_by('-fecha_publicacion')[:count]
    return {'ultimos_posts': ultimos_posts}


@register.inclusion_tag('blog/mas_comentados.html')
def get_posts_mas_comentados(count=5):
    mas_comentados = Post.publico.annotate(total_comentarios=Count('comentarios')).order_by('-total_comentarios')[
                     :count]
    return {'mas_comentados': mas_comentados, 'cuenta': count}
