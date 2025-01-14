from django import forms
from .models import SupportTicket

class SupportTicketForm(forms.ModelForm):
    """Form for creating support tickets."""
    class Meta:
        model = SupportTicket
        fields = ['subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your issue...'}),
        }