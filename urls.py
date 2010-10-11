from django.conf.urls.defaults import *
import settings
from homeland import views
from transit import views as transit_views
from diy import views as diy_views

# Uncomment the next two lines to enable the admin:
from django.contrib.gis import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Example:
#                       (r'^$', views.browse_neighborhoods),
#                       (r'^neighborhood$', views.get_neighborhood),

                       (r'^lookup$', views.lookup),
                       (r'^map/(?P<place_type>\w+)$', views.map),
                       (r'^log$', views.request_kml),
                       (r'^transit/stops$', transit_views.get_nearby_stops),
                       (r'^transit/stop/(?P<stop_id>\d+)/(?P<route_id>\d+)$', transit_views.get_stop),
                       (r'^local/(?P<place_type>.*)$', views.local_search),
                       (r'^diy$', diy_views.index),
                       (r'^diy/create$', diy_views.create),
                       (r'^quad/(?P<quad>\w+)', views.neighborhoods_by_quad),
                       
                       (r'^place/(?P<place_id>[\w]+)', views.place), 
                       (r'^browse_by_neighborhood/(?P<neighborhood_slug>[-\w]+)', views.neighborhood), 
                       (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                                 {'document_root': settings.STATIC_DOC_ROOT}),  
                       (r'^', views.browse),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
 #   (r'^admin/', include(admin.site.urls)),
)
