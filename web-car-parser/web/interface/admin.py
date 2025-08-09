from django.contrib import admin

from .models import User, Filter


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    fields = ['t_id', 'token', 'is_superuser']
    search_fields = ['t_id']
    search_help_text = 'Telegram ID'


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    fields = ['user', 'name', 'link', 'status']
    search_fields = ['name', 'user__t_id', 'link']
    search_help_text = 'Name'
