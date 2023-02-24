# pylint: disable=line-too-long

from django.urls import include, re_path

from django.contrib import admin
admin.autodiscover()

urlpatterns = [  # pylint: disable=invalid-name
    re_path(r'^', include('song.urls')),
    re_path(r'^admin/', admin.site.urls),
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += patterns('',
#                             url(r'^__debug__/', include(debug_toolbar.urls)),
#                             )
