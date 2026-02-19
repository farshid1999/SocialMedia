from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

from .forms import LoginForm
from .views import *

app_name = 'social'
urlpatterns = [
    # path('', views.index, name="index"),
    path('', views.profile, name='profile'),

    path('register/',register, name='register'),

    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
    ), name='login'),

    path('logout/',logout, name='logout'),

    path('password-change/', auth_views.PasswordChangeView.as_view(
        success_url=reverse_lazy('social:password_change_done'),
        template_name='registration/password_change_form.html'
    ), name='password_change'),

    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'
    ), name='password_change_done'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        html_email_template_name='registration/password_reset_email.html',
        success_url=reverse_lazy('social:password_reset_done')
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url=reverse_lazy('social:password_reset_complete')
    ), name='password_reset_confirm'),

    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),



    path('user/edit', views.edit_user, name="edit_account"),
    path('ticket', views.ticket, name="ticket"),
    path('posts/', views.post_list, name="post_list"),
    path('posts/<slug:tag_slug>/', views.post_list, name="post_list_by_tag"),
    path('posts/create_post', views.create_post, name="create_post"),

    path('posts/detail/<int:pk>', views.post_detail, name="post_detail"),
    path('like_post/', views.like_post, name="like_post"),
    path('save_post/', views.save_post, name="save_post"),
    path('users/', views.user_list, name="user_list"),
    path('users/<username>', views.user_detail, name="user_detail"),
    path('follow/', views.user_follow, name="user_follow"),
    path('tickets/', views.find_tickets, name='find_tickets'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),  # for logged-in users
    path('followers/<str:username>/', views.followers_view, name='user_followers'),
    path('following/<str:username>/', views.following_view, name='user_following'),
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('block/<str:username>/', views.block_user, name='block_user'),
    path('unblock/<str:username>/', views.unblock_user, name='unblock_user'),
    path('report/<str:username>/', views.report_user, name='report_user'),
    path('toggle-block/', views.toggle_block_user, name='toggle_block_user'),
    path('report-user/', views.report_user, name='report_user'),

]
