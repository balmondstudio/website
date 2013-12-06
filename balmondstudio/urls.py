from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'balmondstudio.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^crossover/', include('crossover.urls', namespace='crossover')),
    url(r'^', include('crossover.urls', namespace='crossover')),
    url(r'^admin/', include(admin.site.urls)),
)
