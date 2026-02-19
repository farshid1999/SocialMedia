# from django import forms
# from django.contrib.auth.forms import AuthenticationForm
# from django.forms import ModelForm
# from .models import *
#
#
# class RegisterForm(forms.Form):
#     username=forms.CharField(
#         max_length=50,
#         widget=forms.TextInput(attrs={
#             "required":True
#         })
#     )
#     email=forms.CharField(
#         max_length=50,
#         widget=forms.EmailInput(attrs={
#             "required":True
#         })
#     )
#     password=forms.CharField(
#         max_length=50,
#         widget=forms.PasswordInput(attrs={
#             "required":True
#         })
#     )
#     password_again=forms.CharField(
#         max_length=50,
#         widget=forms.PasswordInput(attrs={
#             "required":True
#         })
#     )
#
#     def clean_phone(self):
#         phone=self.cleaned_data['phone']
#         if User.objects.filter(phone=phone).exists():
#             raise forms.ValidationError("Phone number already in use.")
#         return phone
#
#     def clean_email(self):
#         email=self.cleaned_data['email']
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError("Email already registered.")
#         return email
#
#     def clean_username(self):
#         username=self.cleaned_data['username']
#         if User.objects.filter(username=username).exists():
#             raise forms.ValidationError("Username already in use.")
#         return username
#
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         password_again = cleaned_data.get("password_again")
#
#         if password and password_again and password != password_again:
#             raise forms.ValidationError("Passwords don't match")
#
#         return cleaned_data
#
# class LoginForm(AuthenticationForm):
#     username=forms.CharField(
#         max_length=50,
#         widget=forms.TextInput(attrs={
#             "required":True
#         })
#     )
#     password=forms.CharField(
#         max_length=50,
#         widget=forms.PasswordInput(attrs={
#             "required":True
#         })
#     )
#
# class UserRegisterForm(forms.Form):
#     password=forms.CharField(
#         max_length=50,
#         widget=forms.PasswordInput(attrs={
#             "required":True
#         })
#     )
#     password2=forms.CharField(
#         max_length=50,
#         widget=forms.PasswordInput(attrs={
#             "required":True
#         })
#     )
#     def clean_password(self):
#         cd=self.cleaned_data
#         if cd["password"] != cd["password2"]:
#             raise forms.ValidationError("پسورد ها مطابقت ندارد")
#         return cd["password"]
#
#     class Meta:
#         model=User
#         fields=['first_name','last_name','username','email']
#
#
# class UserEditForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['date_of_birth', 'bio', 'photo', 'job']
#
#     def clean(self):
#         cleaned_data = super().clean()
#         # قفل کردن فیلدهایی که نباید تغییر کنن
#         if self.instance:
#             cleaned_data['username'] = self.instance.username
#             cleaned_data['email'] = self.instance.email
#             cleaned_data['phone'] = self.instance.phone
#         return cleaned_data
#
