import re
from . import models
from django import forms

'''

    @version: v1.0

    @author: Cesar Armando Perez Fernandez

    Revisions:
        Revision 1.0 2015/10/10 1:38 PM

'''


def clean_name(name, name_type):
    for character in name:
        if character.isdigit() or not character.isalpha():
            raise forms.ValidationError('Invalid ' + name_type + '.')


class Registration(forms.ModelForm):
    # class Meta {content}
    class Meta:
        model = models.User
        fields = ['first_name', 'middle_initial', 'last_name', 'email', 'phone_number', 'password', ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_initial': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 12}),
        }

    # end Meta

    temp_password_holder = ''
    password_verification = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']

        if not re.compile(r'[0-9]{3}-[0-9]{3}-[0-9]{4}').match(phone_number):
            raise forms.ValidationError('Invalid phone number.')

        return phone_number


    def clean_middle_initial(self):
        middle_initial = self.cleaned_data['middle_initial']

        # clean_name(middle_initial, 'Middle Initial')

        return middle_initial

    # end clean_middle_initial

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        # clean_name(first_name, 'First Name')

        return first_name

    # end clean_first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        # clean_name(last_name, 'Last Name')

        return last_name

    # end clean_last_name

    def clean_password(self):
        password = self.cleaned_data['password']

        if len(password) < 6:
            raise forms.ValidationError('Password should be greater than 6 characters.')

        self.temp_password_holder = password

        return password

    # end clean_password

    def clean_password_verification(self):
        password_verification = self.cleaned_data['password_verification']

        if password_verification != self.temp_password_holder:
            raise forms.ValidationError('Password and Password verification should contain the same value.')

        return password_verification

        # end clean_password_verification

        # end Registration

    def set_role(self, role):
        self.instance.role = role


class Login(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))
