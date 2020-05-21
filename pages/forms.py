from django import forms
from django.forms import ModelForm
from .models import Project, Contact
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProjectForm(ModelForm):
    class Meta:
        model = Project

        fields = '__all__'
        widgets = {
            'external_links': forms.Textarea(attrs={'placeholder': 'Paste Important Links'}),
            'sign_details': forms.Textarea(attrs={'placeholder': 'Add sign info from right side here for file-keeping'}),

        }


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
