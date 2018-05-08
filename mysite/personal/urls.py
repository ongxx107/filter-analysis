from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^index/', views.index, name='index'),
    url(r'^dust loading/', views.dust, name='dust'),
    url(r'^pleating design/',views.pleating, name='pleating'),
    url(r'^electret/$', views.electret, name='electret'),
    url(r'^electret/action/',views.action, name='action'),
    url(r'^login/',views.login, name='login'),
    url(r'^pop_up/',views.pop_up, name='pop_up'),
    url(r'^porosity/',views.porosity, name='porosity'),
    url(r'^electret/fit/',views.fit, name='fit'),
    url(r'^electret/fitting/',views.fitting, name='fitting'),
    url(r'^database/',views.database, name='database')
]
