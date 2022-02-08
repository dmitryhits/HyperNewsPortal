from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.head_news),
    path('news/<int:news_id>/', views.news),
    path('news/create/', views.News.as_view()),
    path('', views.under_construction),
]