from django import forms
from .models import Coverage, Client, Campaign, Publication, Edition, CustomFormula, ReportTemplate

class CoverageForm(forms.ModelForm):
    class Meta:
        model = Coverage
        fields = ['client', 'campaign', 'date', 'publication', 'edition', 'headline', 'page', 
                  'size', 'type', 'position', 'is_online', 'ave', 'rate_per_sq_cm']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'ave': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-select select2'}),
            'campaign': forms.Select(attrs={'class': 'form-select select2'}),
            'publication': forms.Select(attrs={'class': 'form-select select2'}),
            'edition': forms.Select(attrs={'class': 'form-select select2'}),
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            'page': forms.TextInput(attrs={'class': 'form-control'}),
            'size': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_size'}),
            'rate_per_sq_cm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'id': 'id_rate_per_sq_cm'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'position': forms.Select(attrs={'class': 'form-select'}),
            'is_online': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize edition queryset to empty by default
        self.fields['edition'].queryset = Edition.objects.none()
        
        # If we have an instance with a publication, filter editions by that publication
        if self.instance and self.instance.pk and self.instance.publication:
            self.fields['edition'].queryset = Edition.objects.filter(publication=self.instance.publication)
        
        # If form is bound (POST data) and has publication data, filter editions
        if 'publication' in self.data:
            try:
                publication_id = int(self.data.get('publication'))
                self.fields['edition'].queryset = Edition.objects.filter(publication_id=publication_id)
            except (ValueError, TypeError):
                pass  # Invalid publication id, keep queryset empty
                
        # Filter campaigns based on selected client
        self.fields['campaign'].queryset = Campaign.objects.none()
        
        if self.instance and self.instance.pk and self.instance.client:
            self.fields['campaign'].queryset = Campaign.objects.filter(client=self.instance.client)
            
        if 'client' in self.data:
            try:
                client_id = int(self.data.get('client'))
                self.fields['campaign'].queryset = Campaign.objects.filter(client_id=client_id)
            except (ValueError, TypeError):
                pass  # Invalid client id, keep queryset empty

    def clean(self):
        cleaned_data = super().clean()
        is_online = cleaned_data.get('is_online')
        type_value = cleaned_data.get('type')
        ave = cleaned_data.get('ave')
        size = cleaned_data.get('size')
        rate_per_sq_cm = cleaned_data.get('rate_per_sq_cm')
        
        # For print coverage, calculate AVE if size and rate are provided
        if not is_online and not type_value == 'Online' and not ave and size and rate_per_sq_cm:
            cleaned_data['ave'] = size * rate_per_sq_cm
        
        # For online coverage, AVE is required
        if (is_online or type_value == 'Online') and not ave:
            self.add_error('ave', 'AVE is required for online coverage')
        
        return cleaned_data

class CustomFormulaForm(forms.ModelForm):
    class Meta:
        model = CustomFormula
        fields = ['name', 'formula', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'formula': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
    def clean_formula(self):
        formula = self.cleaned_data.get('formula')
        # Basic validation to check for potentially dangerous code
        forbidden_terms = ['import', 'exec', 'eval', 'compile', 'open', '__', 'globals', 'locals']
        for term in forbidden_terms:
            if term in formula:
                raise forms.ValidationError(f"Formula contains forbidden term: {term}")
        return formula

# Report Template Forms
class ReportTemplateForm(forms.ModelForm):
    class Meta:
        model = ReportTemplate
        fields = ['name', 'description', 'template_file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        
    def clean_template_file(self):
        template_file = self.cleaned_data.get('template_file')
        if template_file:
            # Check if it's an Excel file
            if not template_file.name.endswith(('.xlsx', '.xls')):
                raise forms.ValidationError("Only Excel files (.xlsx, .xls) are allowed.")
        return template_file

class GenerateReportForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    publication = forms.ModelChoiceField(
        queryset=Publication.objects.all(),
        required=False,
        empty_label="All Publications"
    )
    edition = forms.ModelChoiceField(
        queryset=Edition.objects.all(),
        required=False,
        empty_label="All Editions"
    )
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        required=False,
        empty_label="All Clients"
    )
    campaign = forms.ModelChoiceField(
        queryset=Campaign.objects.all(),
        required=False,
        empty_label="All Campaigns"
    )
    coverage_type = forms.ChoiceField(
        choices=[('', 'All Types'), ('Print', 'Print'), ('Online', 'Online')],
        required=False
    )