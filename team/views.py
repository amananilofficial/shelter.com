from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Team, TeamContactMessage

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
