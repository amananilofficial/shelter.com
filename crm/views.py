from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
from django.contrib.auth import get_user_model
import csv
import io
import pandas as pd
from .models import Customer, CustomerInteraction, CustomerUpload, CRMRole, CustomerHistory, DataTransfer
from .utils import process_customer_upload

User = get_user_model()

def has_crm_permission(user, required_role='employee'):
    """Check if user has required CRM permission"""
    try:
        crm_role = user.crm_role
        role_hierarchy = {'admin': 3, 'manager': 2, 'employee': 1}
        user_level = role_hierarchy.get(crm_role.role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        return user_level >= required_level
    except:
        return False

@login_required
def crm_dashboard(request):
    """CRM Dashboard with role-based access"""
    if not has_crm_permission(request.user):
        messages.error(request, "You don't have permission to access CRM.")
        return redirect('index')
    
    # Get statistics
    total_customers = Customer.objects.count()
    new_leads = Customer.objects.filter(status='lead').count()
    active_customers = Customer.objects.filter(status='customer').count()
    
    # Recent customers
    recent_customers = Customer.objects.order_by('-created_at')[:5]
    
    # Recent interactions
    recent_interactions = CustomerInteraction.objects.order_by('-created_at')[:5]
    
    context = {
        'total_customers': total_customers,
        'new_leads': new_leads,
        'active_customers': active_customers,
        'recent_customers': recent_customers,
        'recent_interactions': recent_interactions,
        'user_role': request.user.crm_role.role if hasattr(request.user, 'crm_role') else 'none'
    }
    
    return render(request, 'crm/admin/dashboard.html', context)

@login_required
def customer_list(request):
    """List all customers with search and filtering"""
    if not has_crm_permission(request.user):
        messages.error(request, "You don't have permission to access CRM.")
        return redirect('index')
    
    customers = Customer.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        customers = customers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    # Status filter
    status_filter = request.GET.get('status')
    if status_filter:
        customers = customers.filter(status=status_filter)
    
    # Priority filter
    priority_filter = request.GET.get('priority')
    if priority_filter:
        customers = customers.filter(priority=priority_filter)
    
    # Pagination
    paginator = Paginator(customers, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'status_choices': Customer.STATUS_CHOICES,
        'priority_choices': Customer.PRIORITY_CHOICES,
    }
    
    return render(request, 'crm/admin/customer_list.html', context)

@login_required
def upload_customers(request):
    """Upload customers from CSV/Excel file"""
    if not has_crm_permission(request.user, 'manager'):
        messages.error(request, "You don't have permission to upload customer data.")
        return redirect('crm:dashboard')
    
    if request.method == 'POST':
        if 'file' not in request.FILES:
            messages.error(request, "No file selected.")
            return redirect('crm:upload_customers')
        
        file = request.FILES['file']
        
        # Validate file type
        if not file.name.endswith(('.csv', '.xlsx', '.xls')):
            messages.error(request, "Please upload a CSV or Excel file.")
            return redirect('crm:upload_customers')
        
        # Create upload record
        upload = CustomerUpload.objects.create(
            file=file,
            original_filename=file.name,
            uploaded_by=request.user,
            status='pending'
        )
        
        # Process file in background (you can use Celery for this)
        try:
            process_customer_upload(upload.id)
            messages.success(request, "File uploaded successfully and is being processed.")
        except Exception as e:
            messages.error(request, f"Error processing file: {str(e)}")
        
        return redirect('crm:upload_customers')
    
    # Get recent uploads
    recent_uploads = CustomerUpload.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')[:10]
    
    return render(request, 'crm/admin/upload_customers.html', {'recent_uploads': recent_uploads})

@login_required
def customer_detail(request, customer_id):
    """Customer detail view with interactions"""
    if not has_crm_permission(request.user):
        messages.error(request, "You don't have permission to access CRM.")
        return redirect('index')
    
    customer = get_object_or_404(Customer, id=customer_id)
    interactions = customer.interactions.order_by('-interaction_date')[:10]  # Last 10 interactions
    recent_history = customer.history.order_by('-changed_at')[:5]  # Last 5 history entries
    
    context = {
        'customer': customer,
        'interactions': interactions,
        'recent_history': recent_history,
    }
    
    return render(request, 'crm/admin/customer_detail.html', context)

@login_required
def add_interaction(request, customer_id):
    """Add interaction for a customer"""
    if not has_crm_permission(request.user):
        return JsonResponse({'success': False, 'message': 'Permission denied'})
    
    if request.method == 'POST':
        customer = get_object_or_404(Customer, id=customer_id)
        
        interaction = CustomerInteraction.objects.create(
            customer=customer,
            interaction_type=request.POST.get('interaction_type'),
            subject=request.POST.get('subject'),
            description=request.POST.get('description'),
            created_by=request.user
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Interaction added successfully',
            'interaction': {
                'type': interaction.get_interaction_type_display(),
                'subject': interaction.subject,
                'description': interaction.description,
                'date': interaction.interaction_date.strftime('%Y-%m-%d %H:%M'),
                'created_by': interaction.created_by.username
            }
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def add_customer(request):
    """Add new customer with reason tracking"""
    if not has_crm_permission(request.user):
        messages.error(request, "You don't have permission to access CRM.")
        return redirect('index')
    
    if request.method == 'POST':
        # Extract customer data
        customer_data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'whatsapp': request.POST.get('whatsapp', ''),
            'address': request.POST.get('address', ''),
            'city': request.POST.get('city', ''),
            'status': request.POST.get('status', 'lead'),
            'priority': request.POST.get('priority', 'medium'),
            'source': request.POST.get('source', ''),
            'notes': request.POST.get('notes', ''),
            'created_by': request.user
        }
          # Check if customer already exists
        if Customer.objects.filter(email=customer_data['email']).exists():
            messages.error(request, f"Customer with email {customer_data['email']} already exists.")
            return render(request, 'crm/admin/add_customer.html', {
                'status_choices': Customer.STATUS_CHOICES,
                'priority_choices': Customer.PRIORITY_CHOICES,
                'form_data': request.POST
            })
        
        try:
            # Create customer
            customer = Customer.objects.create(**customer_data)
            
            # Create history entry
            reason = request.POST.get('add_reason', 'Customer added via CRM interface')
            CustomerHistory.objects.create(
                customer=customer,
                action='created',
                reason=reason,
                changed_by=request.user
            )
            
            messages.success(request, f"Customer {customer.full_name} added successfully.")
            return redirect('crm:customer_detail', customer_id=customer.id)
            
        except Exception as e:
            messages.error(request, f"Error adding customer: {str(e)}")
    
    context = {
        'status_choices': Customer.STATUS_CHOICES,
        'priority_choices': Customer.PRIORITY_CHOICES,
    }
    
    return render(request, 'crm/admin/add_customer.html', context)

@login_required
def edit_customer(request, customer_id):
    """Edit customer with change tracking"""
    if not has_crm_permission(request.user):
        messages.error(request, "You don't have permission to access CRM.")
        return redirect('index')
    
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        # Store original values for comparison
        original_data = {
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'email': customer.email,
            'phone': customer.phone,
            'whatsapp': customer.whatsapp,
            'address': customer.address,
            'city': customer.city,
            'status': customer.status,
            'priority': customer.priority,
            'source': customer.source,
            'notes': customer.notes,
            'assigned_to': customer.assigned_to
        }
        
        # Update customer data
        customer.first_name = request.POST.get('first_name')
        customer.last_name = request.POST.get('last_name')
        customer.email = request.POST.get('email')
        customer.phone = request.POST.get('phone')
        customer.whatsapp = request.POST.get('whatsapp', '')
        customer.address = request.POST.get('address', '')
        customer.city = request.POST.get('city', '')
        customer.status = request.POST.get('status')
        customer.priority = request.POST.get('priority')
        customer.source = request.POST.get('source', '')
        customer.notes = request.POST.get('notes', '')
        
        # Handle assigned_to
        assigned_to_id = request.POST.get('assigned_to')
        if assigned_to_id:
            try:
                assigned_user = User.objects.get(id=assigned_to_id)
                customer.assigned_to = assigned_user
            except User.DoesNotExist:
                customer.assigned_to = None
        else:
            customer.assigned_to = None
        
        try:
            customer.save()
            
            # Track changes and create history entries
            reason = request.POST.get('change_reason', 'Customer updated via CRM interface')
            changes_made = []
            
            # Compare fields and create history entries
            for field_name, old_value in original_data.items():
                new_value = getattr(customer, field_name)
                
                # Handle foreign key fields
                if field_name == 'assigned_to':
                    old_value = old_value.username if old_value else 'None'
                    new_value = new_value.username if new_value else 'None'
                
                if str(old_value) != str(new_value):
                    CustomerHistory.objects.create(
                        customer=customer,
                        action='updated',
                        field_changed=field_name,
                        old_value=str(old_value),
                        new_value=str(new_value),
                        reason=reason,
                        changed_by=request.user
                    )
                    changes_made.append(field_name)
            
            if changes_made:
                messages.success(request, f"Customer updated successfully. Changed fields: {', '.join(changes_made)}")
            else:
                messages.info(request, "No changes were made to the customer.")
            
            return redirect('crm:customer_detail', customer_id=customer.id)
            
        except Exception as e:
            messages.error(request, f"Error updating customer: {str(e)}")
    
    # Get all CRM users for assignment dropdown
    crm_users = User.objects.filter(crm_role__isnull=False)
    
    context = {
        'customer': customer,
        'status_choices': Customer.STATUS_CHOICES,
        'priority_choices': Customer.PRIORITY_CHOICES,
        'crm_users': crm_users,
    }
    
    return render(request, 'crm/admin/edit_customer.html', context)

@login_required
def customer_history(request, customer_id):
    """View customer change history"""
    if not has_crm_permission(request.user):
        messages.error(request, "You don't have permission to access CRM.")
        return redirect('index')
    
    customer = get_object_or_404(Customer, id=customer_id)
    history = customer.history.order_by('-changed_at')
    
    # Pagination
    paginator = Paginator(history, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'customer': customer,
        'page_obj': page_obj,
    }
    
    return render(request, 'crm/admin/customer_history.html', context)

@login_required
def transfer_list(request):
    """List all data transfers (managers only)"""
    if not has_crm_permission(request.user, 'manager'):
        messages.error(request, "You don't have permission to access transfers.")
        return redirect('crm:dashboard')
    
    transfers = DataTransfer.objects.all()
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        transfers = transfers.filter(status=status_filter)
    
    # Filter by target app
    app_filter = request.GET.get('target_app')
    if app_filter:
        transfers = transfers.filter(target_app=app_filter)
    
    # Pagination
    paginator = Paginator(transfers, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'app_filter': app_filter,
        'status_choices': DataTransfer.STATUS_CHOICES,
        'app_choices': DataTransfer.TARGET_APP_CHOICES,
    }
    
    return render(request, 'crm/admin/transfer_list.html', context)

@login_required
def create_transfer(request):
    """Create data transfer to other apps (managers only)"""
    if not has_crm_permission(request.user, 'manager'):
        messages.error(request, "You don't have permission to create transfers.")
        return redirect('crm:dashboard')
    
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        target_app = request.POST.get('target_app')
        target_manager_id = request.POST.get('target_manager')
        
        try:
            customer = Customer.objects.get(id=customer_id)
            target_manager = User.objects.get(id=target_manager_id)
            
            # Create transfer
            transfer = DataTransfer.objects.create(
                customer=customer,
                target_app=target_app,
                target_manager=target_manager,
                sent_by=request.user,
                transfer_reason=request.POST.get('transfer_reason'),
                customer_request=request.POST.get('customer_request', ''),
                priority=request.POST.get('priority', 'medium'),
                notes=request.POST.get('notes', '')
            )
            
            # Create history entry for customer
            CustomerHistory.objects.create(
                customer=customer,
                action='updated',
                field_changed='transfer_status',
                old_value='None',
                new_value=f'Transferred to {target_app}',
                reason=f'Customer transferred to {target_app}: {transfer.transfer_reason}',
                changed_by=request.user
            )
            
            messages.success(request, f"Customer {customer.full_name} transferred to {target_app} successfully.")
            return redirect('crm:transfer_detail', transfer_id=transfer.id)
            
        except Exception as e:
            messages.error(request, f"Error creating transfer: {str(e)}")
    
    # Get available customers and managers
    customers = Customer.objects.all().order_by('first_name', 'last_name')
    
    # Get managers from different apps
    managers = []
    
    # Get agents app managers
    try:
        from agents.models import AgentRole
        agent_managers = User.objects.filter(agent_role__role__in=['admin', 'manager'])
        for user in agent_managers:
            managers.append({
                'id': user.id,
                'name': f"{user.get_full_name() or user.username} (Agents)",
                'app': 'agents'
            })
    except ImportError:
        pass
    
    # Get team app managers
    try:
        from team.models import TeamRole
        team_managers = User.objects.filter(team_role__role__in=['admin', 'manager'])
        for user in team_managers:
            managers.append({
                'id': user.id,
                'name': f"{user.get_full_name() or user.username} (Team)",
                'app': 'team'
            })
    except ImportError:
        pass
    
    context = {
        'customers': customers,
        'managers': managers,
        'app_choices': DataTransfer.TARGET_APP_CHOICES,
        'priority_choices': DataTransfer.STATUS_CHOICES,
    }
    
    return render(request, 'crm/admin/create_transfer.html', context)

@login_required
def transfer_detail(request, transfer_id):
    """View transfer details"""
    if not has_crm_permission(request.user, 'manager'):
        messages.error(request, "You don't have permission to view transfers.")
        return redirect('crm:dashboard')
    
    transfer = get_object_or_404(DataTransfer, id=transfer_id)
    
    context = {
        'transfer': transfer,
    }
    
    return render(request, 'crm/admin/transfer_detail.html', context)
