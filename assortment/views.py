from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, CreateView

from assortment.models import LabelType, Label


class LabelTypeList(LoginRequiredMixin, ListView):
    model = LabelType


class LabelList(LoginRequiredMixin, ListView):
    model = Label


class LabelTypeCreate(LoginRequiredMixin, CreateView):
    model = LabelType


class LabelCreate(LoginRequiredMixin, CreateView):
    model = Label
