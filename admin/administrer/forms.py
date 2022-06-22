from django import forms
from .models import *
from django.forms import ModelForm


class XYZ_DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        # kwargs["format"] = "%d-%m-%Y"
        super().__init__(**kwargs)


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"

        widgets = {
            'datePrise': XYZ_DateInput(format=["%Y-%m-%d"],),
            'dateEnr': XYZ_DateInput(format=["%Y-%m-%d"],),
            'dateE': XYZ_DateInput(format=["%Y-%m-%d"],),

            'dteNaiss_per': XYZ_DateInput(format=["%Y-%m-%d"],),
            'nom_per':forms.TextInput(attrs={'required': True}),

        }
      

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.none()

        if 'sousdirection' in self.data:
            try:
                sousdirection_id = int(self.data.get('sousdirection'))
                self.fields['service'].queryset = Service.objects.filter(
                    sousdirection_id=sousdirection_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['service'].queryset = self.instance.sousdirection.service_set.order_by('name')


    
class EntiteForm(ModelForm):
    class Meta:
        model = Entite
        fields = "__all__"




class CourrierForm(ModelForm):
    class Meta:
        model = Courrier
        fields = "__all__"
        widgets = {
            'DestRecp': forms.Select(attrs={'class': 'form-control'}),
            'num_AccRecp_cour': forms.NumberInput(attrs={'class': 'form-control'}),
            'type_cour': forms.TextInput(attrs={'class': 'form-control'}),
            'obj_cour': forms.Textarea(attrs={'class': 'form-control',"rows":3, "cols":10}),
            'num_ordre_cour': forms.NumberInput(attrs={'class': 'form-control'}),
            'type_cour': forms.Select(attrs={'class': 'form-control','type': 'select'}),
            
            'date_Emiss_cour':XYZ_DateInput(format=["%Y-%m-%d"],),
            'date_AccuseRecp_cour': XYZ_DateInput(format=["%Y-%m-%d"],),
            
        }
   