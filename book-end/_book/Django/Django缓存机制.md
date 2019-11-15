Django缓存机制



### 概述

对于中等流量网站来说，尽可能的减少开销是必要的。缓存数据就是为了保存那些需要很多计算资源大的结果，这样的的话就不必在下次重复消耗计算资源。

  Django自带了一个健壮的缓存系统来保存动态页面，避免每次请求都重新计算。

  Django提供了不同级别的缓存策略，可以缓存特定的视图输出、可以仅仅缓存那些很难计算出来的部分、或者缓存整个网站。

 

  将缓存存储到redis中，默认使用redis中的数据库，首先需要安装扩展库，pip install django-redis-cache。

  然后在setting.py里配置，

		CACHES={
	'default':{
	    'BACKEND':'redis_cache.cache.RedisCache',
	    'LOCATION':'localhost:6379',#redis数据库，
	    'TIMEOUT':60  #过期时间
	}
	}
  然后再，**单个view缓存**：

第一种方法在视图views里面设置，

		django.views.decorators.cache.cache_page装饰器用于对视图的输出进行缓存
		from django.views.decorators.cache import cache_page

		@cache_page(60 * 2)
		def index(request):
			# return HttpResponse("sunck is a good man")
			return HttpResponse("sunck is a nice man")
cache_page(timeout, [cache=cache name], [key_prefix=key prefix])

cache_page只接受一个参数和两个关键字参数，

- timeout是缓存时间，以秒为单位

- cache：指定使用你的CACHES设置中的哪一个缓存后端

- key_prefix：指定缓存前缀，可以覆盖在配置文件中CACHE_MIDDLEWARE_KEY_PREFIX的值

  

第二种，在路由URL里面设置

```
from django.views.decorators.cache import cache_page
urlpatterns = ('',
	(r'^foo/(\d{1,2})/$', cache_page(60 * 15)(my_view)),
```