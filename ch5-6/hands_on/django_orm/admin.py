import csv

from django.contrib import admin
from django.http import HttpResponse

from django_orm.models import User, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 1  # 기본으로 제공하는 빈 폼의 개수


def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'

    writer = csv.writer(response)
    field_names = [field.name for field in modeladmin.model._meta.fields]
    writer.writerow(field_names)

    for obj in queryset:
        row = [getattr(obj, field) for field in field_names]
        writer.writerow(row)
    return response


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('username', 'email')
    list_filter = ('social_provider',)
    inlines = [ProfileInline]
    actions = [export_as_csv]
