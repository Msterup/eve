from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from battlefield_tracker.battlefield_timer import get_battlefield_timers


def index(request):
    context = get_battlefield_timers()
    return render(request, "index/index.html", context)

def battlefield_base(request):
    context = None
    return render(request, "battlefield_base.html", context)

def scan_logs(request):
    context = None
    return render(request, "scan_logs.html", context)