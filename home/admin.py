from django.contrib import admin

# from home.models import ContactProfile, Certificate
from home.models import ContactProfile

# Register your models here.


@admin.register(ContactProfile)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "timestamp",
        "name",
    )


# @admin.register(Certificate)
# class CertificateAdmin(admin.ModelAdmin):
#     list_display = ("id", "name")
