from django.views.generic.base import ContextMixin
from django.utils.translation import ugettext_lazy as _


class NamedPageMixin(ContextMixin):
    page_name = ""

    def get_context_data(self, **kwargs):
        context = super(NamedPageMixin, self).get_context_data(**kwargs)
        context['page_title'] = _(self.page_name)
        return context
