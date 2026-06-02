from django.urls import path
from . import views  # Import your views from the home app

urlpatterns = [
    path('', views.home_view, name='home'),  # Route the home page to home_view
    path('search/', views.search_results, name='search_results'),
]


