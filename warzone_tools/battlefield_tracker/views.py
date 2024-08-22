from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from battlefield_tracker.battlefield_timer import get_battlefield_timers

def index(request, faction="caldari"):
    return battlefield_tracker(request, faction)

def battlefield_tracker(request, faction: str):
    context = get_battlefield_timers(faction)
    context["faction"] = faction.capitalize()
    return render(request, "index/index.html", context)

def battlefield_base(request):
    context = None
    return render(request, "battlefield_base.html", context)

def scan_logs(request):
    context = None
    return render(request, "scan_logs.html", context)