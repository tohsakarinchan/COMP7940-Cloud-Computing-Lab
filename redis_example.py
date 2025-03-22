"""Basic connection example.
"""

import redis

r = redis.Redis(
    host='redis-17571.c266.us-east-1-3.ec2.redns.redis-cloud.com',
    port=17571,
    decode_responses=True,
    username="default",
    password="z6GjGQDhXTjjo5O7LMmqlKwOkC9vlbcL",
)

success = r.set('foo', 'bar')
# True

result = r.get('foo')
print(result)
# >>> bar