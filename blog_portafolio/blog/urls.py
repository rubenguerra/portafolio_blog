from django.urls import path

from .views import *

app_name = 'blog'

urlpatterns = [
    path('', Inicio.as_view(), name='index'),
    path('general/', Listado.as_view(), {'nombre_categoria': 'General'}, name='general'),
    path('machinelearning/', Listado.as_view(), {'nombre_categoria': 'Machine Learning'}, name='machinelearning'),
    path('deeplearning/', Listado.as_view(), {'nombre_categoria': 'Deep Learning'}, name='deeplearning'),
    path('contacto/', ContactView.as_view(), name='contacto'),
    path('formulario_contacto/', FormularioContacto.as_view(), name='formulario_contacto'),
    path('<slug:slug>/', DetallePost.as_view(), name='detalle_post'),
    path('suscribirse/', Suscribir.as_view(), name='suscribirse'),
    path('buscar-post', buscar_post, name='buscar'),
    path('posts/<int:pk>/', detalles_post, name='detalles_post'),

    path('list/', post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
    path('<int:post_id>/share/', post_share, name='post_share')
]
# ['posts/(?P<pk>[0-9]+)/$']
