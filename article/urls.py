from django.urls import path
from . import views

urlpatterns = [
    path('article/post/<int:pk>/', views.post_detail, name='post_detail'),
    path('ajax_calls/search/', views.search, name='search'),
    path('search/', views.post_search, name='post_search'),
    path('', views.main_title, name='main_title'),
]
