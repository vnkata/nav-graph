# Setup MacOS

- https://developer.redis.com/develop/python/
- https://redis.com/blog/beyond-the-cache-with-python/
- https://onelinerhub.com/python-redis/save-json-to-redis
Install redis server
```brew
brew tap redis-stack/redis-stack
brew install --cask redis-stack
```
Start server
```
redis-server
```
Connect to the Redis instance
```
redis-cli
```
Example:
```python
import redis
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)
r.set('foo', 'bar')
value = r.get('foo')
print(value)
```