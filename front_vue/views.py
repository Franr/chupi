from django.views.generic import TemplateView


class FrontEndView(TemplateView):
    template_name = "index.html"
