[Django中的类视图及三种类视图装饰器]( https://blog.csdn.net/weixin_44786530/article/details/93239823 )

1 类视图引入
以函数的方式定义的视图称为函数视图，函数视图便于理解。但是遇到一个视图对应的路径提供了多种不同HTTP请求方式的支持时，便需要在一个函数中编写不同的业务逻辑，代码可读性与复用性都不佳。

 def register(request):
    """处理注册"""

    # 获取请求方法，判断是GET/POST请求
    if request.method == 'GET':
        # 处理GET请求，返回注册页面
        return render(request, 'register.html')
    else:
        # 处理POST请求，实现注册逻辑
        return HttpResponse('这里实现注册逻辑')
在Django中也可以使用类来定义一个视图，称为类视图。

使用类视图可以将视图对应的不同请求方式以类中的不同方法来区别定义。如下所示

```
from django.views.generic import View

class RegisterView(View):
    """类视图：处理注册"""
    
    def get(self, request):
    """处理GET请求，返回注册页面"""
    return render(request, 'register.html')

    def post(self, request):
        """处理POST请求，实现注册逻辑"""
        return HttpResponse('这里实现注册逻辑')
```

类视图的好处：

代码可读性好
类视图相对于函数视图有更高的复用性， 如果其他地方需要用到某个类视图的某个特定逻辑，直接继承该类视图即可
2 类视图使用
定义类视图需要继承自Django提供的父类View，可使用from django.views.generic import View或者from django.views.generic.base import View 导入，定义方式如上所示。

配置路由时，使用类视图的as_view()方法来添加。

```
urlpatterns = [
    # 视图函数：注册
    # url(r'^register/$', views.register, name='register'),
    # 类视图：注册
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
]
```

3 类视图原理

    @classonlymethod
    def as_view(cls, **initkwargs):
        """
        Main entry point for a request-response process.
        """
        ...省略代码...
        
      def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.request = request
            self.args = args
            self.kwargs = kwargs
            # 调用dispatch方法，按照不同请求方式调用不同请求方法
            return self.dispatch(request, *args, **kwargs)
     
        ...省略代码...
     
        # 返回真正的函数视图
        return view

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
4 类视图使用装饰器
为类视图添加装饰器，可以使用三种方法。

为了理解方便，我们先来定义一个为函数视图准备的装饰器（在设计装饰器时基本都以函数视图作为考虑的被装饰对象），及一个要被装饰的类视图。

    def my_decorator(func):
        def wrapper(request, *args, **kwargs):
            print('自定义装饰器被调用了')
            print('请求路径%s' % request.path)
            return func(request, *args, **kwargs)
        return wrapper
    
    class DemoView(View):
        def get(self, request):
            print('get方法')
            return HttpResponse('ok')
            
    def post(self, request):
        print('post方法')
        return HttpResponse('ok')
4.1 在URL配置中装饰
urlpatterns = [
    url(r'^demo/$', my_decorate(DemoView.as_view()))
]
此种方式最简单，但因装饰行为被放置到了url配置中，单看视图的时候无法知道此视图还被添加了装饰器，不利于代码的完整性，不建议使用。

此种方式会为类视图中的所有请求方法都加上装饰器行为（因为是在视图入口处，分发请求方式前）。

4.2 在类视图中装饰
在类视图中使用为函数视图准备的装饰器时，不能直接添加装饰器，需要使用method_decorator将其转换为适用于类视图方法的装饰器。

    from django.utils.decorators import method_decorator
    
    #为全部请求方法添加装饰器
    
    class DemoView(View):
        @method_decorator(my_decorator)
        def dispatch(self, *args, **kwargs):
            return super().dispatch(*args, **kwargs)
    
        def get(self, request):
            print('get方法')
            return HttpResponse('ok')
    
        def post(self, request):
            print('post方法')
            return HttpResponse('ok')
            
    #为特定请求方法添加装饰器
    class DemoView(View):
    	@method_decorator(my_decorator)
        def get(self, request):
            print('get方法')
            return HttpResponse('ok')
    
        def post(self, request):
            print('post方法')
            return HttpResponse('ok')

method_decorator装饰器还支持使用name参数指明被装饰的方法

#为全部请求方法添加装饰器

    @method_decorator(my_decorator, name='dispatch')
    class DemoView(View):
        def get(self, request):
            print('get方法')
            return HttpResponse('ok')
            
        def post(self, request):
            print('post方法')
            return HttpResponse('ok')

    #为特定请求方法添加装饰器
    
    @method_decorator(my_decorator, name='get')
    class DemoView(View):
        def get(self, request):
            print('get方法')
            return HttpResponse('ok')	
        def post(self, request):
            print('post方法')
            return HttpResponse('ok')
为什么需要使用method_decorator???

为函数视图准备的装饰器，其被调用时，第一个参数用于接收request对象

```
def my_decorate(func):
    def wrapper(request, *args, **kwargs):  # 第一个参数request对象
        ...代码省略...
        return func(request, *args, **kwargs)
    return wrapper
```


而类视图中请求方法被调用时，传入的第一个参数不是request对象，而是self 视图对象本身，第二个位置参数才是request对象

    
    class DemoView(View):
        def dispatch(self, request, *args, **kwargs):
            ...代码省略...
            
        def get(self, request):
        	...代码省略...
所以如果直接将用于函数视图的装饰器装饰类视图方法，会导致参数传递出现问题。

method_decorator的作用是为函数视图装饰器补充第一个self参数，以适配类视图方法。

如果将装饰器本身改为可以适配类视图方法的，类似如下，则无需再使用method_decorator。

```
def my_decorator(func):
    def wrapper(self, request, *args, **kwargs):  # 此处增加了self
        print('自定义装饰器被调用了')
        print('请求路径%s' % request.path)
        return func(self, request, *args, **kwargs)  # 此处增加了self
    return wrapper
```

4.3 构造Mixin扩展类
使用面向对象多继承的特性。

    class MyDecoratorMixin(object):
        @classmethod
        def as_view(cls, *args, **kwargs):
            view = super().as_view(*args, **kwargs)
            view = my_decorator(view)
            return view
    
    class DemoView(MyDecoratorMixin, View):
        def get(self, request):
            print('get方法')
            return HttpResponse('ok')
        def post(self, request):
            print('post方法')
            return HttpResponse('ok')
使用Mixin扩展类，也会为类视图的所有请求方法都添加装饰行为。
————————————————
版权声明：本文为CSDN博主「1024小神」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_44786530/article/details/93239823