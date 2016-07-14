from . import models
from django import forms


def get_rate_choices():
    choices = [(0, 'Rejected'), (1, 'Accepted'), (2, 'Accepted with modification')]
    return choices


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Paper_PCM_Rate
        fields = ['review']
        widgets = {
            'review': forms.Textarea(attrs={'class': 'form-control'}),
        }

    CHOICES = [(0, 'Rejected'), (1, 'Accepted'), (2, 'Accepted with modification')]

    final_decision = forms.ChoiceField(choices=get_rate_choices(), widget=forms.RadioSelect())

    def set_paper(self, paper):
        self.instance.paper = paper

    def set_pcm(self, pcm):
        self.instance.pcm = pcm

    def set_decision(self, decision):
        self.instance.decision = decision

    def clean_review(self):
        return self.cleaned_data['review']


class FinalRatingForm(forms.Form):
    CHOICES = [(0, 'Rejected'), (1, 'Accepted'), (2, 'Accepted with modification')]
    final_decision = forms.ChoiceField(choices=get_rate_choices(), widget=forms.RadioSelect())
