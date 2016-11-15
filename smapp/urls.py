from django.conf.urls import patterns, url
from smapp import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^login/$', views.login_user, name='login'),
                       url(r'^login_concierge/$', views.login_concierge, name='login_concierge'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^dashboard/$', views.dashboard, name='dashboard'),
                       url(r'^dashboard_concierge/$', views.dashboard_concierge, name='dashboard_concierge'),
                       url(r'^register_visit/$', views.register_visit, name='register visit'),
                       url(r'^historical_record/$', views.historical_record, name='historical record'),
                       url(r'^visit_record/$', views.visit_record, name='visit record'),
                       url(r'^publish/$', views.publish, name='publish'),
                       )
