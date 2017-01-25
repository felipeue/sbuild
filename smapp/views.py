from django.shortcuts import render, render_to_response
from smapp.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from smapp.forms import *
from django.core.exceptions import ObjectDoesNotExist
from fullcalendar.util import events_to_json
# Create your views here.


def index(request):
    return render(request, 'index.html', {})


def login_resident(request):
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
def dashboard_resident(request):
    current = request.user
    try:
        resident = Resident.objects.get(userOrigin=current.id)
        if resident:
            r = Resident.objects.filter(userOrigin=current)
            publications = Publication.objects.order_by('-id')[:5]
            records = Visit.objects.filter(resident=r).order_by('-id')[:5]
            reservations = Event.objects.order_by('-id')[:6]
            payments = Rent.objects.filter(resident=r).order_by('id')[:5]
            return render(request, 'resident/index_dashboard.html',
                          {
                              'records': records,
                              'publications': publications,
                              'reservations': reservations,
                              'payments': payments,
                              'resident': resident
                          })
        else:
            return render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def list_visit(request):
    current = request.user
    try:
        resident = Resident.objects.get(userOrigin=current.id)
        if resident:
            records = Visit.objects.filter(resident=resident).order_by('id').all()
            return render(request, 'resident/visit_record.html', {'records': records})
        else:
            return render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def post_publication(request):
    current = request.user
    try:
        resident = Resident.objects.get(userOrigin=current)
        if resident:
            if request.method == 'POST':
                publication_form = PublicationForm(data=request.POST)
                if publication_form.is_valid():
                    publication = publication_form.save(commit=False)
                    publication.publisher = current
                    publication.save()
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
        resident = Resident.objects.get(userOrigin=current)
        if resident:
            publications = Publication.objects.order_by('-id').all()
            return render(request, 'resident/publications_wall.html', {'publications': publications})
        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def rent_list(request):
    current = request.user
    try:
        resident = Resident.objects.get(userOrigin=current)
        if resident:
            rents = Rent.objects.filter(resident=resident).order_by('-id').all()
            return render(request, 'resident/pay_list.html', {'rents': rents})
        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def event_calendar(request):
    current = request.user
    try:
        resident = Resident.objects.get(userOrigin=current)
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
        resident = Resident.objects.get(userOrigin=current)
        if resident:
            if request.method == 'POST':
                event_form = EventForm(data=request.POST)
                if event_form.is_valid():
                    event = event_form.save(commit=False)
                    event.all_day = 0
                    event.end = event.start
                    event.resident = resident
                    nombre = event.resident.userOrigin.first_name
                    apellido = event.resident.userOrigin.last_name
                    lugar = event.location.name
                    event.title = nombre + ' ' + apellido + '-' + lugar
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


def login_consierge(request):
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
def dashboard_consierge(request):
    current = request.user
    try:
        consierge = Consierge.objects.get(userOrigin=current)
        if consierge:
            records = Visit.objects.order_by('-id')[:5]
            publications = Publication.objects.order_by('-id')[:5]
            return render(request, 'consierge/concierge_dashboard.html',
                          {
                              'records': records,
                              'publications': publications
                          })
        else:
            return render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def register_visit(request):
    current = request.user
    try:
        concierge = Consierge.objects.get(userOrigin=current)
        if concierge:
            if request.method == 'POST':
                visit_form = VisitForm(data=request.POST)
                if visit_form.is_valid():
                    visit = visit_form.save(commit=False)
                    visit.save()
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
        concierge = Consierge.objects.get(userOrigin=current)
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
        consierge = Consierge.objects.get(userOrigin=current)
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
        consierge = Consierge.objects.get(userOrigin=current)
        if consierge:
            return render(request, 'consierge/calendar_locations_consierge.html', {})
        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def post_publication_consierge(request):
    current = request.user
    try:
        consierge = Consierge.objects.get(userOrigin=current)
        if consierge:
            if request.method == 'POST':
                publication_form = PublicationForm(data=request.POST)
                if publication_form.is_valid():
                    publication = publication_form.save(commit=False)
                    publication.publisher = current
                    publication.save()
                    return HttpResponseRedirect('/dashboard_concierge/')
            else:
                publication_form = PublicationForm()
            return render(request, 'consierge/publish_consierge.html', {'publication_form': publication_form})
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
        owner = Owner.objects.get(userOrigin=current)
        if owner:
            records = Visit.objects.order_by('-id')[:5]
            publications = Publication.objects.order_by('-id')[:5]
            return render(request, 'owner/owner_dashboard.html',
                          {
                              'records': records,
                              'publications': publications
                          })
        else:
            return render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})

@login_required
def register_rent(request):
    current = request.user
    try:
        owner = Owner.objects.get(userOrigin=current)
        if owner:
            if request.method == 'POST':
                rent_form = RentForm(data=request.POST)
                if rent_form.is_valid():
                    rent = rent_form.save(commit=False)
                    rent.save()
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
        owner = Owner.objects.get(userOrigin=current)
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
        owner = Owner.objects.get(userOrigin=current)
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
        owner = Owner.objects.get(userOrigin=current)
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
        owner = Owner.objects.get(userOrigin=current)
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
                    resident.save()
                    return HttpResponseRedirect('/dashboard_owner/')
                else:
                    render_to_response('login_error.html', {})
            else:
                user_form = UserForm()
                resident_form = ResidentForm()
            return render(request, 'owner/register_resident',
                          {
                              'user_form': user_form,
                              'resident_form': resident_form
                          })

        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def list_residents(request):
    current = request.user
    try:
        owner = Owner.objects.get(userOrigin=current)
        if owner:
            residents = Resident.objects.all()
            return render(request, 'owner/list_residents.html', {'residents': residents})
        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def delete_resident(request, resident_id):
    current = request.user
    try:
        owner = Owner.objects.get(userOrigin=current)
        if owner:
            resident = User.objects.get(id=resident_id)
            resident.delete()
            return HttpResponseRedirect('/list_residents/')
        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def create_consierge(request):
    current = request.user
    try:
        owner = Owner.objects.get(userOrigin=current)
        if owner:
            if request.method == 'POST':
                user_form = UserForm(data=request.POST)
                consierge_form = ConsiergeForm(data=request.POST)
                if user_form.is_valid() and consierge_form.is_valid():
                    user = user_form.save()
                    user.set_password(user.password)
                    user.save()
                    consierge = consierge_form.save(commit=False)
                    consierge.userOrigin = user
                    consierge.save()
                    return HttpResponseRedirect('/dashboard_owner/')
                else:
                    render_to_response('login_error.html', {})
            else:
                user_form = UserForm()
                consierge_form = ConsiergeForm()
            return render(request, 'owner/register_consierge.html',
                          {
                              'user_form': user_form,
                              'consierge_form': consierge_form
                          })

        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def list_consierge(request):
    current = request.user
    try:
        owner = Owner.objects.get(userOrigin=current)
        if owner:
            consierges = Consierge.objects.all()
            return render(request, 'owner/list_consierges.html', {'consierges': consierges})
        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def delete_consierge(request, consierge_id):
    current = request.user
    try:
        owner = Owner.objects.get(userOrigin=current)
        if owner:
            consierge = User.objects.get(id=consierge_id)
            consierge.delete()
            return HttpResponseRedirect('/list_consierges/')
        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def create_location(request):
    current = request.user
    try:
        owner = Owner.objects.get(userOrigin=current)
        if owner:
            if request.method == 'POST':
                location_form = LocationForm(data=request.POST)
                if location_form.is_valid():
                    location = location_form.save()
                    location.save()
                    return HttpResponseRedirect('/list_locations/')
                else:
                    render_to_response('login_error.html', {})
            else:
                location_form = LocationForm()
            return render(request, 'owner/register_location.html', {'location_form': location_form})

        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def list_location(request):
    current = request.user
    try:
        owner = Owner.objects.get(userOrigin=current)
        if owner:
            locations = Location.objects.all()
            return render(request, 'owner/list_locations.html', {'locations': locations})
        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def delete_location(request, location_id):
    current = request.user
    try:
        owner = Owner.objects.get(userOrigin=current)
        if owner:
            location = Location.objects.get(id=location_id)
            location.delete()
            return HttpResponseRedirect('/list_consierges/')
        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})


@login_required
def post_publication_owner(request):
    current = request.user
    try:
        owner = Owner.objects.get(userOrigin=current)
        if owner:
            if request.method == 'POST':
                publication_form = PublicationForm(data=request.POST)
                if publication_form.is_valid():
                    publication = publication_form.save(commit=False)
                    publication.publisher = current
                    publication.save()
                    return HttpResponseRedirect('/dashboard_owner/')
            else:
                publication_form = PublicationForm()
            return render(request, 'owner/publication_owner.html', {'publication_form': publication_form})
        else:
            render_to_response('login_error.html', {})
    except ObjectDoesNotExist:
        return render_to_response('login_error.html', {})