from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from eve_tools.templates.pages.tracker.battlefield_timer import get_battlefield_timers

def index(request, faction="caldari"):
    return tracker(request, faction)

def tracker(request, faction: str):
    context = get_battlefield_timers(faction)
    context["faction"] = faction.capitalize()
    return render(request, "pages/tracker/tracker.html", context)