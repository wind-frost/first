# 使用JWT(Json Web Token认证机制)实现Token认证



session:用户经过应用认证后会在服务端保存，以便于下次请求鉴别。第一点session是储存在服务器上面的，会占用少量内存，如果网站用户非常多的话，会影响服务器的性能；
第二点拓展性:如果网站比较大，需要搭建有多个服务器，但是session是保存在当前服务器的，其他服务器调用不到。第三点：:session是基于cookie进行识别的，容易被CSRF跨站请求伪造拦截。

为什么使用JWT？
 随着技术的发展，分布式web应用的普及，通过session管理用户登录状态成本越来越高，因此慢慢发展成为token的方式做登录身份校验，然后通过token去取redis中的缓存的用户信息，随着之后jwt的出现，校验方式更加简单便捷化，无需通过redis缓存，而是直接根据token取出保存的用户信息，以及对token可用性校验，单点登录更为简单。

JWT架构图



![img](https://upload-images.jianshu.io/upload_images/3383598-c82676bb8445bae9.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200)

![](../img/1.jpg)

基于token的鉴权机制（加密的随机字符串）
基于token的鉴权机制类似于http协议也是无状态的，它不需要在服务端去保留用户的认证信息或者会话信息。基于token认证机制的应用不需要去考虑用户在哪一台服务器登录了，这就为应用的扩展提供了便利。token放在请求头部中，不易被请求，而且可以设置过期时间。
第三方模块：JWT是由三段信息构成的,第一部分我们称它为头部（header),第二部分我们称其为载荷（payload, 类似于飞机上承载的物品)，第三部分是签证（signature).

##### jwt的头部（header）承载两部分信息

声明是jwt类型
声明加密的算法 通常直接使用 HMAC SHA256
然后将头部进行base64加密
完整的头部就像下面这样的JSON：

    {
      'typ': 'JWT',
      'alg': 'HS256'
    }

然后将头部进行base64加密（该加密是可以对称解密的),构成了第一部分.

    eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9

##### 第二部分payload：存放有效信息，这些有效信息包含三个部分这些有效信息包含三个部分

标准中注册的声明
公共的声明
私有的声明
标准中注册的声明 (建议但不强制使用) ：
iss: jwt签发者
sub: jwt所面向的用户
aud: 接收jwt的一方
exp: jwt的过期时间，这个过期时间必须要大于签发时间
nbf: 定义在什么时间之前，该jwt都是不可用的.
iat: jwt的签发时间
jti: jwt的唯一身份标识，主要用来作为一次性token,从而回避重放攻击。
公共的声明 ： 公共的声明可以添加任何的信息，一般添加用户的相关信息或其他业务需要的必要信息.但不建议添加敏感信息，因为该部分在客户端可解密.
私有的声明 ： 私有声明是提供者和消费者所共同定义的声明，一般不建议存放敏感信息，因为base64是对称解密的，意味着该部分信息可以归类为明文信息。
定义一个payload:

    {
      "sub": "1234567890",
      "name": "John Doe",
      "admin": true
    }

然后将其进行base64加密，得到JWT的第二部分。

    eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9Signature



##### 第三部分Signature 

Signature部分是对前两部分的签名，防止数据篡改。

首先，需要指定一个密钥（secret）。这个密钥只有服务器才知道，不能泄露给用户。然后，使用 Header 里面指定的签名算法（默认是 HMAC SHA256），按照下面的公式产生签名。

```javascript
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret)
```

算出签名以后，把 Header、Payload、Signature 三个部分拼成一个字符串，每个部分之间用"点"（`.`）分隔，连接成一个完整的字符串,构成了最终的jwt，就可以返回给用户。



    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ


secret是保存在服务器端的（配置文件里），jwt的签发生成也是在服务器端的，secret就是用来进行jwt的签发和jwt的验证，所以，它就是你服务端的私钥，在任何场景都不应该流露出去。

优点
因为json的通用性，所以JWT是可以进行跨语言支持的。
因为有了payload部分，所以JWT可以在自定义一些参数，非敏感信息。
便于传输，jwt的构成非常简单，字节占用很小，所以它是非常便于传输的。
jwt不需要在服务端保存会话信息, 易于应用的扩展。
安全相关
不应该在jwt的payload部分存放敏感信息，因为该部分是客户端可解密的部分。
保护好secret私钥，该私钥非常重要。
如果可以，请使用https协议。

## JWT 的使用方式

客户端收到服务器返回的 JWT，可以储存在 Cookie 里面，也可以储存在 localStorage。

此后，客户端每次与服务器通信，都要带上这个 JWT。你可以把它放在 Cookie 里面自动发送，但是这样不能跨域，所以更好的做法是放在 HTTP 请求的头信息`Authorization`字段里面。

> ```javascript
> Authorization: Bearer <token>
> ```

另一种做法是，跨域的时候，JWT 就放在 POST 请求的数据体里面。











基于token的鉴权机制

基于token的鉴权机制类似于http协议也是无状态的，它不需要在服务端去保留用户的认证信息或者会话信息。这就意味着基于token认证机制的应用不需要去考虑用户在哪一台服务器登录了，这就为应用的扩展提供了便利。 流程上是这样的：

​	• 用户使用用户名密码来请求服务器

​	• 服务器进行验证用户的信息

​	• 服务器通过验证发送给用户一个token

​	• 客户端存储token，并在每次请求时附送上这个token值

​	• 服务端验证token值，并返回数据

这个token必须要在每次请求时传递给服务端，它应该保存在请求头里， 另外，服务端要支持CORS(跨来源资源共享)策略，一般我们在服务端这么做就可以了Access-Control-Allow-Origin: *。

