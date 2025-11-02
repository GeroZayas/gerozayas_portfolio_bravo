from django.shortcuts import render, get_object_or_404
from portfolio.models import Project
from django.views import generic

# Create your views here.
# def portfolio(request):
#     # Render app template with context
#     return render(
#         request,
#         r"C:\Users\Gero Zayas\Downloads\CODING\Django\django-alpha\portfolio\templates\portfolio\portfolio_index.html",
#     )


class PortfolioView(generic.ListView):
    model = Project
    # template_name = "main/portfolio.html"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).select_related().only('id', 'title', 'description', 'slug', 'technology', 'github_link', 'image', 'ranking')

    def project_index(request):
        projects = Project.objects.filter(is_active=True).select_related().only('id', 'title', 'description', 'slug', 'technology', 'github_link', 'image', 'ranking')
        context = {"projects": projects}
        return render(request, "portfolio/portfolio_index.html", context)

    def project_detail(request, pk):
        project = get_object_or_404(Project, pk=pk, is_active=True)
        context = {"project": project}
        return render(request, "portfolio/project_detail.html", context)
