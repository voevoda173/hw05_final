from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    """Предназначен для вывода информации об авторе проекта."""

    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    """
    Предназначен для вывода информации об используемых
    в проекте технологиях.
    """

    template_name = 'about/tech.html'
