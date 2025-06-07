from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Agent, AgentContact, AgentPropertyContact
from django.core.paginator import Paginator
from shelter.models import Listening

def agent_list(request):
    agents = Agent.objects.all()
    return render(request, 'agents/agents_list.html', {'agents': agents})

def agent_detail(request, agent_id):
    agent = get_object_or_404(Agent, pk=agent_id)
    # Get all properties listed by this agent
    agent_properties = Listening.objects.filter(agent=agent)
      # Split work experience into points
    if agent.work_experience:
        work_experience_points = [point.strip() for point in agent.work_experience.split('|') if point.strip()]
    else:
        work_experience_points = []
        
    return render(request, 'agents/agent_detail.html', {
        'agent': agent, 
        'agent_properties': agent_properties,
        'work_experience_points': work_experience_points
    })

def agent_property_contact(request):
    if request.method == 'POST':
        agent_name = request.POST['agentname']
        property_title = request.POST['property_title']
        user_name = request.POST['name']
        user_email = request.POST['email']
        user_phone = request.POST['number']
        user_subject = request.POST['textarea']
        agent_id = request.POST.get('agent_id')
        property_slug = request.POST.get('property_slug')
        
        contact = AgentPropertyContact.objects.create(
            agentname=agent_name,
            property_title=property_title,
            user_name=user_name,
            user_email=user_email,
            user_phone=user_phone,
            user_subject=user_subject
        )
        
        messages.success(request, "Thank you! The agent will contact you about this property soon.")
        # Redirect back to the property detail page
        return redirect('property_detail', slug=property_slug)

def agentcontact(request):
    if request.method == 'POST':
        agent_name = request.POST['agentname']
        user_name = request.POST['name']
        user_email = request.POST['email']
        user_phone = request.POST.get('phone', '')  # Making phone optional
        user_subject = request.POST['textarea']
        agent_id = request.POST.get('agent_id')
        
        contact = AgentContact.objects.create(
            agentname=agent_name,
            user_name=user_name,
            user_email=user_email,
            user_phone=user_phone,
            user_subject=user_subject
        )
        messages.success(request, "Thank you! Your message has been sent to the agent.")

        # Redirect back to agent detail page
        return redirect('agent_detail', agent_id=agent_id)
