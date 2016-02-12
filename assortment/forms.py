from django import forms

from assortment.models import Label, LabelType, UnitType


class LabelCreateForm(forms.Form):
    class Meta:
        model = Label
        fields = ['value', 'label_type']
        widgets = {
            'value': forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
        }


class LabelTypeForm(forms.Form):
    class Meta:
        model = LabelType
        fields = ['name_long']
        # after creation of a label type, only the long name can be changed, to prevent the unintended relabeling of
        # many articles at once.

        widgets = {
            'name_long': forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
        }


class LabelTypeCreateForm(forms.Form):
    class Meta:
        model = LabelType
        fields = ['name_short', 'name_long', 'unit_type']
        widgets = {
            'name_short': forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
            'name_long': forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
        }


class UnitTypeCreateForm(forms.Form):
    class Meta:
        model = UnitType
        fields = ['type_long', 'type_short', 'counting_type', 'incremental_type']
        widgets = {
            'type_long': forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
            'name_long': forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
        }
