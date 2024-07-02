from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from .models import User

class SignUpForm(UserCreationForm):
    user_id = forms.CharField(max_length=50, required=True, widget=forms.TextInput())
    user_email = forms.EmailField(max_length=200, required=True, widget=forms.EmailInput())
    user_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput())
    user_phone = forms.CharField(max_length=20, required=True, widget=forms.TextInput())
    user_birth = forms.DateField(required=True, widget=forms.DateInput())
    user_address = forms.CharField(max_length=255, required=False, widget=forms.TextInput())

    class Meta:
        model = User
        fields = ('user_id', 'user_email', 'user_name', 'user_phone', 'user_birth', 'user_address', 'password1', 'password2')

