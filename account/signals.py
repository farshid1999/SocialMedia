# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
# from social.models import Post
# from django.db.models.signals import m2m_changed, post_delete, pre_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
#
# # سیگنال برای به‌روزرسانی total_likes
# @receiver(m2m_changed, sender=Post.likes.through)
# def update_total_likes(sender, instance, action, **kwargs):
#     if action in ['post_add', 'post_remove', 'post_clear']:
#         instance.total_likes = instance.likes.count()
#         instance.save()
#
#
# @receiver(m2m_changed, sender=Post.likes.through)
# def users_like_changed(sender,instance,**kwargs):
#     instance.total_likes = instance.likes.count()
#     instance.save()
#
#
# @receiver(post_delete, sender=Post)
# def post_deleted(sender, instance,  **kwargs):
#     author = instance.author
#     subject = f"Your post has been deleted."
#     message = f"Your post has been deleted, because it is violated the rule.(Id: {instance.id})"
#     send_mail(subject,message,'python.django.1404.1@gmail.com', [author.email],fail_silently=False)