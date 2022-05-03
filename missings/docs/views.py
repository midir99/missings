from django.views.generic import TemplateView


class SwaggerUIView(TemplateView):
    template_name = "docs/swagger_ui.html"
