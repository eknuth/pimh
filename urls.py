from django.conf.urls.defaults import *
import settings
from homeland import views

# Uncomment the next two lines to enable the admin:
from django.contrib.gis import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Example:
                       (r'^$', views.browse_neighborhoods),
                       (r'^neighborhood$', views.get_neighborhood),
                       (r'^search$', views.search),
                       (r'^m$', views.mobile),
                       (r'^neighborhood/quad/(?P<quad>[\w]+)', views.quad_neighborhoods), 
                       (r'^neighborhood/(?P<neighborhood_slug>[-\w]+)', views.map_neighborhood), 
                       (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                                 {'document_root': settings.STATIC_DOC_ROOT}),  
                     
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
