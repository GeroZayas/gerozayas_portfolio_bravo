from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.PortfolioView.project_index, name="porfolio.index"),
    path("<int:pk>/", views.PortfolioView.project_detail, name="project_detail"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
