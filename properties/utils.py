from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Try to get cached queryset
    queryset = cache.get('all_properties')
    if queryset is None:
        # If not cached, fetch from DB
        queryset = list(Property.objects.all().values(
            "id", "title", "description", "price", "location", "created_at"
        ))
        # Store in Redis for 1 hour
        cache.set('all_properties', queryset, 3600)
    return queryset
