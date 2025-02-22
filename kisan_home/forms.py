from django import forms
from .models import contactForm


class ContactForm(forms.ModelForm):
    class Meta:
        model = contactForm
        fields = ['name','email','message']
