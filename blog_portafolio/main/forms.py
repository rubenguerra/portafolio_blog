"""

from django import forms
from .models import ContactProfile


class ContactForm(forms.ModelForm):
    nombre = forms.CharField(max_length=100, required=True,
                             widget=forms.TextInput(attrs={
                                 'placeholder': '* Nombre...',
                             }))
    email = forms.EmailField(max_length=254, required=True,
                             widget=forms.TextInput(attrs={
                                 'placeholder': '* Email...',
                             }))
    mensaje = forms.CharField(max_length=1000, required=True,
                              widget=forms.TextInput(attrs={
                                  'placeholder': '* Mensaje...',
                                  'rows': 7,
                              }))

    class Meta:
        model = ContactProfile
        fields = ('nombre', 'email', 'mensaje',)
"""
