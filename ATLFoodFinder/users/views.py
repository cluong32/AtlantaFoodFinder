import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from .models import FavoriteRestaurant, Restaurant, UserReview
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import Http404
import requests

@login_required
def home(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def profile_view(request):
    user = request.user
    google_profile_image = None

    if user.is_authenticated:
        try:
            social_account = SocialAccount.objects.get(user=user, provider='google')
            google_profile_image = social_account.extra_data.get('picture')  # URL to the profile image
        except SocialAccount.DoesNotExist:
            pass

    return render(request, 'profile.html', {'google_profile_image': google_profile_image})

def map_view(request):
    return render(request, 'map.html')

import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import FavoriteRestaurant

@login_required
@csrf_exempt
def add_favorite(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            place_id = data.get('place_id')
            name = data.get('name')
            address = data.get('address')

            # Validate required fields
            if not place_id or not name or not address:
                return JsonResponse({'error': 'Missing required fields.'}, status=400)

            existing_favorite = FavoriteRestaurant.objects.filter(user=request.user, place_id=place_id).exists()
            if existing_favorite:
                return JsonResponse({'message': 'This restaurant is already in your favorites.'}, status=400)

            favorite = FavoriteRestaurant(
                user=request.user,
                place_id= place_id,
                name= name,
                address= address,
                rating= data.get('rating')
            )
            favorite.save()
            return JsonResponse({'message': 'Favorite added successfully.'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@login_required
def get_favorites(request):
    if request.method == 'GET':
        user = request.user
        favorites = FavoriteRestaurant.objects.filter(user=user).values('name', 'address', 'rating', 'place_id')
        return JsonResponse(list(favorites), safe=False)
    return JsonResponse({'error': 'Invalid method'}, status=405)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

@login_required
@csrf_exempt
def remove_favorite(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            favorite_count, _ = FavoriteRestaurant.objects.filter(
                user=request.user, address=data['address']).delete()
            if favorite_count:
                return JsonResponse({'message': 'Favorite removed successfully.'}, status=200)
            else:
                return JsonResponse({'error': 'Favorite not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@login_required
@csrf_exempt
def toggle_favorite(request, restaurant_id):
    try:
        favorite, created = FavoriteRestaurant.objects.get_or_create(user=request.user, place_id=restaurant_id)

        if not created:
            favorite.delete()
            is_favorited = False
        else:
            is_favorited = True

        return JsonResponse({'is_favorited': is_favorited})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)
# See reviews for a restaurant
def see_reviews(request, place_id):
    # Fetch reviews from Google

  
    restaurant = Restaurant.objects.filter(place_id=place_id).first()
    google_reviews = get_google_reviews(place_id)
    user_reviews = restaurant.userreview_set.all() if restaurant else []

    context = {
        'place_id': place_id,
        'restaurant': restaurant,
        'user_reviews': user_reviews,
        'google_reviews': google_reviews,
    }

    return render(request, 'reviews/see_reviews.html', context)

# Leave a review for a restaurant
@login_required
def leave_review(request, place_id):
    # Attempt to fetch the restaurant from the database
    restaurant = Restaurant.objects.filter(place_id=place_id).first()

    # If the restaurant does not exist, fetch it from the Google Maps API
    if restaurant is None:
        restaurant_data = fetch_restaurant_from_api(place_id)
        if restaurant_data is None:
            raise Http404("No Restaurant matches the given query.")
        # Create a new restaurant record in the database
        restaurant = Restaurant.objects.create(
            name=restaurant_data['name'],
            place_id=restaurant_data['place_id'],
            # Add more fields as needed
        )

    if request.method == 'POST':
        review_text = request.POST['review_text']
        rating = request.POST['rating']
        UserReview.objects.create(user=request.user, restaurant=restaurant, review_text=review_text, rating=rating)
        return redirect('see_reviews', place_id=place_id)

    return render(request, 'reviews/leave_review.html', {'restaurant': restaurant})

def fetch_restaurant_from_api(place_id):
    # Replace YOUR_API_KEY with your actual API key
    api_key = settings.GOOGLE_PLACES_API_KEY
    url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}'

    response = requests.get(url)
    data = response.json()

    if data.get('status') == 'OK':
        return data['result']
    else:
        return None

def get_google_reviews(place_id):
    api_key = settings.GOOGLE_PLACES_API_KEY
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=reviews&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if 'result' in data and 'reviews' in data['result']:
        return data['result']['reviews']
    return []