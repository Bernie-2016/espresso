from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'.*', RedirectView.as_view(url='https://berniesanders.com/'))
)
