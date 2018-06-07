# Register your models here.

from django.contrib import admin

from crm.models import SwipePermissionGroup, SwipePermission


class PermissionInLine(admin.TabularInline):
    model = SwipePermission.groups.through


@admin.register(SwipePermissionGroup)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', 'users')

    inlines = [
        PermissionInLine,
    ]


@admin.register(SwipePermission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name',)
