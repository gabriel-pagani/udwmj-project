from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Recipe


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput()
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput()
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput()
    )


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already in use.')
        return username


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'instructions',
                  'preparation_time', 'servings', 'cover', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Recipe title'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Brief description of the recipe'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Detailed cooking instructions...',
                'rows': 3
            }),
            'preparation_time': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Minutes',
                'min': 1
            }),
            'servings': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Number of people',
                'min': 1
            }),
            'cover': forms.FileInput(attrs={
                'class': 'form-file-input',
                'accept': 'image/*'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            })
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise forms.ValidationError(
                'Title must be at least 3 characters long.')
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 10:
            raise forms.ValidationError(
                'Description must be at least 10 characters long.')
        return description

    def clean_instructions(self):
        instructions = self.cleaned_data.get('instructions')
        if len(instructions) < 20:
            raise forms.ValidationError(
                'Instructions must be at least 20 characters long.')
        return instructions
