from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import HomeSearchForm, ContactForm

def index(request):
    """Handle homepage with search functionality"""
    if request.method == 'POST':
        form = HomeSearchForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            search_type = form.cleaned_data['search_type']
            # Store search parameters in session
            request.session['search_location'] = location
            request.session['search_type'] = search_type
            return redirect('searches:search_results')
    else:
        form = HomeSearchForm()
    return render(request, 'hello_world/index.html', {'form': form})

def about(request):
    """Handle about page with contact form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            message = form.cleaned_data['message']

            # Send email
            subject = f'Contact Form Submission from {first_name} {last_name}'
            email_message = f'From: {email}\nName: {first_name} {last_name}\n\nMessage:\n{message}'
            try:
                send_mail(
                    subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Thank you for your message! We will get back to you soon.')
            except Exception as e:
                messages.error(request, 'Sorry, there was an error sending your message. Please try again later.')
            return redirect('hello_world:about')
    else:
        form = ContactForm()
    return render(request, 'hello_world/about.html', {'form': form})

# Error handlers
def custom_404(request, exception):
    """Handle 404 errors"""
    return render(request, 'hello_world/404.html', status=404)

def custom_500(request):
    """Handle 500 errors"""
    return render(request, 'hello_world/500.html', status=500)