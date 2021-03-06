from rest_framework import serializers

from crm.models import Customer, Person, Organisation, ContactOrganisation


class CustomerSerializer(serializers.Serializer):

    CUSTOMER_TYPES = ("P", "O", "CO")
    CUSTOMER_TYPES_MEANING = {"P": "Person", "O": "Organisation", "CO": "ContactOrganisation"}

    def to_representation(self, instance):
        data = {}
        data['id'] = instance.id
        # is the customer a person?
        if hasattr(instance, 'person'):
            data['type'] = "P"
            data['person'] = PersonSerializer(instance=instance.person).data
            data['organisation'] = None
        # is the customer an organisation?
        elif hasattr(instance, 'organisation'):
            data['type'] = "O"
            data['person'] = None
            data['organisation'] = OrganisationSerializer(instance=instance.organisation).data
        # is the customer a contactorganisation?
        elif hasattr(instance, 'contactorganisation'):
            data['type'] = "CO"
            data['person'] = PersonSerializer(instance=instance.contactorganisation.contact).data
            data['organisation'] = OrganisationSerializer(instance=instance.contactorganisation.organisation).data
        return data


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = (
            'id',
            'name',
            'email',
            'address',
            'zip_code',
            'city',
            'phone',
            'memo',
            'types',
            'user',
        )


class OrganisationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organisation
        fields = (
            'id',
            'inherited_fields',
            'name',
            'email',
            'address',
            'zip_code',
            'city',
            'phone',
            'fax',
            'kvk',
            'memo',
            'parent_organisation',
            'types'
        )


# This serializer is different from the ContactOrganisationSerializer as this serializer also serializes the contact
# and the organisation instead of returning their id's
class DetailedContactOrganisationSerializer(serializers.ModelSerializer):

    contact = PersonSerializer()
    organisation = OrganisationSerializer()

    class Meta:
        model = ContactOrganisation
        fields = (
            'contact',
            'organisation'
        )


class ContactOrganisationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactOrganisation
        fields = (
            'contact',
            'organisation'
        )
