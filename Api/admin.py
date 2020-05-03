from django.contrib import admin
from .models import User, Link, Click, Report, Token


def ban_links(modeladmin, request, queryset):
    short_description = 'ban selected links'
    queryset.update(banned=True)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Report._meta.fields]
    list_filter = ['short_url__url_id']


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Link._meta.fields]
    list_filter = ['dateTime', 'expired', 'banned', 'user__email', 'has_password']
    actions = [ban_links]
    search_fields = ['url_id', 'long_url', 'user__email']


@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Click._meta.fields]
    list_filter = ['dateTime', 'short_url__url_id']
    search_fields = ['os', 'browser', 'country', 'device', 'short_url__url_id']



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [f.name for f in User._meta.fields]
    list_filter = ['signup_at', 'last_login_at', 'verified']
    search_fields = ['email']


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Token._meta.fields]
    search_fields = ['user__email']