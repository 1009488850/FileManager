
from django.conf.urls import url
from sharefile import views

urlpatterns = [
    url(r'^$', views.show_home,name='home'),
    url(r'^index/$', views.show_tables,name='index'),
    url(r'^adduserinfo$', views.AddUserInfo,name='userinfo'),
    url(r'^remove_img$', views.remove_img,name='removeimg'),
    url(r'^upload_img$', views.upload_img,name='uploadimg'),
    # url(r'^.*', views.return500,name='error500'),


]
