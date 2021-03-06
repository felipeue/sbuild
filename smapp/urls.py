from django.conf.urls import patterns, url
from smapp import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^login/$', views.login_resident, name='login'),
                       url(r'^login_concierge/$', views.login_consierge, name='login_concierge'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^dashboard/$', views.dashboard_resident, name='dashboard'),
                       url(r'^dashboard_concierge/$', views.dashboard_consierge, name='dashboard_concierge'),
                       url(r'^register_visit/$', views.register_visit, name='register visit'),
                       url(r'^historical_record/$', views.historical_record, name='historical record'),
                       url(r'^visit_record/$', views.list_visit, name='visit record'),
                       url(r'^publish/$', views.post_publication, name='publish'),
                       url(r'^publications_wall/$', views.publications_wall, name='publications_wall'),
                       url(r'^calendar_locations/$', views.event_calendar, name='calendar'),
                       url(r'^all_events/$', views.all_events, name='calendar'),
                       url(r'^create_event/$', views.create_event, name='create_event'),
                       url(r'^publications_wall_consierge/$', views.publications_wall_consierge, name='publications_wall_consierge'),
                       url(r'^publication_consierge/$', views.post_publication_consierge, name='post_publication_consierge'),
                       url(r'^calendar_consierge/$', views.calendar_consierge, name='calendar_consierge'),
                       url(r'^login_owner/$', views.login_owner, name='login_owner'),
                       url(r'^dashboard_owner/$', views.dashboard_owner, name='dashboard_owner'),
                       url(r'^register_rent/$', views.register_rent, name='register_rent'),
                       url(r'^historical_record_owner/$', views.historical_record_owner, name='historical_record_owner'),
                       url(r'^publications_wall_owner/$', views.publications_wall_owner, name='publications_wall_owner'),
                       url(r'^calendar_owner/$', views.calendar_owner, name='calendar_owner'),
                       url(r'^pay_list/$', views.rent_list, name='rent_pay'),
                       url(r'^register_resident/$', views.create_resident, name='register_resident'),
                       url(r'^list_residents/$', views.list_residents, name='list_residents'),
                       url(r'^delete_resident/(?P<resident_id>[\w\-]+)/$', views.delete_resident, name='delete_resident'),
                       url(r'^create_consierge/$', views.create_consierge, name='list_residents'),
                       url(r'^list_consierges/$', views.list_consierge, name='list_consierges'),
                       url(r'^delete_consierge/(?P<consierge_id>[\w\-]+)/$', views.delete_consierge, name='delete_consierge'),
                       url(r'^create_location/$', views.create_location, name='create_location'),
                       url(r'^list_locations/$', views.list_location, name='list_locations'),
                       url(r'^delete_location/(?P<location_id>[\w\-]+)/$', views.delete_location, name='delete_locations'),
                       url(r'^publication_owner/$', views.post_publication_owner, name='post_publication_owner'),
                       )