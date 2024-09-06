from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from eve_tools.templates.pages.tracker.battlefield_timer import get_battlefield_timers
from django.shortcuts import render, redirect, get_object_or_404
from .models import ScheduledBattlefield, SolarSystem, BattlefieldCompletion
from .forms import BattlefieldCompletionForm
from django.contrib.auth.decorators import login_required

def index(request, faction="caldari"):
    return tracker(request, faction)

def tracker(request, faction: str):
    context = get_battlefield_timers(faction)
    context["faction"] = faction.capitalize()
    return render(request, "pages/tracker/tracker.html", context)

def battlefield_detail(request, battlefield_id):
    battlefield = get_object_or_404(ScheduledBattlefield, pk=battlefield_id)
    return render(request, 'pages/fleets/battlefield.html', {'battlefield': battlefield})

def system_detail(request, solarsystem_id):
    # Get the solar system by its solarsystem_id (e.g., its primary key or unique identifier)
    system = get_object_or_404(SolarSystem, solarsystem_id=solarsystem_id)
    
    # Pass the system to the template
    return render(request, 'pages/systems/system_detail.html', {'system': system})

@login_required
def report_battlefield(request):
    if request.method == 'POST':
        form = BattlefieldCompletionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('eve_tools:battlefield_log')  # Redirect to the log page after submission
    else:
        form = BattlefieldCompletionForm()
    
    return render(request, 'pages/tracker/report_completion.html', {'form': form})
