from django.conf.urls import include, url
from django.contrib import admin

import debug_toolbar

urlpatterns = [
    url(r'^rooms/', include('rooms.urls')),
    url(r'^admin/', admin.site.urls),
]


urlpatterns = [
    url(r'^debug/', include(debug_toolbar.urls)),
] + urlpatterns
