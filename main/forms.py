# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.core.validators import RegexValidator
# from .models import User

# class SignUpForm(UserCreationForm):
#     user_id = forms.CharField(
#         max_length=50, 
#         required=True, 
#         widget=forms.TextInput(), 
#         error_messages={
#             'required': 'ID is required',
#             'max_length': 'ID cannot exceed 50 characters'
#         }
#     )
#     user_email = forms.EmailField(
#         max_length=200, 
#         required=True, 
#         widget=forms.EmailInput(), 
#         error_messages={
#             'required': 'Email is required',
#             'invalid': 'Enter a valid email address',
#             'max_length': 'Email cannot exceed 200 characters'
#         }
#     )
#     user_name = forms.CharField(
#         max_length=100, 
#         required=True, 
#         widget=forms.TextInput(), 
#         error_messages={
#             'required': 'Name is required',
#             'max_length': 'Name cannot exceed 100 characters'
#         }
#     )
#     user_phone = forms.CharField(
#         max_length=20, 
#         required=True, 
#         widget=forms.TextInput(), 
#         validators=[
#             RegexValidator(
#                 regex=r'^010-\d{4}-\d{4}$',
#                 message='Phone number must be in the format 010-1234-5678'
#             )
#         ],
#         error_messages={
#             'required': 'Phone number is required',
#             'max_length': 'Phone number cannot exceed 20 characters',
#             'invalid': 'Phone number must be in the format 010-1234-5678'
#         }
#     )
#     user_birth = forms.DateField(
#         required=True, 
#         widget=forms.DateInput(attrs={'placeholder': 'yyyy-mm-dd'}), 
#         validators=[
#             RegexValidator(
#                 regex=r'^\d{4}-\d{2}-\d{2}$',
#                 message='Birth date must be in the format yyyy-mm-dd'
#             )
#         ],
#         error_messages={
#             'required': 'Birth date is required',
#             'invalid': 'Enter a valid birth date in the format yyyy-mm-dd'
#         }
#     )
#     user_address = forms.CharField(
#         max_length=255, 
#         required=True, 
#         widget=forms.TextInput(), 
#         error_messages={
#             'required': 'Address is required',
#             'max_length': 'Address cannot exceed 255 characters'
#         }
#     )

#     class Meta:
#         model = User
#         fields = ('user_id', 'user_email', 'user_name', 'user_phone', 'user_birth', 'user_address', 'password1', 'password2')


# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.core.validators import RegexValidator
# from .models import User

# class SignUpForm(UserCreationForm):
#     user_id = forms.CharField(
#         max_length=50, 
#         required=True, 
#         widget=forms.TextInput(), 
#         error_messages={
#             'required': 'ID is required',
#             'max_length': 'ID cannot exceed 50 characters'
#         }
#     )
#     user_email = forms.EmailField(
#         max_length=200, 
#         required=True, 
#         widget=forms.EmailInput(), 
#         error_messages={
#             'required': 'Email is required',
#             'invalid': 'Enter a valid email address',
#             'max_length': 'Email cannot exceed 200 characters'
#         }
#     )
#     user_name = forms.CharField(
#         max_length=100, 
#         required=True, 
#         widget=forms.TextInput(), 
#         error_messages={
#             'required': 'Name is required',
#             'max_length': 'Name cannot exceed 100 characters'
#         }
#     )
#     user_phone = forms.CharField(
#         max_length=20, 
#         required=True, 
#         widget=forms.TextInput(), 
#         validators=[
#             RegexValidator(
#                 regex=r'^010-\d{4}-\d{4}$',
#                 message='Phone number must be in the format 010-1234-5678'
#             )
#         ],
#         error_messages={
#             'required': 'Phone number is required',
#             'max_length': 'Phone number cannot exceed 20 characters',
#             'invalid': 'Phone number must be in the format 010-1234-5678'
#         }
#     )
#     user_birth = forms.DateField(
#         required=True, 
#         widget=forms.DateInput(attrs={'placeholder': 'yyyy-mm-dd'}), 
#         validators=[
#             RegexValidator(
#                 regex=r'^\d{4}-\d{2}-\d{2}$',
#                 message='Birth date must be in the format yyyy-mm-dd'
#             )
#         ],
#         error_messages={
#             'required': 'Birth date is required',
#             'invalid': 'Enter a valid birth date in the format yyyy-mm-dd'
#         }
#     )
#     user_address = forms.CharField(
#         max_length=255, 
#         required=True, 
#         widget=forms.TextInput(), 
#         error_messages={
#             'required': 'Address is required',
#             'max_length': 'Address cannot exceed 255 characters'
#         }
#     )

#     class Meta:
#         model = User
#         fields = ('user_id', 'user_email', 'user_name', 'user_phone', 'user_birth', 'user_address', 'password1', 'password2')

# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Notice_board  # Assuming you are using the Notice_board model for posts
#         fields = ['notice_title', 'notice_ield']
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import User, Notice_board

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

    class Meta:
        model = User
        fields = ('user_id', 'user_email', 'user_name', 'user_phone', 'user_birth', 'user_address', 'password1', 'password2')

class PostForm(forms.ModelForm):
    class Meta:
        model = Notice_board
        fields = ['notice_title', 'notice_ield']
