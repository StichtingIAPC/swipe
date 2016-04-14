from django import forms
from django.forms import Form

from money.models import Denomination
from register.models import Register


class RegisterCountForm(Form):

    def __init__(self, is_open, register=False,*args, **kwargs):
            super(RegisterCountForm, self).__init__(*args, **kwargs)
            self.name = register.name
            if is_open:
                self.fields['reg_%s_active' % register.name] = forms.BooleanField(label="active")
            else:
                print("CLOSE")
            for denom in Denomination.objects.filter(currency=register.currency).order_by('amount'):
                self.fields['reg_%s_%s' % (register.name, denom.amount)] = forms.IntegerField(min_value=0,label=str(denom.currency.symbol)+str(denom.amount))
                print("ADD")


class OpenForm(Form):
    columns = []

    def __init__(self, *args, **kwargs):
        super(OpenForm, self).__init__(*args, **kwargs)
        registers = Register.objects.filter(is_active=True,is_cash_register=True)
        self.columns = []
        for register in registers:
            self.columns.append(RegisterCountForm(True,register = register))

        registers = Register.objects.filter(is_active=True,is_cash_register=False)
        for register in registers:
            self.fields['brief_%s' % register.name] = forms.DecimalField(min_value=0,label=register.name)

    def extra_data(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('reg_') or name.startswith('brief_'):
                yield (self.fields[name].label, value)


class CloseForm(Form):
    columns = []

    def __init__(self, *args, **kwargs):
        super(CloseForm, self).__init__(*args, **kwargs)
        registers = Register.objects.filter(is_active=True,is_cash_register=True)
        self.columns = []
        for register in registers:
            self.columns.append(RegisterCountForm(False,register = register))

        registers = Register.objects.filter(is_active=True,is_cash_register=False)
        for register in registers:
            self.fields['brief_%s' % register.name] = forms.DecimalField(min_value=0,label=register.name)
