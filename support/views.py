from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SupportTicket
from .forms import SupportTicketForm

@login_required
def create_ticket(request):
    """Create a new support ticket."""
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, 'Ticket created successfully!')
            return redirect('ticket_list')
    else:
        form = SupportTicketForm()
    return render(request, 'support/create_ticket.html', {'form': form})

@login_required
def ticket_list(request):
    """Display a list of support tickets for the logged-in user."""
    tickets = SupportTicket.objects.filter(user=request.user)
    return render(request, 'support/ticket_list.html', {'tickets': tickets})

def about(request):
    """Display the about page."""
    return render(request, 'support/about.html')  # Ensure this path is correct

def faq_support(request):
    """Display the FAQ support page."""
    return render(request, 'support/faq_support.html')  # Ensure this path is correct