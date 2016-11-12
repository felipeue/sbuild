from django.shortcuts import render, render_to_response
from smapp.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from smapp.forms import VisitForm


# Create your views here.

def index(request):
    return render(request, 'index.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        resident = UserSM.objects.get(rut=username)
        if user:
            if user.is_active and resident.user_type == 'R':
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
            else:
                return render_to_response('login_error.html', {})
        else:
            return HttpResponseRedirect('/login/')
    else:
        return render(request, 'login.html', {})


@login_required
def dashboard(request):
    current = request.user
    resident = UserSM.objects.get(rut=current.username)
    if resident.user_type != 'R':
        return render_to_response('login_error.html', {})
    else:
        r = UserSM.objects.filter(userOrigin=current)
        records = Visit.objects.filter(resident=r).order_by('id')[:5]
        return render(request, 'index_dashboard.html', {'records': records})


@login_required
def visit_record(request):
    current = request.user
    resident = UserSM.objects.get(rut=current.username)
    if resident.user_type != 'R':
        return render_to_response('login_error.html', {})
    else:
        records = Visit.objects.filter(resident=resident).order_by('id').all()
        return render(request, 'visit_record.html', {'records': records})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_concierge(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        concierge = UserSM.objects.get(rut=username)
        if user:
            if user.is_active and concierge.user_type == 'C':
                login(request, user)
                return HttpResponseRedirect('/dashboard_concierge/')
            else:
                return render_to_response('login_error.html', {})
        else:
            return HttpResponseRedirect('/login_concierge/')
    else:
        return render(request, 'login_concierge.html', {})


@login_required
def dashboard_concierge(request):
    current = request.user
    concierge = UserSM.objects.get(rut=current.username)
    if concierge.user_type != 'C':
        return render_to_response('login_error.html', {})
    else:
        records = Visit.objects.order_by('-id')[:5]
        return render(request, 'concierge_dashboard.html', {'records': records})


@login_required
def register_visit(request):
    current = request.user
    concierge = UserSM.objects.get(rut=current.username)
    if concierge.user_type != 'C':
        return render_to_response('login_error.html', {})
    else:
        if request.method == 'POST':
            visit_form = VisitForm(data=request.POST)
            if visit_form.is_valid():
                visit = visit_form.save(commit=False)
                visit.save()
                print visit_form.errors
        else:
            visit_form = VisitForm()
        return render(request, 'register_visit.html', {'visit_form': visit_form})


@login_required
def historical_record(request):
    current = request.user
    concierge = UserSM.objects.get(rut=current.username)
    if concierge.user_type != 'C':
        return render_to_response('login_error.html', {})
    else:
        records = Visit.objects.order_by('id').all()
        return render(request, 'historical_record.html', {'records': records})
