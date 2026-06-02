from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Restaurant


@login_required
@never_cache
def home_view(request):
    return render(request, 'homepage.html')


def search_results(request):
    query = request.GET.get('query')

    show_american_info = False
    show_chinese_info = False

    if query:
        if query.lower() == "american":
            show_american_info = True
            results = None
        elif query.lower() == "chinese":
            show_chinese_info = True
            results = None
        else:
            results = Restaurant.objects.filter(name__icontains=query)  # Adjust based on your search fields
    else:
        results = Restaurant.objects.none()  # Return an empty queryset if no query

    return render(request, 'search_results.html', {
        'results': results,
        'query': query,
        'show_american_info': show_american_info,
        'show_chinese_info': show_chinese_info
    })
