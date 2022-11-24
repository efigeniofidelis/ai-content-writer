from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column,Field


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
                    required = True,
                    label='first name',
                    widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'first name'})
                    )
    last_name = forms.CharField(
                    required = False,
                    label='last name',
                    widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'last name'})
                    )
    addressLine1 = forms.CharField(
                    required = True,
                    label='address line 1',
                    widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter address line 1'})
                    )

    addressLine2 =forms.CharField(
                    required = True,
                    label='address line 2',
                    widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter address line 2'})
                    )
    city = forms.CharField(
                    required = True,
                    label='city',
                    widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter city name'})
                    )
    province = forms.CharField(
                    required = True,
                    label='province',
                    widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'province'})
                    )


    country = forms.CharField(
                    required = True,
                    label='address line 1',
                    widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'postal code'})
                    )

    postalCode = forms.CharField(
                    required = True,
                    label='address line 1',
                    widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'postal code'})
                    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column(Field('first_name',value = self.user.first_name), css_class='form-group col-md-6'),Column(Field('last_name', value=self.user.last_name),css_class='form-group col-md-6')),
            Row(Column('addressLine1', css_class='form-group col-md-6'),Column('addressLine2', css_class='form-group col-md-6')),
            Row(Column('city', css_class='form-group col-md-6'),Column('province', css_class='form-group col-md-6')),
            Row(Column('country', css_class='form-group col-md-6'),Column('postalCode', css_class='form-group col-md-6')),
            Submit('submit', 'save changes',css_class = "bt btn-primary me-2")
            )

    class Meta:
        model=Profile
        fields=['addressLine1', 'addressLine2', 'city','province','country','postalCode']
    
    def save(self, *args,**kwargs):
        user = self.instance.user
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        profile = super(ProfileForm,self).save(*args,**kwargs)
        return profile



class ProfileImageForm(forms.ModelForm):
    profileimage = forms.ImageField(
                      required=True,
                      label='Upload Image',
                      widget=forms.FileInput(attrs={'class': 'form-control'})
                      )
    class Meta:
        model = Profile
        fields = ['profileimage']