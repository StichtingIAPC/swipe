from django import forms
from django.forms import Form, BoundField
from django.utils.encoding import force_text

from money.models import Denomination
from register.models import Register


class DenominationCountBoundField(BoundField):
    def __init__(self, form, field, name):
        super(DenominationCountBoundField, self).__init__(form, field, name)
        self.currency = field.currency
        self.denomination_amount = field.denomination_amount
        if hasattr(form,"name"):
            self.register = form.name
        elif hasattr(field,"name"):
            self.register = field.name

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        if attrs == None:
            attrs = {}
        attrs["currency"] = self.currency
        attrs["denomination"] = self.denomination_amount
        attrs["register"] = self.register
        attrs["onchange"] = "update_differences()"
        return super(DenominationCountBoundField, self).as_widget(widget, attrs, only_initial)


class DenominationCountField(forms.IntegerField):
    def get_bound_field(self, form, field_name):
        return DenominationCountBoundField(form, self, field_name)


class BriefCountField(forms.DecimalField):
    def get_bound_field(self, form, field_name):
        return DenominationCountBoundField(form, self, field_name)


class RegisterCountForm(Form):
    name = ""
    def __init__(self, is_open, register=None,*args, **kwargs):
            super(RegisterCountForm, self).__init__(*args, **kwargs)
            self.name = register.name
            self.register = register

            if is_open:
                self.fields['reg_%s_active' % register.name] = forms.BooleanField(label="active", initial=True)
            else:
                print("CLOSE")

            denomination_counts = register.previous_denomination_count()
            for denom_c in denomination_counts:
                denom = denom_c.denomination
                formfield = DenominationCountField(min_value=0,label=str(denom.currency.symbol)+str(denom.amount),initial=denom_c.amount)
                formfield.currency = denom.currency
                formfield.denomination_amount = denom.amount

                self.fields['reg_%s_%s' % (register.name, denom.amount)] = formfield
            if is_open:
                self.fields['reg_%s_difference' % register.name] = forms.CharField(label="Difference", initial="EUR 0.00", disabled=True)

class OpenForm(Form):
    columns = []
    briefs = []
    def __init__(self, *args, **kwargs):
        super(OpenForm, self).__init__(*args, **kwargs)
        self.briefs = []

        registers = Register.objects.filter(is_active=True,is_cash_register=True)
        self.columns = []
        for register in registers:
            self.columns.append(RegisterCountForm(True,register = register))

        registers = Register.objects.filter(is_active=True,is_cash_register=False)
        for register in registers:
            self.fields['brief_%s' % register.name] = forms.BooleanField(label=register.name,initial=False,required=False)
            self.briefs.append(register.name)

    def extra_data(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('reg_') or name.startswith('brief_'):
                yield (self.fields[name].label, value)


class CloseForm(Form):
    columns = []
    briefs = []

    def __init__(self, *args, **kwargs):
        super(CloseForm, self).__init__(*args, **kwargs)
        registers = Register.objects.filter(is_active=True,is_cash_register=True)
        self.columns = []
        for register in registers:
            if register.is_open():
                self.columns.append(RegisterCountForm(False,register = register))

        registers = Register.objects.filter(is_active=True,is_cash_register=False)
        self.name="TOTAL"
        self.briefs = []
        for register in registers:
            if register.is_open():
                self.fields['brief_%s' % register.name] = BriefCountField(min_value=0,initial=0,label=register.name)
                self.fields['brief_%s' % register.name].currency = register.currency
                self.fields['brief_%s' % register.name].name = register.name

                self.fields['brief_%s' % register.name].denomination_amount = 0
                self.briefs.append(register.name)

