from django import forms
from .models import Deadline
import re


class DeadlineForm(forms.ModelForm):
    class Meta:
        model = Deadline
        fields = ['code', 'name', 'description', 'date', 'time', 'enabled']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control resize-text-area-none'}),
            'date': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'yyyy-mm-dd'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'HH:mm (military time)'}),
            'enabled': forms.RadioSelect
        }

    def clean_code(self):
        pattern = re.compile("^([0-9a-zA-Z]+)$")
        if pattern.match(self.cleaned_data['code']) is None:
            raise forms.ValidationError("Invalid code format")
        return self.cleaned_data['code']

    def clean_name(self):
        return self.cleaned_data['name']

    def clean_description(self):
        return self.cleaned_data['description']

    def clean_date(self):
        return self.cleaned_data['date']

    def clean_time(self):
        return self.cleaned_data['time']

    def clean_enabled(self):
        return self.cleaned_data['enabled']
