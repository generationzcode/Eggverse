from django.urls import path,re_path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^signUp/$', views.signUp, name='signUp'),
    re_path(r'^signUpF/$', views.signUpF, name='signUpF'),
    re_path(r'^signIn/$', views.signIn, name='signIn'),
    re_path(r'^signInF/$', views.signInF, name='signInF'),
    path('logout', views.logout_view, name='logout'),
]

