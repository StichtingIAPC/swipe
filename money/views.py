from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from rest_framework import mixins, generics

from money.models import CurrencyData, Denomination
from money.serializers import CurrencySerializer, DenominationSerializer
from tools.templatetags.tools.breadcrumbs import crumb


class CurrencyListView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    queryset = CurrencyData.objects.all()\
        .prefetch_related('denomination_set')
    serializer_class = CurrencySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CurrencyView(mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   generics.GenericAPIView):
    queryset = CurrencyData.objects.all()\
        .prefetch_related('denomination_set')
    serializer_class = CurrencySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class DenominationDelete(mixins.DestroyModelMixin,
                         generics.GenericAPIView):
    queryset = Denomination.objects.all()
    serializer_class = DenominationSerializer


@crumb(_('Currency list'), 'money_index')
class CurrencyDataList(ListView):
    model = CurrencyData
    template_name = 'money/currencydata_list.html'


@crumb(_('Currency index'))
def index(request):
    return render(request, 'money/index.html')


@crumb(_('Detail'), 'currencydata_list')
class CurrencyDataDetail(DetailView):
    model = CurrencyData
    template_name = 'money/currencydata_detail.html'


@crumb(_('Create'), 'currencydata_list')
class CurrencyDataCreate(CreateView):
    model = CurrencyData
    fields = ['iso', 'name', 'digits', 'symbol']
    success_url = reverse_lazy('currencydata_detail')
    template_name = 'money/currencydata_form.html'

    def get_success_url(self):
        return reverse_lazy('currencydata_detail', kwargs={'pk': self.object.pk})


@crumb(_('Edit'), 'currencydata_detail', ['pk'])
class CurrencyDataEdit(UpdateView):
    model = CurrencyData
    fields = ['iso', 'name', 'digits', 'symbol']
    template_name = 'money/currencydata_form.html'

    def get_success_url(self):
        return reverse_lazy('currencydata_detail', kwargs=self.kwargs)


@crumb(_('Denomination list'), 'currencydata_detail', ['pk'])
class DenominationList(LoginRequiredMixin, ListView):
    model = Denomination
    template_name = "money/denomination_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx.update({'currency': CurrencyData.objects.get(iso=self.kwargs['pk'])})
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(currency__iso=self.kwargs['pk'])


@crumb(_('Detail'), 'denomination_list', ['pk'])
class DenominationDetail(LoginRequiredMixin, DetailView):
    model = Denomination
    template_name = "money/denomination_detail.html"

    def get_object(self, queryset=None):
        return self.model.objects.get(currency__iso=self.kwargs['pk'], pk=self.kwargs['denom'])


@crumb(_('Create denomination'), 'denomination_list', ['pk'])
class DenominationCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'register.create_denomination'
    template_name = "money/denomination_form.html"

    model = Denomination
    fields = ['currency', 'amount']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx.update(self.get_initial())
        return ctx

    def get_initial(self):
        currency = CurrencyData.objects.get(iso=self.kwargs['pk'])
        return {
            'currency': currency
        }

    def get_success_url(self):
        return reverse_lazy('denomination_list', kwargs={'pk': self.object.currency.iso})