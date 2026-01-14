from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property
import logging


logger = logging.getLogger(__name__)


def get_all_properties():
    # Try to get cached queryset
    queryset = cache.get('all_properties')
    if queryset is None:
        # If not cached, fetch from DB
        queryset = list(Property.objects.all().values(
            'id', 'title', 'description', 'price', 'location', 'created_at'
        ))
        # Store in Redis for 1 hour
        cache.set('all_properties', queryset, 3600)
    return queryset


def get_redis_cache_metrics():
    '''Retrieve Redis hit/miss metrics and calculate hit ratio.'''
    # Connect to the default Redis connection
    redis_conn = get_redis_connection('default')
    
    # Get Redis INFO stats
    info = redis_conn.info()
    hits = info.get('keyspace_hits', 0)
    misses = info.get('keyspace_misses', 0)
    
    # Calculate hit ratio
    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0.0
    
    # Log metrics
    logger.info(f'Redis cache hits: {hits}, misses: {misses}, hit ratio: {hit_ratio:.2f}')
    
    # Return metrics as dict
    return {
        'hits': hits,
        'misses': misses,
        'hit_ratio': hit_ratio
    }