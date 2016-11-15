
from django.conf.urls import url,include
from django.contrib import admin
from sharefile import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include("sharefile.urls")),
    url(r'^login/$', views.acc_login,name='login'),
    url(r'^changepwd/$', views.changepwd,name='changepwd'),
    url(r'^logout/$', views.acc_logout,name='logout'),

    # url(r'^.*',views.return500,name='error500'),
]
