from django import template
from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.publico.count()


@register.inclusion_tag('blog/ultimo_post.html')
def mostrar_ultimos_posts(count=5):
    ultimos_posts = Post.publico.order_by('-fecha_publicacion')[:count]
    return {'ultimos_posts': ultimos_posts}
