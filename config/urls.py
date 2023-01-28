from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),  # include your app urls
    path("blog/", include("blog.urls")),
    path("portfolio/", include("portfolio.urls")),  # include your app urls
]
