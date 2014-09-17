from django.conf.urls import patterns, url

from loz_lol import views

urlpatterns = patterns('',
	#ex: /loz_lol/
    url(r'^$', views.index, name='index'),
    #ex: /loz_lol/1/
    url(r'^(?P<part_id>\d+)/$', views.detail, name='detail'),
    url(r'^install/(\d+)/$', 'install_part', name='install_part'),
)
