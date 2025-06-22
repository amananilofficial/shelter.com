from django.shortcuts import render,get_object_or_404,HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Listening,Quickcontact,Newsletter,Contact
from agents.models import Agent, AgentContact
from  .locations_data import locations
from .forms import QuickContactForm
# Create your views here.

def index(request):
    homes = Listening.objects.all()[:6]
    agents = Agent.objects.all()[:4]
    
    return render(request,'shelter/index.html',{'homes':homes,'agents':agents})


def propertiesList(request):

    if 'increment' not in request.session :
        #declare empty variable 
        counter = 0 
        request.session['increment'] = 0
    
    request.session['increment'] += 6
    counter = request.session['increment']
    
    homes = Listening.objects.all()[:counter]
    return render(request,'shelter/properties_list.html',{'homes':homes})

def propertyDetail(request,slug):
    sidebar_homes = Listening.objects.all()[:3]
    home = get_object_or_404(Listening,slug=slug,available=True)
    return render(request,'shelter/property_detail.html',{'home':home,'sidebar_homes':sidebar_homes})

from django.contrib import messages
from django.shortcuts import redirect

def contact(request):
    """Handle contact form submissions"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            message = request.POST.get('message')
            
            # Validate input
            if not all([name, email, phone, message]):
                messages.error(request, 'All fields are required')
                return redirect('contact')
            
            # Save to database
            contact = Contact.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message
            )
            
            messages.success(request, 'Thank you! Your message has been sent successfully.')
            return redirect('contact')
        
        except Exception as e:
            print(f"Error processing contact form: {str(e)}")
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('contact')
    
    return render(request, 'shelter/contact.html')


def searchResult(request):
    query_list = Listening.objects.all()
    search_locations = locations
    
    if not request.GET:
        return render(request, 'shelter/search.html', {'query_list': query_list, 'search_locations': search_locations})
    
    #location
    if 'location' in request.GET:
        location = request.GET['location']
        if location:
            query_list = query_list.filter(location__iexact=location)
    # keyword
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            query_list = query_list.filter(description__icontains=keyword) 
    #bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            query_list = query_list.filter(bedrooms__lte=bedrooms)    

    #bathrooms
    if 'bathrooms' in request.GET:
        bathrooms = request.GET['bathrooms']
        if bathrooms:
            query_list = query_list.filter(bathrooms__lte=bathrooms) 

    #price    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            strprice = str(price)
            # Convert the price string directly to int without dollar sign assumption
            remove_dollar = int(strprice)
            if remove_dollar:
                query_list = query_list.filter(price__lte=remove_dollar)  

    return render(request,'shelter/search.html',{
        'query_list': query_list,
        'search_locations': search_locations,
        'values': request.GET
    })

def Services(request):
    return render(request,'shelter/services.html')

def Quick_Contact(request):
    if request.method == 'POST':
        form = QuickContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            saveform = Quickcontact.objects.create(
                name=cd['name'],
                email=cd['email'],
                phone=cd['phone']
            )
            messages.success(request, "Thank you! Your message has been received.")
            return redirect('index')
        else:
            messages.error(request, "There was an error with your submission.")
    
    return redirect('index')


def UserAgentContact(request):
    if request.method == 'POST':
        agent_name = request.POST['agentname']
        user_name = request.POST['name']
        user_email = request.POST['email']
        user_subject = request.POST['textarea']
        property_id = request.POST.get('property_id')  # Property ID
        agent_id = request.POST.get('agent_id')  # Agent ID
        
        agentcontact = AgentContact.objects.create(
            agentname=agent_name,
            user_name=user_name,
            user_email=user_email,
            user_subject=user_subject
        )
        
        from django.contrib import messages
        from django.shortcuts import redirect
        messages.success(request, "Thank you! The agent will contact you soon.")
        
        # If property_id is provided, redirect to property detail
        if property_id:
            try:
                home = Listening.objects.get(id=property_id)
                return redirect('property_detail', slug=home.slug)
            except Listening.DoesNotExist:
                return redirect('properties_list')
        # If agent_id is provided, redirect to agent detail
        elif agent_id:
            return redirect('agent_detail', agent_id=agent_id)
        # Default fallback
        else:
            return redirect('properties_list')

def newsletter_signup(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone', '')
            whatsapp = request.POST.get('whatsapp') == 'on'
            
            # Check if email already exists
            if Newsletter.objects.filter(email=email).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'You are already subscribed to our newsletter!'
                })
            
            # Create new subscriber
            Newsletter.objects.create(
                name=name,
                email=email,
                phone=phone,
                whatsapp_updates=whatsapp
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Thank you for subscribing to our newsletter!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'An error occurred. Please try again.'
            })
            
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    })

def about_view(request):
    agents = Agent.objects.all()[:4]
    from team.models import Team
    teams = Team.objects.filter(is_published=True)[:3]
    return render(request, 'shelter/about.html', {'agents': agents, 'teams': teams})

def terms_view(request):
    return render(request, 'shelter/terms.html')

def privacy_view(request):
    return render(request, 'shelter/privacy.html')

def cookies_view(request):
    return render(request, 'shelter/cookies.html')

def sale_view(request):
    return render(request, 'shelter/sale.html')

def buy_view(request):
    return render(request, 'shelter/buy.html')

def rent_view(request):
    return render(request, 'shelter/rent.html')

def property_management_view(request):
    return render(request, 'shelter/property_management.html')