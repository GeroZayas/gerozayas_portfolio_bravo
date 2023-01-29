from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.IndexView.as_view(), name="home.home"),
    path("about", views.about, name="home.about"),
    path("contact/", views.ContactView.as_view(), name="home.contact"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
