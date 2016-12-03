from django.shortcuts import render, render_to_response
from smapp.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from smapp.forms import VisitForm, PublicationForm, EventForm, RentForm, UserForm, ResidentForm
from django.core.exceptions import ObjectDoesNotExist
from fullcalendar.util import events_to_json
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
        return render(request, 'resident/login.html', {})


@login_required
def dashboard(request):
    current = request.user
    try:
        resident = Resident.objects.get(rut=current.username)
        if resident:
            r = Resident.objects.filter(userOrigin=current)
            publications = Publication.objects.order_by('-id')[:5]
            records = Visit.objects.filter(resident=r).order_by('-id')[:5]
            reservations = Event.objects.order_by('-id')[:6]
            payments = Rent.objects.filter(resident=r).order_by('id')[:5]
            return render(request, 'resident/index_dashboard.html', {'records': records, 'publications': publications, 'reservations': reservations, 'payments': payments})
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
            return render(request, 'consierge/visit_record.html', {'records': records})
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
            return render(request, 'resident/publish.html', {'publication_form': publication_form})
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
            return render(request, 'resident/publications_wall.html', {'publications': publications})
        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def rent_pay(request):
    current = request.user
    try:
        resident = Resident.objects.get(rut=current.username)
        if resident:
            rents = Rent.objects.filter(resident=resident).order_by('-id').all()
            return render(request, 'resident/pay_list.html', {'rents': rents})
        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def calendar(request):
    current = request.user
    try:
        resident = Resident.objects.get(rut=current.username)
        if resident:
            return render(request, 'resident/calendar_locations.html', {})
        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


def all_events(request):
    events = Event.objects.all().values('title', 'start', 'end', 'all_day')
    return HttpResponse(events_to_json(events), content_type='application/json')


@login_required
def create_event(request):
    current = request.user
    try:
        resident = Resident.objects.get(rut=current.username)
        if resident:
            if request.method == 'POST':
                event_form = EventForm(data=request.POST)
                if event_form.is_valid():
                    event = event_form.save(commit=False)
                    event.all_day = 0
                    event.end = event.start
                    event.resident = resident
                    event.title = event.resident.userOrigin.first_name + ' ' + event.resident.userOrigin.last_name + '-' + event.location.name
                    s = Event.objects.filter(start__contains=event.start)
                    l = Event.objects.filter(location=event.location)
                    if s and l:
                        return render_to_response('reserv_error.html', {})
                    else:
                        event.save()
                        return HttpResponseRedirect('/calendar_locations/')
            else:
                event_form = EventForm()
            return render(request, 'resident/register_event.html', {'event_form': event_form})
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
        return render(request, 'consierge/login_concierge.html', {})


@login_required
def dashboard_concierge(request):
    current = request.user
    try:
        concierge = Consierge.objects.get(rut=current.username)
        if concierge:
            records = Visit.objects.order_by('-id')[:5]
            publications = Publication.objects.order_by('-id')[:5]
            return render(request, 'consierge/concierge_dashboard.html', {'records': records , 'publications': publications})
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
            return render(request, 'consierge/register_visit.html', {'visit_form': visit_form})
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
            return render(request, 'consierge/historical_record.html', {'records': records})
        else:
            return render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def publications_wall_consierge(request):
    current = request.user
    try:
        consierge = Consierge.objects.get(rut=current.username)
        if consierge:
            publications = Publication.objects.order_by('-id').all()
            return render(request, 'consierge/publications_wall_consierge.html', {'publications': publications})
        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def calendar_consierge(request):
    current = request.user
    try:
        consierge = Consierge.objects.get(rut=current.username)
        if consierge:
            return render(request, 'consierge/calendar_locations_consierge.html', {})
        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


def login_owner(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/dashboard_owner/')
            else:
                return render_to_response('login_error.html', {})
        else:
            return HttpResponseRedirect('/login_owner/')
    else:
        return render(request, 'owner/login_owner.html', {})


@login_required
def dashboard_owner(request):
    current = request.user
    try:
        owner = Owner.objects.get(rut=current.username)
        if owner:
            records = Visit.objects.order_by('-id')[:5]
            publications = Publication.objects.order_by('-id')[:5]
            return render(request, 'owner/owner_dashboard.html', {'records': records, 'publications': publications})
        else:
            return render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})

@login_required
def register_rent(request):
    current = request.user
    try:
        owner = Owner.objects.get(rut=current.username)
        if owner:
            if request.method == 'POST':
                rent_form = RentForm(data=request.POST)
                if rent_form.is_valid():
                    rent = rent_form.save(commit=False)
                    rent.save()
                    print rent_form.errors
                    return HttpResponseRedirect('/dashboard_owner/')
            else:
                rent_form = RentForm()
            return render(request, 'owner/register_rent.html', {'rent_form': rent_form})
        else:
            return render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def historical_record_owner(request):
    current = request.user
    try:
        owner = Owner.objects.get(rut=current.username)
        if owner:
            records = Visit.objects.order_by('id').all()
            return render(request, 'owner/historical_record_owner.html', {'records': records})
        else:
            return render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def calendar_owner(request):
    current = request.user
    try:
        owner = Owner.objects.get(rut=current.username)
        if owner:
            return render(request, 'owner/calendar_location_owner.html', {})
        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def publications_wall_owner(request):
    current = request.user
    try:
        owner = Owner.objects.get(rut=current.username)
        if owner:
            publications = Publication.objects.order_by('-id').all()
            return render(request, 'owner/publications_wall_owner.html', {'publications': publications})
        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def create_resident(request):
    current = request.user
    try:
        owner = Owner.objects.get(rut=current.username)
        if owner:
            if request.method == 'POST':
                user_form = UserForm(data=request.POST)
                resident_form = ResidentForm(data=request.POST)
                if user_form.is_valid() and resident_form.is_valid():
                    user = user_form.save()
                    user.set_password(user.password)
                    user.save()
                    resident = resident_form.save(commit=False)
                    resident.userOrigin = user
                    resident.rut = user.username
                    resident.save()
                    return HttpResponseRedirect('/dashboard_owner/')
                else:
                    print user_form.errors, resident_form.errors
            else:
                user_form = UserForm()
                resident_form = ResidentForm()
            return render(request, 'owner/register_resident', {'user_form': user_form, 'resident_form': resident_form})

        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def list_residents(request):
    current = request.user
    try:
        owner = Owner.objects.get(rut=current.username)
        if owner:
            residents = Resident.objects.all()
            return render(request, 'owner/list_residents.html', {'residents': residents})
        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})
