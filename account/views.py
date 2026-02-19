# from django.contrib.auth import authenticate, login, logout
# from django.core.mail import send_mail
# from django.http import HttpResponse
# from django.shortcuts import render, redirect
#
# from account.forms import RegisterForm, UserEditForm, LoginForm, TicketForm
# from account.models import User
# # from account.utils import send_email
# # from social import settings
#
#
# def register(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#
#             if User.objects.filter(email=email).exists():
#                 return HttpResponse("Email already registered")
#             if User.objects.filter(username=username).exists():
#                 return HttpResponse("Username is already taken")
#
#             user = User.objects.create_user(username=username, email=email, password=password)
#             user.is_active = False
#             user.save()
#             # TODO: send email activation
#             return redirect('account:login')
#     else:
#         form = RegisterForm()
#     return render(request, 'forms/register.html', {'form': form})
#
#
# def edit_user(request):
#     if request.method == "POST":
#         user_form = UserEditForm(request.POST, instance=request.user, files=request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return redirect('account:profile')
#     else:
#         user_form = UserEditForm(instance=request.user)
#     return render(request, 'forms/edit_user.html', {'form': user_form})
#
#
# def profile(request):
#     user = request.user
#     user = User.objects.prefetch_related('followers','following').get(id=request.user.id)
#     saved_posts = user.saved_posts.all()
#     context = {
#         'saved_posts': saved_posts,
#         'user': user,
#     }
#     return render(request, 'account/profile.html', context)
#
#
# def user_login(request):
#     if request.user.is_authenticated:
#         return redirect('post_list_page')  # اگر صفحه‌ای با این نام داری
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('account:profile')
#                 else:
#                     return HttpResponse('Your account is not activated')
#             else:
#                 return HttpResponse('Invalid username or password')
#         else:
#             return HttpResponse('Invalid form data')
#     else:
#         form = LoginForm()
#     return render(request, 'forms/login.html', {'form': form})
#
#
# def user_logout(request):
#     if request.user.is_authenticated:
#         logout(request)
#     return redirect('profile')
#
