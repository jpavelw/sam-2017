from django import forms
from . import models


class SubmitPaperForm(forms.ModelForm):

    file = forms.FileField(label="Select File", widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.Paper
        fields = ['title', 'list_of_authors', 'preferred_contact_method', 'format', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'list_of_authors': forms.Textarea(attrs={'class': 'form-control resize-text-area-none', 'rows': 3}),
            'preferred_contact_method': forms.Select(attrs={'class': 'form-control'}),
            'format': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_title(self):
        return self.cleaned_data['title']

    def clean_list_of_authors(self):
        return self.cleaned_data['list_of_authors']

    def clean_version_number(self):
        return self.cleaned_data['version_number']

    def clean_format(self):
        return self.cleaned_data['format']

    def clean_file(self):
        if 'file' in self.cleaned_data:
            file_name = str(self.cleaned_data['file']).lower()
            file_parts = file_name.split(".")
            if not file_parts[-1] in ['pdf', 'doc', 'docx']:
                raise forms.ValidationError("Invalid file format.")
        return self.cleaned_data['file']


class UpdatePaperForm(forms.ModelForm):

    class Meta:
        model = models.Paper
        fields = ['title', 'list_of_authors', 'preferred_contact_method', 'format']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'list_of_authors': forms.Textarea(attrs={'class': 'form-control resize-text-area-none'}),
            'preferred_contact_method': forms.Select(attrs={'class': 'form-control'}),
            'format': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_title(self):
        return self.cleaned_data['title']

    def clean_list_of_authors(self):
        return self.cleaned_data['list_of_authors']

    def clean_version_number(self):
        return self.cleaned_data['version_number']

    def clean_format(self):
        return self.cleaned_data['format']


