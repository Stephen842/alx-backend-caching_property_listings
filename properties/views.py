from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .utils import get_all_properties


# Cache the property list view for 15 minutes
@cache_page(60 * 15)
def property_list(request):
    # Use low-level cache function from utils.py file
    data = get_all_properties()
    return JsonResponse({'properties': data})