from django import forms
from accounts.models import RoomListing
from datetime import date
class AdvancedSearchForm(forms.Form):
    """Form for advanced search filters"""
    # Location and Basic Info
    location = forms.CharField(
        required=False,
        label="Location",
        widget=forms.TextInput(attrs={'placeholder': 'Enter city, town, or postcode'})
    )

    # Rent and Bills
    min_rent = forms.DecimalField(
        required=False,
        label='Minimum Rent (£)',
        widget=forms.NumberInput(attrs={'placeholder': 'Min'})
    )
    max_rent = forms.DecimalField(
        required=False,
        label='Maximum Rent (£)',
        widget=forms.NumberInput(attrs={'placeholder': 'Max'})
    )

    # Room Size
    room_size = forms.ChoiceField(
        choices=[
            ('any', 'Any room size'),
            ('Single', 'Single Room'),
            ('Double', 'Double Room'),
            ('Ensuite', 'Ensuite Room'),
            ('Studio', 'Studio')
        ],
        required=False,
        label="Room Size"
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
        widget=forms.CheckboxSelectMultiple,
        label="Property Type"
    )

    # Search Type
    search_type = forms.ChoiceField(
        choices=[
            ('rooms_match', 'Rooms Match'),
            ('tenant_match', 'Tenant Match'),
            ('coliving_match', 'CoLiving Match')
        ],
        required=False,
        widget=forms.RadioSelect,
        label="Search Type"
    )

    # Keywords
    keywords = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by keywords...'})
    )

    # Move-in Date and Minimum Stay
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
        label='Minimum Stay'
    )

    def clean(self):
        """Custom validation for the form"""
        cleaned_data = super().clean()
        min_rent = cleaned_data.get('min_rent')
        max_rent = cleaned_data.get('max_rent')

        if min_rent and max_rent and min_rent > max_rent:
            raise forms.ValidationError("Minimum rent cannot be greater than maximum rent.")

        return cleaned_data

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
    
    from django import forms
from datetime import date


class SearchFilterForm(forms.Form):
    location = forms.CharField(
        max_length=100,
        required=False,
        label="Location",
        widget=forms.TextInput(attrs={'placeholder': 'e.g., Bristol'})
    )
    room_size = forms.ChoiceField(
        choices=[('any', 'Any'), ('Single', 'Single'), ('Double', 'Double')],
        required=False,
        label="Room Size",
        initial='any'
    )
    min_rent = forms.IntegerField(
        required=False,
        label="Min Rent (£)",
        widget=forms.NumberInput(attrs={'placeholder': 'e.g., 500'})
    )
    max_rent = forms.IntegerField(
        required=False,
        label="Max Rent (£)",
        widget=forms.NumberInput(attrs={'placeholder': 'e.g., 1000'})
    )
    property_type = forms.MultipleChoiceField(
        choices=[('Flat', 'Flat'), ('House', 'House'), ('Studio', 'Studio')],
        required=False,
        label="Property Type",
        widget=forms.CheckboxSelectMultiple
    )
    search_type = forms.ChoiceField(
        choices=[('', 'Any')] + RoomListing.SEARCH_TYPE,  # Match the model's attribute name
        required=False,
        label="Search Type"
    )
    keywords = forms.CharField(
        max_length=100,
        required=False,
        label="Keywords",
        widget=forms.TextInput(attrs={'placeholder': 'e.g., garden, parking'})
    )
    move_in_date = forms.DateField(
        required=False,
        label="Move-in Date",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    min_stay = forms.IntegerField(
        required=False,
        label="Min Stay (months)",
        widget=forms.NumberInput(attrs={'placeholder': 'e.g., 6'})
    )
    sort_by = forms.ChoiceField(
        choices=[
            ('', 'Relevance'),
            ('price_low_to_high', 'Price: Low to High'),
            ('price_high_to_low', 'Price: High to Low'),
            ('newest', 'Newest'),
            ('location', 'Location')
        ],
        required=False,
        label="Sort By"
    )