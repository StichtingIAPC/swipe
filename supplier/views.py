from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView

from supplier.models import Supplier


class SupplierList(ListView):
    model = Supplier


class SupplierDetail(DetailView):
    model = Supplier


class SupplierCreate(CreateView):
    model = Supplier
    fields = ['name', 'search_url', 'notes', 'is_used', 'is_backup']
    success_url = reverse_lazy('supplier_list')


class SupplierEdit(UpdateView):
    model = Supplier
    fields = ['name', 'search_url', 'notes', 'is_used', 'is_backup']


class SupplierDelete(DeleteView):
    model = Supplier

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get_success_url(self):
        return reverse_lazy('supplier_detail', args=[self.object.pk])

    # Overwrite the delete method to soft-delete instead of delete the object
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        if request.path == reverse_lazy('supplier_delete', args=[self.object.pk]):
            self.object.is_deleted = True
        elif request.path == reverse_lazy('supplier_undelete', args=[self.object.pk]):
            self.object.is_deleted = False

        self.object.save()
        return HttpResponseRedirect(success_url)
