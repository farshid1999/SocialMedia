# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.urls import reverse
# from django.utils import timezone
# from taggit.managers import TaggableManager
#
# from SocialMedia import settings
#
#
# # Create your models here.
#
# class User(AbstractUser):
#     date_joined = models.DateTimeField(default=timezone.now)
#     date_of_birth = models.DateField(null=True, blank=True)
#     bio = models.TextField(null=True, blank=True,max_length=500)
#     photo = models.ImageField(null=True, blank=True)
#     job = models.CharField(null=True, blank=True,max_length=100)
#     phone = models.CharField(null=True, blank=True,max_length=20)
#
#     following = models.ManyToManyField('self',
#                                        through='Contact',
#                                        related_name='followers',
#                                        blank=True,
#                                        symmetrical=False
#                                        )
#
#     blocked_users = models.ManyToManyField('self',
#                                            through='BlockRelation',
#                                            related_name='blocked_users',
#                                            symmetrical=False,
#                                            blank=True,
#                                            )
#     reported_users = models.ManyToManyField('self',
#                                             symmetrical=False,
#                                             related_name='reported_users',
#                                             )
#
#     def is_blocked(self,other_user):
#         return other_user in self.blocked_users.all()
#
#     def has_blocked(self,other_user):
#         return self.blocked_users.filter(id = other_user.id).exists()
#
#     def get_absolute_url(self):
#         return reverse('account:user_detail', kwargs=[self.username])
#
#
# class Report(models.Model):
#     reporter = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#     reported=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#     reason=models.TextField(null=True, blank=True)
#     created_at=models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.reporter} reported {self.reported}'
#
#
# class BlockRelation(models.Model):
#     blocker = models.ForeignKey('User',on_delete=models.CASCADE,related_name='blocker_users')
#     blocked = models.ForeignKey('User',on_delete=models.CASCADE,related_name='blocked_users')
#     blocked_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.blocker} blocks {self.blocked}'
#
#
# class Contact(models.Model):
#     user_from = models.ForeignKey('User',on_delete=models.CASCADE,related_name='rel_from_set')
#     user_to = models.ForeignKey('User',on_delete=models.CASCADE,related_name='rel_to_set')
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         indexes = [models.Index(fields=['created_at'])]
#         ordering = ['-created_at']
#
#     def __str__(self):
#         return f"{self.user_from} follows {self.user_to}"