from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from supplier.models import Supplier


class SupplierList(LoginRequiredMixin, ListView):
    model = Supplier


class SupplierDetail(LoginRequiredMixin, DetailView):
    model = Supplier


class SupplierCreate(PermissionRequiredMixin, CreateView):
    model = Supplier
    permission_required = 'supplier.add_supplier'
    fields = ['name', 'search_url', 'notes', 'is_used', 'is_backup']
    success_url = reverse_lazy('supplier_list')


class SupplierEdit(PermissionRequiredMixin, UpdateView):
    model = Supplier
    permission_required = 'supplier.change_supplier'
    fields = ['name', 'search_url', 'notes', 'is_used', 'is_backup']
    success_url = reverse_lazy('supplier_list')


class SupplierDelete(PermissionRequiredMixin, DeleteView):
    model = Supplier
    permission_required = 'supplier.delete_supplier'

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
