from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.Login, name='Login'),
    path('logout/', views.Logout, name='Logout'),
    path('signup/', views.user_signup, name='user_signup'),
    path('user/<slug:username>/', views.to_do, name='to_do'),
    path('user/<slug:username>/add/', views.AddEvent, name='AddEvent'),
    path('user/<slug:username>/delete/<int:id>/', views.Delete, name='Delete')
]