import csv

from django.contrib import admin
from django.http import HttpResponse

from orm.models import CustomUser, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 1


def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=export.csv"

    writer = csv.writer(response)
    field_names = [field.name for field in modeladmin.model._meta.fields]
    writer.writerow(field_names)

    for obj in queryset:
        row = [getattr(obj, field) for field in field_names]
        writer.writerow(row)
    return response


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "date_joined")
    search_fields = ("username", )
    list_filter = ("is_staff", )
    inlines = [ProfileInline]
    actions = [export_as_csv]
