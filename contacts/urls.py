from django.urls import path

from . import views

urlpatterns = [
    path('send_friend_request/<int:userID>/', views.send_friend_request, name='send friend request'),
    path('accept_friend_request/<int:requestID>/', views.accept_friend_request, name='accept friend request'),
    path('deny_friend_request/<int:requestID>/', views.deny_friend_request, name='deny friend request'),
    path('delete_from_friends/<int:personID>/', views.delete_from_friends, name='del from friends'),
    path('recall_request/<int:requestID>/', views.recall_request, name='recall request'),
    path('', views.test, name='test'),
    path('users/', views.see_users, name='see_users'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
]
