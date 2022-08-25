from django import forms
from .models import Contacto, Comentario


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('nombre', 'email', 'contenido')


class FormBuscar(forms.Form):
    busqueda = forms.CharField(required=False, min_length=3)
    buscar_en = forms.ChoiceField(required=False, choices=(("titulo", "Titulo"), ("autor", "Autor")))


class EmailPostForm(forms.Form):
    """
    Formulario para compartir post a través de contacto por e-mail.
    """
    nombre = forms.CharField(max_length=25)
    email = forms.EmailField()
    a = forms.EmailField()
    comentario = forms.CharField(required=False, widget=forms.Textarea)


"""

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = '__all__'
        exclude = ('estado',)

        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su nombre',
                }
            ),
            'apellido': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su apellido',
                }
            ),
            'correo': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su correo electrónico',
                }
            ),
            'asunto': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Asunto',
                }
            ),
            'mensaje': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Escriba su mensaje',
                }
            )
        }

"""


class ContactForm(forms.ModelForm):
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
