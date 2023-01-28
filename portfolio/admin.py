from django.contrib import admin
from portfolio.models import Project


# class ProjectAdmin(admin.ModelAdmin):
#     pass


# admin.site.register(Project, ProjectAdmin)


@admin.register(Project)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_active", "ranking")
    readonly_fields = ("slug",)
