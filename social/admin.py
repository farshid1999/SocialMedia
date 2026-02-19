from django.contrib import admin
from django.core.mail import send_mail

from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.views.main import IS_POPUP_VAR, TO_FIELD_VAR
from django.contrib import messages
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.utils.timezone import now
# Register your models here.

# Actions
@admin.action(description="Mark selected tickets as answered")
def mark_as_answered(self, request, queryset):
    queryset.update(answered=True, answered_at=now())


@admin.action(description='Activate selected posts')
def post_activation(modeladmin, request, queryset):
    already_active = queryset.filter(active=True)
    if already_active.exists():
        messages.warning(request, f"{already_active.count()} post(s) are already active.")
    result = queryset.update(active=True)
    modeladmin.message_user(request, f"Activated {result} post(s).")
# post_activation.short_description = "Activate selected posts"
@admin.action(description='Deactivate selected posts')
def post_deactivation(modeladmin, request, queryset):
    already_inactive = queryset.filter(active=False)
    if already_inactive.exists():
        messages.warning(request, f"{already_inactive.count()} post(s) are already inactive.")
    result =  queryset.update(active=False)
    modeladmin.message_user(request, f"Deactivated {result} post(s).")
# post_deactivation.short_description = "Deactivate selected posts"


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'answered', 'created_at')
    list_filter = ('answered', 'subject')
    search_fields = ('name', 'email', 'message')

    actions = ['mark_as_answered']

    # Inline way to answer
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')

    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'phone', 'subject', 'message', 'created_at')
        }),
        ('Answer', {
            'fields': ('answer', 'answered', 'answered_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.answer and not obj.answered:
            obj.answered = True
            obj.answered_at = now()
            # Optional: send response email here to user
        super().save_model(request, obj, form, change)
        if obj.answer and not obj.answered:
            send_mail(
                f"پاسخ به تیکت شما: {obj.subject}",
                obj.answer,
                'python.django.1404.1@gmail.com',  # from email
                [obj.email],  # to the user
                fail_silently=True
            )
            obj.answered = True
            obj.answered_at = now()



class BlockRelationInline(admin.TabularInline):
    model = BlockRelation
    fk_name = 'blocker'  # Show "who this user blocked"
    extra = 0
    verbose_name = 'Blocked User'
    verbose_name_plural = 'Blocked Users'
    readonly_fields = ['blocked', 'blocked_at']
    can_delete = True  # Allow unblocking from admin


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_superuser','phone','blocked_count')
    inlines = [BlockRelationInline]  # ✅ Add inline here
    list_filter = ('is_superuser',)
    fieldsets = (
        ('Additional Info', {'fields': ('date_of_birth', 'bio','photo','job','phone','email','password')}),
    )
    fieldsets = UserAdmin.fieldsets + (
        ('بلاک/گزارش کاربران', {
            'fields': ( 'reported_users',),
        }),
    )
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(report_count=models.Count('reported_by'))

    def report_count(self, obj):
        return obj.reported_by.count()

    report_count.short_description = 'تعداد گزارش‌ها'

    def blocked_count(self, obj):
        return obj.blocked_users.count()

    blocked_count.short_description = 'تعداد بلاک‌شده‌ها'

    filter_horizontal = ( 'reported_users',)  # Optional: adds UI for editing


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'date_posted','description','total_likes','active']
    ordering = ('-date_posted','-total_likes')
    search_fields = ['description']
    actions = [post_deactivation,post_activation,]

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     selected = request.POST.getlist(ACTION_CHECKBOX_NAME)
    #
    #     if selected:
    #         selected_queryset = self.model.objects.filter(pk__in=selected)
    #         all_active = selected_queryset.filter(active=True).count() == selected_queryset.count()
    #         all_inactive = selected_queryset.filter(active=False).count() == selected_queryset.count()
    #
    #         if all_active:
    #             actions.pop('activate_posts', None)
    #         elif all_inactive:
    #             actions.pop('deactivate_posts', None)
    #
    #     return actions


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'actor', 'verb', 'is_read', 'timestamp']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['reporter', 'reported', 'reason', 'created_at']
    search_fields = ['reporter__username', 'reported__username', 'reason']


admin.site.register(Contact)

