from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import csv
import json
from .models import Team, TeamContactMessage, TeamRole

User = get_user_model()

def team(request):
    teams = Team.objects.order_by('-created_at').filter(is_published=True)
    context = {
        'teams': teams
    }
    return render(request, 'team/team.html', context)

def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    work_experience = team.work_experience_as_list()
    
    context = {
        'team': team,
        'work_experience': work_experience
    }
    return render(request, 'team/team_detail.html', context)

def team_contact(request, team_id):
    if request.method == 'POST':
        team = get_object_or_404(Team, pk=team_id)
        
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        
        # Validate inputs
        if not all([name, email, phone, message]):
            # Return to team detail page with error message
            messages.error(request, 'All fields are required.')
            return redirect('team:team_detail', team_id=team_id)
        
        # Create contact message
        contact = TeamContactMessage(
            team=team,
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        contact.save()
        
        # Add success message and redirect to team detail page
        messages.success(request, 'Your message has been sent successfully. We\'ll get back to you soon.')
        return redirect('team:team_detail', team_id=team_id)
    
    # If not POST, redirect to team detail page
    return redirect('team:team_detail', team_id=team_id)

@login_required
def check_user_role(request):
    """API endpoint to check user's role in team app"""
    try:
        team_role = TeamRole.objects.get(user=request.user)
        return JsonResponse({
            'role': team_role.role,
            'permissions': {
                'can_manage': team_role.role in ['admin', 'manager'],
                'can_export': team_role.role in ['admin', 'manager'],
                'can_import': team_role.role in ['admin', 'manager'],
                'can_sync': team_role.role in ['admin', 'manager']
            }
        })
    except TeamRole.DoesNotExist:
        return JsonResponse({
            'role': 'none',
            'permissions': {
                'can_manage': False,
                'can_export': False,
                'can_import': False,
                'can_sync': False
            }
        })

@staff_member_required
def export_team_data(request):
    """Export team data for managers and admins"""
    try:
        user_role = TeamRole.objects.get(user=request.user)
        if user_role.role not in ['admin', 'manager']:
            return JsonResponse({'error': 'Insufficient permissions'}, status=403)
    except TeamRole.DoesNotExist:
        if not request.user.is_superuser:
            return JsonResponse({'error': 'Insufficient permissions'}, status=403)
    
    format_type = request.GET.get('format', 'csv')
    
    if format_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="team_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'Title', 'Role', 'Email', 'Phone', 'WhatsApp', 'Instagram', 'LinkedIn', 'Hire Date', 'Published'])
        
        teams = Team.objects.all()
        for team in teams:
            writer.writerow([
                team.name,
                team.title,
                team.role,
                team.email,
                team.phone,
                team.whatsapp,
                team.instagram,
                team.linkedin,
                team.hire_date,
                team.is_published
            ])
        
        return response
    
    return JsonResponse({'error': 'Invalid format'}, status=400)

@csrf_exempt
@staff_member_required
def sync_with_apps(request):
    """Sync team data with other apps"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        user_role = TeamRole.objects.get(user=request.user)
        if user_role.role not in ['admin', 'manager']:
            return JsonResponse({'error': 'Insufficient permissions'}, status=403)
    except TeamRole.DoesNotExist:
        if not request.user.is_superuser:
            return JsonResponse({'error': 'Insufficient permissions'}, status=403)
    
    try:
        data = json.loads(request.body)
        direction = data.get('direction', 'to')  # 'to' or 'from'
        target_app = data.get('app', 'all')
        
        synced_count = 0
        
        if direction == 'to':
            # Sync to other apps
            teams = Team.objects.filter(role__in=['manager', 'admin'])
            for team in teams:
                team.sync_with_other_apps()
                synced_count += 1
        else:
            # Sync from other apps (reverse sync)
            # This would need to be implemented based on specific requirements
            pass
        
        return JsonResponse({
            'success': True,
            'synced_count': synced_count,
            'message': f'Successfully synced {synced_count} team members'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
