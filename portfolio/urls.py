from django.urls import path
from . import views

urlpatterns = [
    path("", views.PortfolioView.project_index, name="porfolio.index"),
    path("<int:pk>/", views.PortfolioView.project_detail, name="project_detail"),
]
