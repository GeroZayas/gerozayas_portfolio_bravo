from django.shortcuts import render
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
        return super().get_queryset().filter(is_active=True)

    def project_index(request):
        projects = Project.objects.all()
        context = {"projects": projects}
        return render(request, "portfolio/portfolio_index.html", context)

    def project_detail(request, pk):
        project = Project.objects.get(pk=pk)
        context = {"project": project}
        return render(request, "portfolio/project_detail.html", context)
