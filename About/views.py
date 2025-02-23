from django.shortcuts import render
from .models import TeamMember  # Import the model if you created one

def about_us(request):
    team_members = TeamMember.objects.all()  # Fetch team members from the database
    context = {
        'team_members': team_members,
    }
    return render(request, 'aboutus.html', context)