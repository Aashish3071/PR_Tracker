from django import forms
from .models import Coverage, Client, Campaign, Publication

class CoverageForm(forms.ModelForm):
    class Meta:
        model = Coverage
        fields = ['client', 'campaign', 'date', 'publication', 'edition', 'headline', 'page', 
                  'size_sq_cm', 'type', 'position', 'is_online', 'ave']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'ave': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.publication:
            self.fields['edition'].queryset = Edition.objects.filter(publication=self.instance.publication)