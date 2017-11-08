from crm.models import Customer


class CustomerSerializer():

    CUSTOMER_TYPES = ("P", "O", "CO")
    CUSTOMER_TYPES_MEANING = {"P": "Person", "O": "Organisation", "CO": "ContactOrganisation"}

    def serialize(self, customer: Customer):
        # TODO: Check if this method of getting a name is correct
        # TODO: Perhaps split up this method by making use of inner classes for serialization (more modular)
        # is the customer a person?
        if hasattr(self, 'person'):
            name = self.person.name
            email = self.person.email
            type = "P"
        # is the customer an organisation?
        elif hasattr(self, 'organisation'):
            name = self.organisation.name
            email = self.organisation.email
            type = "O"
        # is the customer a contactorganisation?
        elif hasattr(self, 'contactorganisation'):
            name =  "{} - {}".format(self.contactorganisation.organisation.name, self.contactorganisation.contact.name)
            # here we grab 2 emails, but should we do that?
            email ="{} - {}".format(self.contactorganisation.organisation.email, self.contactorganisation.contact.email)
            type = "CO"


