from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from taggit.models import Tag

from .forms import *
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from .models import *


# Create your views here.
def log_out(request):
    logout(request)
    # return redirect(request.META.get('HTTP_REFERER'))
    return HttpResponse('خارج شدید')


def index(request):
    return HttpResponse('وارد شدید')

@login_required
def profile(request):
    user = request.user
    user = User.objects.prefetch_related('followers', 'following').get(id=request.user.id)
    saved_posts = user.saved_posts.all()

    conntext = {
        'saved_posts': saved_posts,

    }
    return render(request, 'social/profile.html', conntext)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            return render(request, 'registration/register_done.html', {'user': user})
    else:
        form = UserRegisterForm()
    return render(request, 'registration/user_registration.html', {'form': form})


@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user, files=request.FILES)
        print(user_form)
        if user_form.is_valid():
            user_form.save()
        return redirect('social:profile')
    else:
        user_form = UserEditForm(instance=request.user)

    context = {

        'user_form': user_form
    }
    return render(request, 'social/edit_user.html', context)


def ticket(request):
    # sent = False
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            message = f"{cd['name']}\n {cd['email']}\n {cd['phone']}\n\n {cd['message']}"
            # Ticket.objects.create(message=cd['message'], name=cd['name'], email=cd['email'],
            #                       phone=cd['phone'], subject=cd['subject'])
            send_mail(cd['subject'], message, 'python.django.1404.1@gmail.com', ['eskandary.a@gmail.com'],
                      fail_silently=False)
            # sent = True
            messages.success(request, 'ایمیل به پشتیبانی ارسال شد.')
            messages.info(request, 'نمونه اینفو.')
            messages.warning(request, 'نمونه هشدار.')
            # return redirect("social:index")
    else:
        form = TicketForm()
    context={'form':form}
    return render(request, "forms/ticket.html", context)
    # form = TicketForm(request.POST or None)
    # if request.method == "POST" and form.is_valid():
    #     cd = form.cleaned_data
    #     message = f"{cd['name']}\n {cd['email']}\n {cd['phone']}\n\n {cd['message']}"
    #
    #     # Save Ticket in database
    #     Ticket.objects.create(
    #         name=cd['name'],
    #         email=cd['email'],
    #         phone=cd['phone'],
    #         subject=cd['subject'],
    #         message=cd['message']
    #     )
    #
    #     # Send Email to Admin (optional)
    #     send_mail(
    #         cd['subject'],
    #         message,
    #         'python.django.1404.1@gmail.com',
    #         [cd['email']],
    #         fail_silently=False
    #     )
    #
    #     messages.success(request, 'تیکت شما ارسال شد.')
    #     return redirect("social:profile")  # or wherever you want
    #
    # context = {'form': form}
    # return render(request, "forms/ticket.html", context)


@login_required
def my_tickets(request):
    user_email = request.user.email
    # print("#:",request.user.email)
    tickets = Ticket.objects.filter(email=user_email)
    return render(request, 'forms/my_tickets.html', {'tickets': tickets})


def find_tickets(request):
    tickets = None

    if request.method == 'POST':
        email = request.POST.get('email')
        tickets = Ticket.objects.filter(email=email)

    return render(request, 'forms/find_tickets.html', {'tickets': tickets})


def post_list(request, tag_slug=None):
    posts = Post.objects.all()
    # posts = Post.objects.select_related('author').all()
    posts = Post.objects.select_related('author').order_by('-total_likes')
    posts = posts.exclude(author__in = request.user.blocked_users.all())
    # posts = Post.objects.exclude(author__in=request.user.blocked_users.all())

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.objects.filter(tags__in=[tag])

    page = request.GET.get('page')
    paginator = Paginator(posts, 2)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = []
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'social/list-ajax.html', {'posts': posts})
    context = {
        'posts': posts,
        'tag': tag,

    }
    return render(request, "social/list.html", context)


@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('social:index')
    else:
        form = CreatePostForm()
    return render(request, 'forms/create-post.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_post = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_post = similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags', '-date_posted')[:4]

    # print(similar_post)
    context = {
        'post': post,
        'similar_post': similar_post,

    }
    return render(request, 'social/detail.html', context)


@login_required
@require_POST
def like_post(request):
    post_id = request.POST.get('post_id')

    if post_id is not None:
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True
            if post.author != user:
                from .utils import create_notification
                create_notification(
                    recipient=post.author,
                    actor=user,
                    verb='like',
                    target=post
                )
        post_likes_count = post.likes.count()
        response_data = {'liked': liked, 'likes_count': post_likes_count, }
    else:
        response_data = {'error': 'Invalid post id!'}

    return JsonResponse(response_data)


@login_required
@require_POST
def save_post(request):
    post_id = request.POST.get('post_id')
    if post_id is not None:
        post = Post.objects.get(id=post_id)
        user = request.user
        if user in post.saved_by.all():
            post.saved_by.remove(user)
            saved = False
        else:
            post.saved_by.add(user)
            saved = True
        return JsonResponse({'saved': saved})
    return JsonResponse({'error': 'Invalid post id!'})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    users = users.exclude(id__in=request.user.blocked_users.values_list('id', flat=True))

    context = {'users': users}
    return render(request, 'user/user_list.html', context)


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    blocked = request.user.blocked_users.filter(id=user.id).exists() if request.user.is_authenticated else False
    blocked_by_you = user.blocked_users.all() if request.user == user else None
    blocked_you = user.blocked_by.all() if request.user == user else None
    is_blocked = False
    if request.user.is_authenticated:
        is_blocked = request.user.has_blocked(user)
    context = {
        'user': user,
        'blocked_by_you': blocked_by_you,
        'blocked_you': blocked_you,
        'blocked': blocked,
        'is_blocked': is_blocked,
    }
    # context = {'user': user, 'blocked': blocked}
    return render(request, 'user/user_detail.html', context)


@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    # print(request.POST)
    if user_id is not None:
        try:
            user = User.objects.get(id=user_id)
            if request.user in user.followers.all():
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
                follow = False
            else:
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                follow = True
            following_count = user.following.count()
            followers_count = user.followers.count()
            context = {
                'follow': follow,
                'following_count': following_count,
                'followers_count': followers_count,
            }
            return JsonResponse(context)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist!'})
    return JsonResponse({'error': 'Invalid user id!'})

# @require_POST
@login_required
def followers_view(request, username):
    user = get_object_or_404(User, username=username)
    # followers = user.followers.all()
    followers = user.followers.exclude(id__in=request.user.blocked_users.values_list('id', flat=True))

    return render(request, 'user/followers.html', {'followers': followers})


@login_required
def following_view(request, username):
    user = get_object_or_404(User, username=username)
    # users = users.exclude(id__in=request.user.blocked_users.values_list('id', flat=True))

    # following = user.following.all()
    following = user.following.exclude(id__in=request.user.blocked_users.values_list('id', flat=True))

    return render(request, 'user/following.html', {'following': following})


@login_required
def notifications_list(request):
    notifications = request.user.notifications.all()
    return render(request, 'notifications/list.html', {'notifications': notifications})


@login_required
def block_user(request, username):
    user_to_block = get_object_or_404(User, username=username)
    if user_to_block != request.user:
        request.user.blocked_users.add(user_to_block)
        messages.success(request, f"کاربر {user_to_block.username} مسدود شد.")
    return redirect('social:user_detail', username=username)

@login_required
def unblock_user(request, username):
    user_to_unblock = get_object_or_404(User, username=username)
    request.user.blocked_users.remove(user_to_unblock)
    messages.success(request, f"کاربر {user_to_unblock.username} از لیست مسدود خارج شد.")
    return redirect('social:user_detail', username=username)

@login_required
def report_user(request, username):
    user_to_report = get_object_or_404(User, username=username)
    if user_to_report != request.user:
        request.user.reported_users.add(user_to_report)
        messages.warning(request, f"شما کاربر {user_to_report.username} را گزارش کردید.")
    return redirect('social:user_detail', username=username)


@login_required
@require_POST
def toggle_block_user(request):

    user_id = request.POST.get("user_id")
    target = User.objects.get(id=user_id)

    if target == request.user or target.is_superuser:
        return JsonResponse({"status": "error", "message": "Invalid operation."}, status=400)

    if request.user.has_blocked(target):
        # Unblock
        BlockRelation.objects.filter(blocker=request.user, blocked=target).delete()
        action = "unblocked"
    else:
        # Block
        BlockRelation.objects.create(blocker=request.user, blocked=target)
        action = "blocked"

    return JsonResponse({"status": "ok", "action": action})

@login_required
@require_POST
def report_user(request):
    user_id = request.POST.get("user_id")
    reason = request.POST.get("reason", "").strip()

    try:
        target = User.objects.get(id=user_id)
        if target == request.user:
            return JsonResponse({"status": "error", "message": "You can't report yourself."}, status=400)

        Report.objects.create(reporter=request.user, reported=target, reason=reason)
        return JsonResponse({"status": "ok", "message": "User reported."})
    except User.DoesNotExist:
        return JsonResponse({"status": "error", "message": "User not found."}, status=404)