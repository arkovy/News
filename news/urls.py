from django.urls import path

from . import views
from .views import IndexView, AllNewsView, SingleNewsView, ReadLaterView, AddNewsView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', IndexView.as_view(), name='starting-page'),
    path('news/', AllNewsView.as_view(), name='news-page'),
    path('news/<str:slug>', SingleNewsView.as_view(), name='news-detail-page'),
    path('read-later/', ReadLaterView.as_view(), name='read-later'),
    path('signup/', views.SignUp.as_view(), name='signup'),  # URL для регистрации
    path('login/', auth_views.LoginView.as_view(), name='login'),  # URL для входа
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),   # URL для выхода
    path('add-news/', AddNewsView.as_view(), name='add-news'),
]
