from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import *

class SignUpForm(UserCreationForm):
    user_id = forms.CharField(
        max_length=50, 
        required=True, 
        widget=forms.TextInput(), 
        error_messages={
            'required': 'ID is required',
            'max_length': 'ID cannot exceed 50 characters'
        }
    )
    user_email = forms.EmailField(
        max_length=200, 
        required=True, 
        widget=forms.EmailInput(), 
        error_messages={
            'required': 'Email is required',
            'invalid': 'Enter a valid email address',
            'max_length': 'Email cannot exceed 200 characters'
        }
    )
    user_name = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(), 
        error_messages={
            'required': 'Name is required',
            'max_length': 'Name cannot exceed 100 characters'
        }
    )
    user_phone = forms.CharField(
        max_length=20, 
        required=True, 
        widget=forms.TextInput(), 
        validators=[
            RegexValidator(
                regex=r'^010-\d{4}-\d{4}$',
                message='Phone number must be in the format 010-1234-5678'
            )
        ],
        error_messages={
            'required': 'Phone number is required',
            'max_length': 'Phone number cannot exceed 20 characters',
            'invalid': 'Phone number must be in the format 010-1234-5678'
        }
    )
    user_birth = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'placeholder': 'yyyy-mm-dd'}), 
        validators=[
            RegexValidator(
                regex=r'^\d{4}-\d{2}-\d{2}$',
                message='Birth date must be in the format yyyy-mm-dd'
            )
        ],
        error_messages={
            'required': 'Birth date is required',
            'invalid': 'Enter a valid birth date in the format yyyy-mm-dd'
        }
    )
    user_address = forms.CharField(
        max_length=255, 
        required=True, 
        widget=forms.TextInput(), 
        error_messages={
            'required': 'Address is required',
            'max_length': 'Address cannot exceed 255 characters'
        }
    )
    #<!-- 상세 주소 -->
    # user_address_Detail = forms.CharField(
    #     max_length=255, 
    #     required=True, 
    #     widget=forms.TextInput(), 
    #     error_messages={
    #         'required': 'Address is required',
    #         'max_length': 'Address cannot exceed 255 characters'
    #     }
    # )

    class Meta:
        model = User
        fields = ('user_id', 'user_email', 'user_name', 'user_phone', 'user_birth', 'user_address', 'password1', 'password2') #'user_address_Detail')

class PostForm(forms.ModelForm):
    beach_no = forms.ModelChoiceField(queryset=Beach.objects.all(), required=False, label='해수욕장')

    class Meta:
        model = Notice_board
        fields = ['notice_title', 'notice_contents', 'beach_no', 'notice_img']
        widgets = {
            'notice_title': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 200, 'required': True}),
            'notice_contents': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'required': True}),
            'notice_img': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
        
class FreePostForm(forms.ModelForm):
    beach_no = forms.ModelChoiceField(queryset=Beach.objects.all(), required=False, label='해수욕장')

    class Meta:
        model = Event_board
        fields = ['event_title', 'event_contents', 'beach_no', 'event_img']
        widgets = {
            'event_title': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 200, 'required': True}),
            'event_contents': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'required': True}),
            'event_img': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
        
        
class SignUpForm(UserCreationForm):
    user_id = forms.CharField(
        max_length=50, 
        required=True, 
        widget=forms.TextInput(), 
        error_messages={
            'required': 'ID is required',
            'max_length': 'ID cannot exceed 50 characters'
        }
    )
    user_email = forms.EmailField(
        max_length=200, 
        required=True, 
        widget=forms.EmailInput(), 
        error_messages={
            'required': 'Email is required',
            'invalid': 'Enter a valid email address',
            'max_length': 'Email cannot exceed 200 characters'
        }
    )
    user_name = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(), 
        error_messages={
            'required': 'Name is required',
            'max_length': 'Name cannot exceed 100 characters'
        }
    )
    user_phone = forms.CharField(
        max_length=20, 
        required=True, 
        widget=forms.TextInput(), 
        validators=[
            RegexValidator(
                regex=r'^010-\d{4}-\d{4}$',
                message='Phone number must be in the format 010-1234-5678'
            )
        ],
        error_messages={
            'required': 'Phone number is required',
            'max_length': 'Phone number cannot exceed 20 characters',
            'invalid': 'Phone number must be in the format 010-1234-5678'
        }
    )
    user_birth = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'placeholder': 'yyyy-mm-dd'}), 
        validators=[
            RegexValidator(
                regex=r'^\d{4}-\d{2}-\d{2}$',
                message='Birth date must be in the format yyyy-mm-dd'
            )
        ],
        error_messages={
            'required': 'Birth date is required',
            'invalid': 'Enter a valid birth date in the format yyyy-mm-dd'
        }
    )
    user_address = forms.CharField(
        max_length=255, 
        required=True, 
        widget=forms.TextInput(), 
        error_messages={
            'required': 'Address is required',
            'max_length': 'Address cannot exceed 255 characters'
        }
    )
    #<!-- 상세 주소 -->
    # user_address_Detail = forms.CharField(
    #     max_length=255, 
    #     required=True, 
    #     widget=forms.TextInput(), 
    #     error_messages={
    #         'required': 'Address is required',
    #         'max_length': 'Address cannot exceed 255 characters'
    #     }
    # )

    class Meta:
        model = User
        fields = ('user_id', 'user_email', 'user_name', 'user_phone', 'user_birth', 'user_address', 'password1', 'password2') #'user_address_Detail')

    

class PasswordResetForm(forms.Form):
    user_id = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(),
        error_messages={
            'required': 'ID is required',
            'max_length': 'ID cannot exceed 50 characters'
        }
    )
    user_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(),
        error_messages={
            'required': 'Name is required',
            'max_length': 'Name cannot exceed 100 characters'
        }
    )
    user_phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(),
        validators=[
            RegexValidator(
                regex=r'^010-\d{4}-\d{4}$',
                message='Phone number must be in the format 010-1234-5678'
            )
        ],
        error_messages={
            'required': 'Phone number is required',
            'max_length': 'Phone number cannot exceed 20 characters',
            'invalid': 'Phone number must be in the format 010-1234-5678'
        }
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        error_messages={
            'required': 'Password is required',
        }
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        error_messages={
            'required': 'Password confirmation is required',
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            self.add_error('new_password2', "The two password fields didn't match.")

