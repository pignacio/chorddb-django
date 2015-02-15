# pylint: disable=line-too-long

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(  # pylint: disable=invalid-name
    '',
    url(r'^', include('song.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += patterns('',
#                             url(r'^__debug__/', include(debug_toolbar.urls)),
#                             )
