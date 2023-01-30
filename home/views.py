from django.shortcuts import render
from .forms import ContactForm
from django.contrib import messages
from django.views import generic

from .models import Certificate

# Create your views here.
# def home(request):
#     # Render app template with context
#     return render(request, "home/home.html")


def about(request):
    return render(request, "home/about.html")


def header(request):
    return render(request, "home/header.html")


class ContactView(generic.FormView):
    template_name = "home/contact.html"
    form_class = ContactForm
    success_url = "/"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Thank you. We will be in touch soon.")
        return super().form_valid(form)


class IndexView(generic.TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        certificates = Certificate.objects.filter(is_active=True)

        context["certificates"] = certificates
        return context


def footer(request):
    return render(request, "home/footer.html")
