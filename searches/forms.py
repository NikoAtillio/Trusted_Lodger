from django import forms
from accounts.models import RoomListing

class AdvancedSearchForm(forms.Form):
    """Form for advanced search filters"""
    # Location and Basic Info
    location = forms.CharField(required=False)

    # Rent and Bills
    min_rent = forms.DecimalField(required=False, label='Minimum Rent')
    max_rent = forms.DecimalField(required=False, label='Maximum Rent')
    rent_period = forms.ChoiceField(
        choices=[('monthly', 'Monthly')],  # Simplified to match RoomListing model
        required=False
    )
    bills_included = forms.BooleanField(required=False, label='Bills included in the rent')

    # Move in dates and Length of stay
    move_in_date = forms.DateField(
        required=False,
        label='Available From',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    min_stay = forms.ChoiceField(
        choices=[
            ('', 'Any'),
            ('1', '1 month'),
            ('3', '3 months'),
            ('6', '6 months'),
            ('12', '12 months')
        ],
        required=False,
        label='Minimum stay'
    )

    # Room Type
    room_size = forms.ChoiceField(
        choices=[
            ('any', 'Any room size'),
            ('Single', 'Single Room'),
            ('Double', 'Double Room'),
            ('Ensuite', 'Ensuite Room'),
            ('Studio', 'Studio')
        ],
        required=False
    )

    # Property Type
    property_type = forms.MultipleChoiceField(
        choices=[
            ('Single', 'Single Room'),
            ('Double', 'Double Room'),
            ('Ensuite', 'Ensuite Room'),
            ('Studio', 'Studio')
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    # Keywords
    keywords = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by keywords...'})
    )

    def clean(self):
        cleaned_data = super().clean()
        min_rent = cleaned_data.get('min_rent')
        max_rent = cleaned_data.get('max_rent')

        if min_rent and max_rent and min_rent > max_rent:
            raise forms.ValidationError(
                "Minimum rent cannot be greater than maximum rent."
            )

        return cleaned_data