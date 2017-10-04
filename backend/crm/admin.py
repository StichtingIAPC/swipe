from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from crm.models import *

admin.site.register(Customer)
admin.site.register(Person)
admin.site.register(PersonType)
admin.site.register(PersonTypeField)
admin.site.register(PersonTypeFieldValue)
admin.site.register(ContactOrganisation)
admin.site.register(Organisation)
admin.site.register(OrganisationType)
admin.site.register(OrganisationTypeField)
admin.site.register(OrganisationTypeFieldValue)


# Show edit fields for the Person object on a User's admin page.
class PersonInline(admin.StackedInline):
    model = Person
    can_delete = False
    verbose_name_plural = _("customer")


class UserAdmin(BaseUserAdmin):
    inlines = (PersonInline, )

# Re-register the UserAdmin with the admin site
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
