# from django.urls import path, reverse_lazy
# from django.contrib.auth import views as auth_views
# from account.views import *
#
#
# urlpatterns = [
#
#     path('register/', register, name='register'),
#
#     path('login/', user_login, name='login'),
#
#     path('logout/', user_logout, name='logout'),
#
#     path('password-change/', auth_views.PasswordChangeView.as_view(
#         success_url=reverse_lazy('account:password_change_done'),
#         template_name='registration/password_change_form.html'
#     ), name='password_change'),
#
#     path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
#         template_name='registration/password_change_done.html'
#     ), name='password_change_done'),
#
#     path('password-reset/', auth_views.PasswordResetView.as_view(
#         template_name='registration/password_reset_form.html',
#         email_template_name='registration/password_reset_email.html',
#         subject_template_name='registration/password_reset_subject.txt',
#         html_email_template_name='registration/password_reset_email.html',
#         success_url=reverse_lazy('account:password_reset_done')
#     ), name='password_reset'),
#
#     path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
#         template_name='registration/password_reset_done.html'
#     ), name='password_reset_done'),
#
#     path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
#         template_name='registration/password_reset_confirm.html',
#         success_url=reverse_lazy('account:password_reset_complete')
#     ), name='password_reset_confirm'),
#
#     path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
#         template_name='registration/password_reset_complete.html'
#     ), name='password_reset_complete'),
# ]
