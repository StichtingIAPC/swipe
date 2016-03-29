from django.contrib import admin
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