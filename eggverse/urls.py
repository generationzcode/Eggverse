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
    path('handle_money', views.handle_money, name="handle_money"),
    path('space_game_loop', views.space_game_loop, name="space_game_loop"),
    path('enter_space', views.enter_space, name="enter_space"),
    path('planet_player', views.planet_player, name="planet_player"),
    path('get_chat', views.planet_chat_get, name="chat_get"),
    path('make_chat', views.planet_chat_make, name="chat_make"),
    path('space_player', views.space_player, name="space_player"),
    path('player_list', views.player_list, name="player_list"),
    path('join_game', views.join_player, name="join_game"),
    path('planet_list', views.planet_list, name="planet_list"),
    path('join_planet', views.join_planet, name="join_planet"),
    path('get_assets', views.get_assets, name="get_assets"),
    path('change_taxation', views.change_taxation, name="change_taxation"),
    path('player_view', views.player_view, name="player_view"),
]

