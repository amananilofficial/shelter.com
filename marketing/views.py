from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from shelter.models import Listening
from .models import MarketingRole, PropertyCampaign, PropertyPromotion, MarketingLead, CampaignMetrics

def has_marketing_permission(user, required_role='employee'):
    """Check if user has required Marketing permission"""
    try:
        marketing_role = user.marketing_role
        role_hierarchy = {'admin': 3, 'manager': 2, 'employee': 1}
        user_level = role_hierarchy.get(marketing_role.role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        return user_level >= required_level
    except:
        return False

@login_required
def marketing_dashboard(request):
    """Marketing Dashboard with role-based access"""
    if not has_marketing_permission(request.user):
        messages.error(request, "You don't have permission to access Marketing.")
        return redirect('index')
    
    # Get statistics
    total_properties = Listening.objects.count()
    active_campaigns = PropertyCampaign.objects.filter(status='active').count()
    active_promotions = PropertyPromotion.objects.filter(is_active=True).count()
    total_leads = MarketingLead.objects.count()
    
    # Recent campaigns
    recent_campaigns = PropertyCampaign.objects.order_by('-created_at')[:5]
    
    # Recent leads
    recent_leads = MarketingLead.objects.order_by('-created_at')[:5]
    
    context = {
        'total_properties': total_properties,
        'active_campaigns': active_campaigns,
        'active_promotions': active_promotions,
        'total_leads': total_leads,
        'recent_campaigns': recent_campaigns,
        'recent_leads': recent_leads,
        'user_role': request.user.marketing_role.role if hasattr(request.user, 'marketing_role') else 'none'
    }
    
    return render(request, 'marketing/dashboard.html', context)

@login_required
def property_list(request):
    """List all properties for marketing"""
    if not has_marketing_permission(request.user):
        messages.error(request, "You don't have permission to access Marketing.")
        return redirect('index')
    
    properties = Listening.objects.filter(available=True)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        properties = properties.filter(
            Q(title__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Status filter
    status_filter = request.GET.get('status')
    if status_filter:
        properties = properties.filter(status=status_filter)
    
    # Location filter
    location_filter = request.GET.get('location')
    if location_filter:
        properties = properties.filter(location__icontains=location_filter)
    
    # Pagination
    paginator = Paginator(properties, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'location_filter': location_filter,
        'status_choices': Listening.STATUS_CHOICES,
    }
    
    return render(request, 'marketing/property_list.html', context)

@login_required
def campaign_list(request):
    """List all marketing campaigns"""
    if not has_marketing_permission(request.user):
        messages.error(request, "You don't have permission to access Marketing.")
        return redirect('index')
    
    campaigns = PropertyCampaign.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        campaigns = campaigns.filter(
            Q(name__icontains=search_query) |
            Q(property__title__icontains=search_query)
        )
    
    # Status filter
    status_filter = request.GET.get('status')
    if status_filter:
        campaigns = campaigns.filter(status=status_filter)
    
    # Campaign type filter
    type_filter = request.GET.get('campaign_type')
    if type_filter:
        campaigns = campaigns.filter(campaign_type=type_filter)
    
    # Pagination
    paginator = Paginator(campaigns, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'status_choices': PropertyCampaign.CAMPAIGN_STATUS,
        'type_choices': PropertyCampaign.CAMPAIGN_TYPES,
    }
    
    return render(request, 'marketing/campaign_list.html', context)

@login_required
def create_campaign(request):
    """Create new marketing campaign"""
    if not has_marketing_permission(request.user, 'manager'):
        messages.error(request, "You don't have permission to create campaigns.")
        return redirect('marketing:dashboard')
    
    if request.method == 'POST':
        try:
            property_id = request.POST.get('property')
            property_obj = get_object_or_404(Listening, id=property_id)
            
            campaign = PropertyCampaign.objects.create(
                name=request.POST.get('name'),
                description=request.POST.get('description', ''),
                property=property_obj,
                campaign_type=request.POST.get('campaign_type'),
                budget=request.POST.get('budget') if request.POST.get('budget') else None,
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                target_audience=request.POST.get('target_audience', ''),
                created_by=request.user
            )
            
            # Create metrics record
            CampaignMetrics.objects.create(campaign=campaign)
            
            messages.success(request, 'Campaign created successfully!')
            return redirect('marketing:campaign_list')
            
        except Exception as e:
            messages.error(request, f'Error creating campaign: {str(e)}')
    
    properties = Listening.objects.filter(available=True)
    context = {
        'properties': properties,
        'campaign_types': PropertyCampaign.CAMPAIGN_TYPES,
    }
    
    return render(request, 'marketing/create_campaign.html', context)

@login_required
def lead_list(request):
    """List all marketing leads"""
    if not has_marketing_permission(request.user):
        messages.error(request, "You don't have permission to access Marketing.")
        return redirect('index')
    
    leads = MarketingLead.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        leads = leads.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    # Status filter
    status_filter = request.GET.get('status')
    if status_filter:
        leads = leads.filter(status=status_filter)
    
    # Source filter
    source_filter = request.GET.get('source')
    if source_filter:
        leads = leads.filter(source=source_filter)
    
    # Pagination
    paginator = Paginator(leads, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'source_filter': source_filter,
        'status_choices': MarketingLead.LEAD_STATUS,
        'source_choices': MarketingLead.LEAD_SOURCES,
    }
    
    return render(request, 'marketing/lead_list.html', context)
