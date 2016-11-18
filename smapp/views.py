from django.shortcuts import render, render_to_response
from smapp.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from smapp.forms import VisitForm, PublicationForm
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def index(request):
    return render(request, 'index.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
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
    try:
        resident = Resident.objects.get(rut=current.username)
        if resident:
            r = Resident.objects.filter(userOrigin=current)
            publications = Publication.objects.order_by('-id')[:5]
            records = Visit.objects.filter(resident=r).order_by('-id')[:5]
            return render(request, 'index_dashboard.html', {'records': records, 'publications': publications})
        else:
            return render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def visit_record(request):
    current = request.user
    try:
        resident = Resident.objects.get(rut=current.username)
        if resident:
            records = Visit.objects.filter(resident=resident).order_by('id').all()
            return render(request, 'visit_record.html', {'records': records})
        else:
            return render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def publish(request):
    current = request.user
    try:
        resident = Resident.objects.get(rut=current.username)
        if resident:
            if request.method == 'POST':
                publication_form = PublicationForm(data=request.POST)
                if publication_form.is_valid():
                    publication = publication_form.save(commit=False)
                    publication.resident = resident
                    publication.save()
                    print publication_form.errors
                    return HttpResponseRedirect('/dashboard/')
            else:
                publication_form = PublicationForm()
            return render(request, 'publish.html', {'publication_form': publication_form})
        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def publications_wall(request):
    current = request.user
    try:
        resident = Resident.objects.get(rut=current.username)
        if resident:
            publications = Publication.objects.order_by('-id').all()
            return render(request, 'publications_wall.html', {'publications': publications})
        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_concierge(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
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
    try:
        concierge = Consierge.objects.get(rut=current.username)
        if concierge:
            records = Visit.objects.order_by('-id')[:5]
            publications = Publication.objects.order_by('-id')[:5]
            return render(request, 'concierge_dashboard.html', {'records': records , 'publications': publications})
        else:
            return render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def register_visit(request):
    current = request.user
    try:
        concierge = Consierge.objects.get(rut=current.username)
        if concierge:
            if request.method == 'POST':
                visit_form = VisitForm(data=request.POST)
                if visit_form.is_valid():
                    visit = visit_form.save(commit=False)
                    visit.save()
                    print visit_form.errors
                    return HttpResponseRedirect('/historical_record/')
            else:
                visit_form = VisitForm()
            return render(request, 'register_visit.html', {'visit_form': visit_form})
        else:
            return render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def historical_record(request):
    current = request.user
    try:
        concierge = Consierge.objects.get(rut=current.username)
        if concierge:
            records = Visit.objects.order_by('id').all()
            return render(request, 'historical_record.html', {'records': records})
        else:
            return render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})



