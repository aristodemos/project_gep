from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gep_db.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^loz_lol/', include('loz_lol.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
