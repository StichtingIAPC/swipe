from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from register.forms import CloseForm, OpenForm
from register.models import RegisterMaster


class OpenFormView(View):
    form_class = OpenForm
    initial = {'key': 'value'}
    template_name = 'count.html'

    def get(self, request, *args, **kwargs):
        if RegisterMaster.sales_period_is_open():
            render(HttpResponseRedirect("ERROR"))

        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.extra_data()
            for col in form.columns:
                for field in col.fields:
                    print(field)
            # <process form cleaned data>
            return HttpResponseRedirect('/register/state/')
        return render(request, self.template_name, {'form': form})


class IsOpenStateView(View):
    template_name = 'is_open_view.html'
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{"is_open":RegisterMaster.sales_period_is_open()})


class CloseFormView(View):
    form_class = CloseForm
    initial = {'key': 'value'}
    template_name = 'count.html'

    def get(self, request, *args, **kwargs):

        if not RegisterMaster.sales_period_is_open():
            return (HttpResponse("ERROR, Register isn't open"))
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/register/state/')

        return render(request, self.template_name, {'form': form})