from django.urls import path, re_path
from . import views
from django.views.static import serve
from JinroServer import settings

urlpatterns = [
    path('hall/', views.hall_list),
    path('join/', views.join_game),
    path('start/', views.game_start),
    path("readyGame/",views.ready_game),
    path('uploadIcon/', views.upload_icon),
    path('updateProfile/', views.update_profile),
    path('updateGameSetting/', views.update_game_setting),
    path('exile/', views.exile_player),
    path('doatngiht/', views.do_at_night),
    path("rooms/", views.rooms),
    path("login/", views.login),
    path('joinSakura/', views.join_sakura),
    path('kickPlayer/', views.kick_player),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

]