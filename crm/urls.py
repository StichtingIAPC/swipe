"""
CRM URL Configuration
"""

from django.conf.urls import url

from crm.views import *
from crm.profile_views import *

urlpatterns = [
    url(r'^$', index, name='crm_index'),

    # Swipe user profile URLs
    url(r'^profile$', PersonProfile.as_view(), name='user_profile'),
    url(r'^profile/(?P<pk>[0-9]+)$', PersonProfile.as_view(), name='user_profile'),
    url(r'^profile/edit$', PersonProfileEdit.as_view(), name='user_profile_edit'),
    url(r'^profile/(?P<pk>[0-9]+)/edit$', PersonProfileEdit.as_view(), name='user_profile_edit'),

    # User management URLs
    url(r'^users/link/(?P<uid>[0-9]+)$', UserProfileLink.as_view(), name='user_profile_link'),
    url(r'^users/link/apply/(?P<pk>[0-9]+)/(?P<pid>-?[0-9]+)$', UserProfileLinkApply.as_view(), name='user_profile_link_apply'),
    url(r'^users/management', UserManagement.as_view(), name='user_management'),

    # Customer URLs
    url(r'^customers$', CustomerList.as_view(), name='customer_list'),
    url(r'^customers/(?P<pk>[0-9]+)$', CustomerDetail.as_view(), name='customer_detail'),
    url(r'^customers/add_person$', PersonCreate.as_view(), name='customer_add_person'),
    url(r'^customers/add_organisation$', OrganisationCreate.as_view(), name='customer_add_organisation'),
    url(r'^customers/(?P<pk>[0-9]+)/delete$', CustomerDelete.as_view(), name='customer_delete'),
    url(r'^customers/(?P<pk>[0-9]+)/edit_person$', PersonEdit.as_view(), name='customer_edit_person'),
    url(r'^customers/(?P<pk>[0-9]+)/edit_organisation$', OrganisationEdit.as_view(), name='customer_edit_organisation'),

    url(r'^save_typefields/(?P<object_type>person|organisation)/(?P<pk>[0-9]+)$', TypeFieldSave.as_view(), name='save_type_fields'),

    # PersonType URLs
    url(r'^persontypes$', PersonTypeList.as_view(), name='persontype_list'),
    url(r'^persontypes/(?P<pk>[0-9]+)$', PersonTypeDetail.as_view(), name='persontype_detail'),
    url(r'^persontypes/add$', PersonTypeCreate.as_view(), name='persontype_add'),
    url(r'^persontypes/(?P<pk>[0-9]+)/delete$', PersonTypeDelete.as_view(), name='persontype_delete'),
    url(r'^persontypes/(?P<pk>[0-9]+)/edit$', PersonTypeEdit.as_view(), name='persontype_edit'),

    # OrganisationType URLs
    url(r'^organisationtypes$', OrganisationTypeList.as_view(), name='organisationtype_list'),
    url(r'^organisationtypes/(?P<pk>[0-9]+)$', OrganisationTypeDetail.as_view(), name='organisationtype_detail'),
    url(r'^organisationtypes/add$', OrganisationTypeCreate.as_view(), name='organisationtype_add'),
    url(r'^organisationtypes/(?P<pk>[0-9]+)/delete$', OrganisationTypeDelete.as_view(), name='organisationtype_delete'),
    url(r'^organisationtypes/(?P<pk>[0-9]+)/edit$', OrganisationTypeEdit.as_view(), name='organisationtype_edit'),

    # ContactOrganisationType URLs
    url(r'^contactorganisation/add$', ContactOrganisationCreate.as_view(), name='customer_add_contactorganisation'),
    url(r'^contactorganisation/(?P<pk>[0-9]+)/edit$', ContactOrganisationEdit.as_view(), name='contactorganisation_edit'),

    # PersonTypeField URLs
    url(r'^persontypefields$', PersonTypeFieldList.as_view(), name='persontypefield_list'),
    url(r'^persontypefields/(?P<pk>[0-9]+)$', PersonTypeFieldDetail.as_view(), name='persontypefield_detail'),
    url(r'^persontypefields/add$', PersonTypeFieldCreate.as_view(), name='persontypefield_add'),
    url(r'^persontypefields/(?P<pk>[0-9]+)/delete$', PersonTypeFieldDelete.as_view(), name='persontypefield_delete'),
    url(r'^persontypefields/(?P<pk>[0-9]+)/edit$', PersonTypeFieldEdit.as_view(), name='persontypefield_edit'),

    # OrganisationTypeField URLs
    url(r'^organisationtypefields$', OrganisationTypeFieldList.as_view(), name='organisationtypefield_list'),
    url(r'^organisationtypefields/(?P<pk>[0-9]+)$', OrganisationTypeFieldDetail.as_view(), name='organisationtypefield_detail'),
    url(r'^organisationtypefields/add$', OrganisationTypeFieldCreate.as_view(), name='organisationtypefield_add'),
    url(r'^organisationtypefields/(?P<pk>[0-9]+)/delete$', OrganisationTypeFieldDelete.as_view(), name='organisationtypefield_delete'),
    url(r'^organisationtypefields/(?P<pk>[0-9]+)/edit$', OrganisationTypeFieldEdit.as_view(), name='organisationtypefield_edit'),
]
