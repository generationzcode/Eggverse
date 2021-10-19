from django.urls import path,re_path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^signUp/$', views.signUp, name='signUp'),
    re_path(r'^signUpF/$', views.signUpF, name='signUpF'),
    re_path(r'^signIn/$', views.signIn, name='signIn'),
    re_path(r'^signInF/$', views.signInF, name='signInF'),
    path('logout', views.logout_view, name='logout'),
    path('planet_join', views.joined_game, name='planet_join'),
    path('planet_game_loop', views.planet_game_loop, name='planet_game_loop'),
    path('change_quadrant', views.change_quadrant, name="change_quadrant"),
    path('enter_planet', views.enter_planet, name="enter_planet"),
    path('handle_death', views.handle_death, name="handle_death"),
    path('space_game_loop', views.change_quadrant, name="space_game_loop"),
    path('enter_space', views.enter_space, name="enter_space"),
    path('planet_player', views.planet_player, name="planet_player"),
]

