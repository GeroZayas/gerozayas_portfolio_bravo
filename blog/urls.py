from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# urlpatterns = [
#     path("blog/", views.blog, name="blog.index"),
# ]

urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("<category>/", views.blog_category, name="blog_category"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
