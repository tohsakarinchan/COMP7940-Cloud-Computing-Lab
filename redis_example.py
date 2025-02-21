"""Basic connection example.
"""

import redis

r = redis.Redis(
    host='redis-12442.c1.asia-northeast1-1.gce.redns.redis-cloud.com',
    port=12442,
    decode_responses=True,
    username="default",
    password="P0bMELOJAzqThwSSTgXCQDnAjymyl3Gg",
)

success = r.set('foo', 'bar')
# True

result = r.get('foo')
print(result)
# >>> bar