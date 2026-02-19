from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.
class User(AbstractUser):
    # date_joined = models.DateTimeField(default=timezone.now)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True, upload_to='account_images/')
    job = models.CharField(max_length=250, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    following = models.ManyToManyField('self', through='Contact', related_name='followers', symmetrical=False)

    # blocked_users: who this user has blocked
    blocked_users = models.ManyToManyField('self',
                                           through='BlockRelation', symmetrical=False, related_name='blocked_by',
                                           blank=True)

    # reported_users: who this user has reported
    reported_users = models.ManyToManyField('self', symmetrical=False, related_name='reported_by', blank=True)

    def is_blocked(self, other_user):
        return other_user in self.blocked_users.all()

    def has_blocked(self, other_user):
        return self.blocked_users.filter(id=other_user.id).exists()

    def get_absolute_url(self):
        return reverse('social:user_detail', args=[self.username])

class Report(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_made')
    reported = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_received')
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reporter} reported {self.reported}"


class BlockRelation(models.Model):
    blocker = models.ForeignKey('User', on_delete=models.CASCADE, related_name='blocker_set')
    blocked = models.ForeignKey('User', on_delete=models.CASCADE, related_name='blocked_set')
    blocked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.blocker} blocked {self.blocked}"


class Post(models.Model):
    # Relations
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post', verbose_name='نویسنده')
    description = models.TextField(verbose_name='توضیحات')
    # date related fields
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    saved_by = models.ManyToManyField(User, related_name="saved_posts", blank=True)
    total_likes = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_posted']
        indexes = [models.Index(fields=['-date_posted', '-total_likes'])]
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def __str__(self):
        # return self.author.first_name+' '+self.author.last_name
        return self.description
        # return self.author.first_name + ": " + self.description[:10] + '...'

    def get_absolute_url(self):
        # return reverse('blog:post_detail', kwargs={'id': self.id})
        # print('+++',self.id)
        return reverse('social:post_detail', args=[self.id])


class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['-created'])]
        ordering = ['-created']

    def __str__(self):
        return f"{self.user_from}  follows {self.user_to}"


class Ticket(models.Model):
    SUBJECT_CHOICES = [
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش'),
    ]

    name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default=False)
    answer = models.TextField(blank=True, null=True)  # admin's answer
    answered_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject} by {self.name}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('follow', 'Follow'),
        ('like', 'Like'),
        ('comment', 'Comment'),
    ]

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='actor_notifications')
    verb = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)

    # Generic link to the object (post, comment, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    target = GenericForeignKey('content_type', 'object_id')

    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
