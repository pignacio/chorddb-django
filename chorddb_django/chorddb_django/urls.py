# pylint: disable=line-too-long

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from song.views import HomeView

urlpatterns = patterns(  # pylint: disable=invalid-name
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^song/', include('song.urls', namespace='song')),
    url(r'^admin/', include(admin.site.urls)),
)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += patterns('',
#                             url(r'^__debug__/', include(debug_toolbar.urls)),
#                             )
