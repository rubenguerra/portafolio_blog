from django import forms
from .models import Contacto, Comentario, Post, Suscriptores


class SuscriptoresForm(forms.ModelForm):
    class Meta:
        model = Suscriptores
        fields = ('correo',)


class FormBuscar(forms.Form):
    busqueda = forms.CharField(required=False, min_length=3)
    buscar_en = forms.ChoiceField(required=False, choices=(("titulo", "Titulo"), ("autor", "Autor")))


class ComentarioForm(forms.ModelForm):
    # Formulario de prueba para los comentarios

    nombre = forms.CharField(max_length=25,
                             widget=forms.TextInput(
                                 attrs={'cols': 43, 'rows': 1,
                                        'style': 'max-width: 99%; min-width: 99%; max-height: 1.2rem; min-height: 1.2rem; font-size: 90%'}))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'cols': 43, 'rows': 1,
                                                            'style': 'max-width: 99%; min-width: 99%; max-height: 1.2rem; min-height: 1.2rem; font-size: 90%'
                                                                           }))
    contenido = forms.CharField(widget=forms.Textarea(attrs={'cols': 43, 'rows': 10,
                                                             'style': 'max-width: 99%; min-width: 99%; max-height: 10rem; min-height: 5rem; font-size: 90%'
                                                             }))

    class Meta:
        model = Comentario
        fields = ('nombre', 'email', 'contenido',)



"""
Esta es una prueba de comentarios a los posts
tomado de: https://realpython.com/build-a-blog-from-scratch-django/#make-your-blog-look-nice


class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Name"}
        ),
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Leave a comment!"}
        )
    )

"""


class EmailPostForm(forms.Form):
    """
    Formulario para compartir post a través de contacto por e-mail.
    """
    nombre = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'cols': 43, 'rows': 1,
                                                                          'style': 'max-width: 99%; min-width: 99%; max-height: 1.2rem;'
                                                                                   'min-height: 1.2rem; font-size: 90%'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'cols': 43, 'rows': 1,
                                                                           'style': 'max-width: 99%; min-width: 99%; max-height: 1.2rem;'
                                                                                    'min-height: 1.2rem; font-size: 90%'
                                                                           }))
    a = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'cols': 43, 'rows': 1,
                                                                       'style': 'max-width: 99%; min-width: 99%; max-height: 1.2rem;'
                                                                                'min-height: 1.2rem; font-size: 90%'
                                                                       }))
    comentario = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': 43, 'rows': 10,
                                                                              'style': 'max-width: 99%; min-width: 99%; max-height: 10rem;'
                                                                                       'min-height: 5rem; font-size: 90%'
                                                                              }))


class ContactForm(forms.ModelForm):
    """
    Formulario para los mensajes de contacto
    """
    nombre = forms.CharField(required=True,
                             widget=forms.TextInput(attrs={
                                 'placeholder': '* Nombre...',
                             }))
    correo = forms.EmailField(required=True,
                              widget=forms.TextInput(attrs={
                                  'placeholder': '* Email...',
                              }))
    asunto = forms.CharField(required=True,
                             widget=forms.TextInput(attrs={
                                 'placeholder': '* Asunto...',
                             }))

    mensaje = forms.CharField(max_length=1000, required=True,
                              widget=forms.TextInput(attrs={
                                  'placeholder': '* Mensaje...',
                                  'rows': 7,
                              }))

    class Meta:
        model = Contacto
        fields = ('nombre', 'correo', 'asunto', 'mensaje',)
