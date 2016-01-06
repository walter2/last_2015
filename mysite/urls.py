from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views


admin.autodiscover()

urlpatterns = [
    url(r'', include('blog.urls')),
    url(r'^accounts/login/$', views.login),
    url(r'^accounts/logout/$', views.logout, {'next_page':'/'}),
    url(r'^admin/', admin.site.urls),
]

