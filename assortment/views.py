from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView

from assortment.forms import LabelTypeCreateForm, LabelCreateForm, UnitTypeCreateForm, LabelTypeForm
from assortment.models import LabelType, Label, UnitType


# Notice that there are no update views for Label and UnitType. This is to prevent anyone from changing the properties
# of many articles at once. If you want to change the UnitType due to a misspelling, create a new one. If you want to
# change properties of the Label, you should not work on this part of Swipe.


class UnitTypeList(LoginRequiredMixin, ListView):
    model = UnitType


class UnitTypeCreate(PermissionRequiredMixin, CreateView):
    model = UnitType
    form_class = UnitTypeCreateForm

    permission_required = 'assortment.add_unittype'


class LabelTypeList(LoginRequiredMixin, ListView):
    model = LabelType


class LabelTypeCreate(PermissionRequiredMixin, CreateView):
    model = LabelType
    form_class = LabelTypeCreateForm

    permission_required = 'assortment.add_labeltype'


class LabelTypeUpdate(PermissionRequiredMixin, UpdateView):
    model = LabelType
    form_class = LabelTypeForm

    permission_required = 'assortment.update_labeltype'


class LabelList(LoginRequiredMixin, ListView):
    model = Label


class LabelCreate(PermissionRequiredMixin, CreateView):
    model = Label
    form_class = LabelCreateForm

    permission_required = 'assortment.add_label'
