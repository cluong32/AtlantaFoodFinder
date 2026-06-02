from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/login/', views.login_view, name='login'),  # Fixed name to 'login'
    path('accounts/signup/', views.signup_view, name='signup'),
    path('map/', views.map_view, name='map'),
    path('add_favorite/', views.add_favorite, name='add_favorite'),
    path('get_favorites/', views.get_favorites, name='get_favorites'),
    path('remove_favorite/', views.remove_favorite, name='remove_favorite'),
    path('toggle_favorite/<str:restaurant_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('see_reviews/<str:place_id>/', views.see_reviews, name='see_reviews'),
    path('leave_review/<str:place_id>/', views.leave_review, name='leave_review'),
]
