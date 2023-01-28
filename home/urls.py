from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="home.home"),
    path("about", views.about, name="home.about"),
    path("contact/", views.ContactView.as_view(), name="home.contact"),
]
