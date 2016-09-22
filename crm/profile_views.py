from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from crm.models import Person
from www.mixins import NamedPageMixin
from django.utils.translation import ugettext_lazy as _


class PersonProfile(LoginRequiredMixin, NamedPageMixin, DetailView):
    template_name = 'crm/profile/detail.html'
    page_name = "User Profile"
    model = User

    def get_object(self, queryset=None):
        """
        Get the object to show details for. If no object is given in kwargs, show the user's own profile.
        """
        if self.pk_url_kwarg not in self.kwargs.keys():
            self.kwargs[self.pk_url_kwarg] = self.request.user.id

        return super(PersonProfile, self).get_object(queryset=queryset)


class PersonProfileEdit(LoginRequiredMixin, NamedPageMixin, UpdateView):
    template_name = 'crm/profile/edit.html'
    page_name = "Edit Profile"
    model = User
    fields = ["username", "email"]

    def get_success_url(self):
        return reverse("user_profile", kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        """
        Get the object to show details for. If no object is given in kwargs, show the user's own profile.
        """
        if self.pk_url_kwarg not in self.kwargs.keys():
            self.kwargs[self.pk_url_kwarg] = self.request.user.id

        return super(PersonProfileEdit, self).get_object(queryset=queryset)


class UserProfileLink(LoginRequiredMixin, PermissionRequiredMixin, NamedPageMixin, ListView):
    template_name = 'crm/profile/link.html'
    permission_required = 'crm.link_user_to_person'
    permission_denied_message = _("You do not have access to this page.")
    page_name = "Link User to Person"
    model = Person
    paginate_by = 100

    def __init__(self):
        super().__init__()
        self.uid = -1
        self.search = ""
    
    def dispatch(self, request, *args, **kwargs):
        self.uid = kwargs.pop("uid", -1)
        return super(UserProfileLink, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.search = request.GET.get('search')
        return super(UserProfileLink, self).get(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        qs = super(UserProfileLink, self).get_queryset()

        # Filter persons on the search
        if self.search:
            qs = qs.filter(name__icontains=self.search)

        return qs

    def get_context_data(self, **kwargs):
        # Get general context
        context = super(UserProfileLink, self).get_context_data(**kwargs)

        # Add found user to context
        try:
            context['user'] = User.objects.get(pk=self.uid)
        except User.DoesNotExist:
            raise Http404("Invalid user: {}".format(self.uid))

        return context


class UserProfileLinkApply(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "crm.link_user_to_person"
    permission_denied_message = _("You do not have access to this page.")

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def get(self, request, **kwargs):
        # Get the user and person to link
        try:
            user = User.objects.get(pk=kwargs['pk'])
        except User.DoesNotExist:
            raise Http404('Invalid user')

        try:
            person = Person.objects.get(pk=kwargs['pid'])
        except Person.DoesNotExist:
            raise Http404("Invalid person")

        # Save user reference in person
        person.user = user
        person.save()

        # Go back to the user list
        return redirect('user_management')


class UserManagement(LoginRequiredMixin, NamedPageMixin, ListView):
    template_name = 'crm/profile/management.html'
    page_name = "User Management"
    model = User
