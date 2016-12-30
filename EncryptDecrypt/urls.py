
from django.conf.urls import url

from EncryptDecrypt import views


urlpatterns = [
     url(r'^$', views.viewlogin, name='index'),
  url(r'^Register/', views.viewRegister, name='register'),
    url(r'^RegisterAct/', views.register, name='registeract'),
     url(r'^LoginAct/', views.login, name='loginact'),
       url(r'^inbox/', views.inbox, name='inbox'),
      url(r'^Sentmail/', views.viewSentMail, name='sent'),
       url(r'^trash/', views.viewTrash, name='trash'),
        url(r'^compose/', views.viewCompose, name='compose'),
       url(r'^download/([^/]+)/$', views.downloader,name="downs"),
        url(r'^sendmail/', views.sendmail,name="composed"),
       url(r'^logut/', views.logout, name='logut'),
 
             
  
         
]
