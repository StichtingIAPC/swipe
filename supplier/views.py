from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from supplier.models import Supplier
from tools.templatetags.tools.breadcrumbs import crumb


@crumb(_('Supplier List'))
class SupplierList(LoginRequiredMixin, ListView):
    model = Supplier


@crumb(_('Detail'), 'supplier_list')
class SupplierDetail(LoginRequiredMixin, DetailView):
    model = Supplier


@crumb(_('Create supplier'), 'supplier_list', [])
class SupplierCreate(PermissionRequiredMixin, CreateView):
    model = Supplier
    permission_required = 'supplier.add_supplier'
    fields = ['name', 'search_url', 'notes', 'is_used', 'is_backup']
    success_url = reverse_lazy('supplier_list')


@crumb(_('Edit'), 'supplier_detail', ['pk'])
class SupplierEdit(PermissionRequiredMixin, UpdateView):
    model = Supplier
    permission_required = 'supplier.change_supplier'
    fields = ['name', 'search_url', 'notes', 'is_used', 'is_backup']
    success_url = reverse_lazy('supplier_list')


@crumb(_('Delete'), 'supplier_detail', ['pk'])
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
