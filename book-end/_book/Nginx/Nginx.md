Nginx介绍



Nginx同Apache一样都是一种WEB服务器。基于REST架构风格，以统一资源描述符(Uniform Resources Identifier)URI或者统一资源定位符(Uniform Resources Locator)URL作为沟通依据，通过HTTP协议提供各种网络服务。

然而，这些服务器在设计之初受到当时环境的局限，例如当时的用户规模，网络带宽，产品特点等局限并且各自的定位和发展都不尽相同。这也使得各个WEB服务器有着各自鲜明的特点。

 

Apache的发展时期很长，而且是毫无争议的世界第一大服务器。它有着很多优点：稳定、开源、跨平台等等。它出现的时间太长了，它兴起的年代，互联网产业远远比不上现在。所以它被设计为一个重量级的。它不支持高并发的服务器。在Apache上运行数以万计的并发访问，会导致服务器消耗大量内存。操作系统对其进行进程或线程间的切换也消耗了大量的CPU资源，导致HTTP请求的平均响应速度降低。

这些都决定了Apache不可能成为高性能WEB服务器，轻量级高并发服务器Nginx就应运而生了。

俄罗斯的工程师Igor Sysoev，他在为Rambler Media工作期间，使用C语言开发了Nginx。Nginx作为WEB服务器一直为Rambler Media提供出色而又稳定的服务。

然后呢，Igor Sysoev将Nginx代码开源，并且赋予自由软件许可证。

由于：

Nginx使用基于事件驱动架构(事件驱动架构（Event Driven Architecture，EDA）可传输于松散耦合的组件和服务之间。一个事件驱动系统典型地由事件消费者和事件产生者组成。事件消费者向事件管理器订阅事件，事件产生者向事件管理器发布事件。当事件管理器从事件产生者那接收到一个事件时，事件管理把这个事件转送给相应的事件消费者。如果这个事件消费者是不可用的，事件管理者将保留这个事件，一段间隔之后再次转送该事件消费者。这种事件传送方法在基于消息的系统里就是:储存（store）和转送（forward）

,是一种以事件为媒介，实现组件或服务之间最大松耦合的方式。传统面向接口编程是以接口为媒介，实现调用接口者和接口实现者之间的解耦，但是这种解耦程度不是很高，如果接口发生变化，双方代码都需要变动，而事件驱动则是调用者和被调用者互相不知道对方，两者只和中间消息队列耦合。

· )，使得其可以支持数以百万级别的TCP连接

· 高度的模块化和自由软件许可证是的第三方模块层出不穷（这是个开源的时代啊~）

· Nginx是一个跨平台服务器，可以运行在Linux,Windows,FreeBSD,Solaris, AIX,Mac OS等操作系统上

· 这些优秀的设计带来的极大的稳定性

 

Nginx是一款自由的、开源的、高性能的HTTP服务器和反向代理服务器；同时也是一个IMAP、POP3、SMTP代理服务器；Nginx可以作为一个HTTP服务器进行网站的发布处理，另外Nginx可以作为反向代理进行负载均衡的实现。

 

 

正向代理和反向代理

![img](file:///C:\Users\think\AppData\Local\Temp\ksohtml8536\wps1.jpg) 

正向代理

正向代理 是一个位于客户端和原始服务器(origin server)之间的服务器，为了从原始服务器取得内容，客户端向代理发送一个请求并指定目标(原始服务器)，然后代理向原始服务器转交请求并将获得的内容返回给客户端

 

我是一个用户，我访问不了某网站，但是我能访问一个代理服务器，这个代理服务器呢,他能访问那个我不能访问的网站，于是我先连上代理服务器,告诉他我需要那个无法访问网站的内容，代理服务器去取回来,然后返回给我。

 

**正向代理的用途：**

　　（1）访问原来无法访问的资源，如google

​        （2） 可以做缓存，加速访问资源

　　 （3）对客户端访问授权，上网进行认证

　　 （4）代理可以记录用户访问记录（上网行为管理），对外隐藏用户信息

 

 

反向代理

初次接触方向代理的感觉是，客户端是无感知代理的存在的，反向代理对外都是透明的，访问者者并不知道自己访问的是一个代理。因为客户端不需要任何配置就可以访问。

　　反向代理（Reverse Proxy）实际运行方式是指以代理服务器来接受internet上的连接请求，然后将请求转发给内部网络上的服务器，并将从服务器上得到的结果返回给internet上请求连接的客户端，此时代理服务器对外就表现为一个服务器。

反向代理的作用：

（1）保证内网的安全，可以使用反向代理提供WAF功能，阻止web攻击

大型网站，通常将反向代理作为公网访问地址，Web服务器是内网。

![img](file:///C:\Users\think\AppData\Local\Temp\ksohtml8536\wps2.jpg)

 

（2）负载均衡，通过反向代理服务器来优化网站的负载

![img](file:///C:\Users\think\AppData\Local\Temp\ksohtml8536\wps3.jpg)

 

 

负载均衡

Nginx支持的负载均衡调度算法方式如下：

1. weight轮询(默认)：接收到的请求按照顺序逐一分配到不同的后端服务器，即使在使用过程中，某一台后端服务器宕机，Nginx会自动将该服务器剔除出队列，请求受理情况不会受到任何影响。 这种方式下，可以给不同的后端服务器设置一个权重值(weight)，用于调整不同的服务器上请求的分配率；权重数据越大，被分配到请求的几率越大；该权重值，主要是针对实际工作环境中不同的后端服务器硬件配置进行调整的。

2. ip_hash：每个请求按照发起客户端的ip的hash结果进行匹配，这样的算法下一个固定ip地址的客户端总会访问到同一个后端服务器，这也在一定程度上解决了集群部署环境下session共享的问题。

3. fair：智能调整调度算法，动态的根据后端服务器的请求处理到响应的时间进行均衡分配，响应时间短处理效率高的服务器分配到请求的概率高，响应时间长处理效率低的服务器分配到的请求少；结合了前两者的优点的一种调度算法。但是需要注意的是Nginx默认不支持fair算法，如果要使用这种调度算法，请安装upstream_fair模块。

4. url_hash：按照访问的url的hash结果分配请求，每个请求的url会指向后端固定的某个服务器，可以在Nginx作为静态服务器的情况下提高缓存效率。同样要注意Nginx默认不支持这种调度算法，要使用的话需要安装Nginx的hash软件包。

 

 

![img](file:///C:\Users\think\AppData\Local\Temp\ksohtml8536\wps4.jpg) 

rewrite模块会根据PCRE正则匹配重写URI

FCGI：fast common gateway interface 快速通用网关接口

热部署，就是在应用正在运行的时候升级软件，却不需要重新启动应用。

 



Ngnix参数配制



\#普通配置

\#==性能配置



\#运行用户

user nobody;

\#pid文件

pid logs/nginx.pid;

 

\#Nginx基于事件的非阻塞多路复用模型（epoll或kquene）

\#一个进程在短时间内可以响应大量请求，工作进程设置与cpu数相同，避免cpu在多个进程间切换增加开销

\#==worker进程数，通常设置<=CPU数量，auto为自动检测，一般设置最大8个即可，再大性能提升较小或不稳定

worker_processes auto;

 

\#==将每个进程绑定到特定cpu上，避免进程在cpu间切换的开销

worker_cpu_affinity 00000001 00000010 00000100 00001000 00010000 00100000 01000000 10000000;

 

\#==worker进程打开最大文件数，可CPU*10000设置，或设置系统最大数量655350

worker_rlimit_nofile 102400;

\#全局错误日志

error_log  logs/error.log;

 

 

\#events模块中包含nginx中所有处理连接的设置，并发响应能力的关键配置

events {

​    \#==每个进程同时打开的最大连接数（最大并发数）

​    worker_connections 102400;

​    

​    \#==告诉nginx收到一个新链接通知后接受尽可能多的链接

​    \#multi_accept on;

​    

​    \#一般http 1.1协议下，浏览器默认使用两个并发链接

​    \#如果是反向代理，nginx需要和客户端保持连接，还需要和后端服务器保持连接

​    \#Http服务器时，设置max_client=worker_processes*worker_connections/2

​    \#反向代理时，设置max_client=worker_processes*worker_connections/4    

​    \#==最大可用客户端数

​    \#max_client 

​    

​    \#==使用非阻塞模型，设置复用客户端线程的轮训方法

​    use epoll;

}

 

 

\#http模块控制着nginx http处理的所有核心特性

http {

​    \#打开或关闭错误页面中的nginx版本号等信息

​    server_tokens on;

​    \#!server_tag on;

​    \#!server_info on;

​    \#==优化磁盘IO设置，指定nginx是否调用sendfile函数来输出文件，普通应用设为on，下载等磁盘IO高的应用，可设为off

​    sendfile on;

​    

​    \#缓存发送请求，启用如下两个配置，会在数据包达到一定大小后再发送数据

​    \#这样会减少网络通信次数，降低阻塞概率，但也会影响响应的及时性

​    \#比较适合于文件下载这类的大数据包通信场景

​    \#tcp_nopush on;

​    \#tcp_nodelay on;

 

​    \#==设置nginx是否存储访问日志，关闭这个可以让读取磁盘IO操作更快

​    access_log on;

​    \#设置nginx只记录严重错误，可减少IO压力

​    \#error_log logs/error.log crit;

 

​    \#Http1.1支持长连接

​    \#降低每个链接的alive时间可在一定程度上提高响应连接数量

​    \#==给客户端分配keep-alive链接超时时间

​    keepalive_timeout 30;

 

​    \#设置用户保存各种key的共享内存的参数，5m指的是5兆

​    limit_conn_zone $binary_remote_addr zone=addr:5m;

​    \#为给定的key设置最大的连接数，这里的key是addr，设定的值是100，就是说允许每一个IP地址最多同时打开100个连接

​    limit_conn addr 100;

 

​    \#include指在当前文件中包含另一个文件内容

​    include mime.types;

​    \#设置文件使用默认的mine-type

​    default_type text/html;

​    \#设置默认字符集

​    charset UTF-8;

 

​    \#==设置nginx采用gzip压缩的形式发送数据，减少发送数据量，但会增加请求处理时间及CPU处理时间，需要权衡

​    gzip on;

​    \#==加vary给代理服务器使用，针对有的浏览器支持压缩，有个不支持，根据客户端的HTTP头来判断是否需要压缩

​    gzip_vary on;

​    \#nginx在压缩资源之前，先查找是否有预先gzip处理过的资源

​    \#!gzip_static on;

​    \#为指定的客户端禁用gzip功能

​    gzip_disable "MSIE[1-6]\.";

​    \#允许或禁止压缩基于请求和相应的响应流，any代表压缩所有请求

​    gzip_proxied any;

​    \#==启用压缩的最少字节数，如果请求小于1024字节则不压缩，压缩过程会消耗系统资源

​    gzip_min_length 1024;

​    \#==数据压缩等级，1-9之间，9最慢压缩比最大，压缩比越大对系统性能要求越高

​    gzip_comp_level 2;

​    \#需要压缩的数据格式

​    gzip_types text/plain text/css text/xml text/javascript  application/json application/x-javascript application/xml application/xml+rss; 

 

​    \#静态文件缓存

​    \#==开启缓存的同时也指定了缓存文件的最大数量，20s如果文件没有被请求则删除缓存

​    open_file_cache max=100000 inactive=20s;

​    \#==多长时间检查一次缓存的有效期

​    open_file_cache_valid 30s;

​    \#==有效期内缓存文件最小的访问次数，只有访问超过2次的才会被缓存

​    open_file_cache_min_uses 2;

​    \#当搜索一个文件时是否缓存错误信息

​    open_file_cache_errors on;

 

​    \#==允许客户端请求的最大单文件字节数

​    client_max_body_size 4m;

​    \#==客户端请求头缓冲区大小

​    client_header_buffer_size 4k;

 

​    \#是否启用对发送给客户端的URL进行修改

​    proxy_redirect off;

​    \#后端的Web服务器可以通过X-Forwarded-For获取用户真实IP

​    proxy_set_header Host $host;

​    proxy_set_header X-Real-IP $remote_addr;

​    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

​    \#==nginx跟后端服务器连接超时时间(代理连接超时)

​    proxy_connect_timeout 60;

​    \#==连接成功后，后端服务器响应时间(代理接收超时)

​    proxy_read_timeout 120;

​    \#==后端服务器数据回传时间(代理发送超时)

​    proxy_send_timeout 20;

​    \#==设置代理服务器（nginx）保存用户头信息的缓冲区大小

​    proxy_buffer_size 32k;

​    \#==proxy_buffers缓冲区，网页平均在32k以下的设置

​    proxy_buffers 4 128k;

​    \#==高负荷下缓冲大小（proxy_buffers*2）

​    proxy_busy_buffers_size 256k;

​    \#==设定缓存文件夹大小，大于这个值，将从upstream服务器传

​    proxy_temp_file_write_size 256k;

​    \#==1G内存缓冲空间，3天不用删除，最大磁盘缓冲空间2G

​    proxy_cache_path /home/cache levels=1:2 keys_zone=cache_one:1024m inactive=3d max_size=2g;

 

 

​    \#设定负载均衡服务器列表

​    upstream nginx.test.com{

​        \#后端服务器访问规则

​        \#ip_hash;

​        \#weight参数表示权重值，权值越高被分配到的几率越大

​        \#server 10.11.12.116:80 weight=5;

​        \#PC_Local

​        server 10.11.12.116:80;

​        \#PC_Server

​        server 10.11.12.112:80;

​        \#Notebook

​        \#server 10.11.12.106:80;

​    }

 

​    \#server代表虚拟主机，可以理解为站点（挂载多个站点，只需要配置多个server及upstream节点即可）

​    server {

​        \#监听80端口

​        listen 80;

​        \#识别的域名，定义使用nginx.test.com访问

​        server_name nginx.test.com;

​        \#设定本虚拟主机的访问日志

​        access_log logs/nginx.test.com.access.log;

​        

​        \#一个域名下匹配多个URI的访问，使用location进行区分，后面紧跟着的/代表匹配规则

​        \#如动态资源访问和静态资源访问会分别指向不同的位置的应用场景

​        \#

​        \# 基本语法规则：location [=|~|~*|^~] /uri/ {...} 

​        \# = 开头表示精确匹配

​        \# ^~ 开头表示uri以某个常规字符串开头，匹配成功后不再进行正则匹配

​        \# ~ 开头表示区分大小写的正则匹配

​        \# ~* 开头表示不区分大小写的正则匹配

​        \# !~ 开头表示区分大小写的不匹配的正则

​        \# !~* 开头表示不区分大小写的不匹配的正则

​        \# / 通用匹配，任何请求都会被匹配到

​        \#

​        \# 理解如下：

​        \# 有两种匹配模式：普通字符串匹配，正则匹配

​        \# 无开头引导字符或以=开头表示普通字符串匹配

​        \# 以~或~*开头表示正则匹配，~*表示不区分大小写

​        \# 【多个location时，先匹配普通字符串location，再匹配正则location】

​        \# 只识别URI部分，例如请求为“/test/1/abc.do?arg=xxx”

​        \# （1）先查找是否有=开头的精确匹配，即“location=/test/1/abc.do {...}”

​        \# （2）再查找普通匹配，以“最大前缀”为规则，如有以下两个location

​        \#    location /test/ {...}

​        \#    location /test/1/ {...}

​        \#    则匹配后一项

​        \# （3）匹配到一个普通location后，搜索并未结束，而是暂存当前结果，并继续进行正则搜索

​        \# （4）在所有正则location中找到第一个匹配项后，以此匹配项为最终结果

​        \# 【所以正则匹配项，匹配规则受定义前后顺序影响，但普通匹配不会】

​        \# （5）如果未找到正则匹配项，则以（3）中缓存的结果为最终结果

​        \# （6）如果一个匹配都没有，则返回404

​        \# location =/ {...}与location / {...}的差别

​        \# 前一个是精确匹配，只响应“/”的请求，所有“/xxx”形式的请求不会以“前缀匹配形式”匹配到它

​        \# 后一个正相反，所有请求必然都是以“/”开头，所以没有其他匹配结果时一定会执行到它

​        \# location ^~ / {...} ^~的意思是禁止正则匹配，表示匹配到此项后不再进行后续的正则搜索

​        \# 相当于普通匹配模式匹配成功后就以此结果为最终结果，停止进行后续的正则匹配

​        location / {

​            \#定义服务器的默认网站根目录位置，可以写相对路径，也可以写绝对路径

​            root html;

​            \#定义首页索引文件的名称

​            index index.html index.htm;

​            \#定义转发后端负载服务器组

​            proxy_pass http://nginx.test.com;

​        }

 

​        \#定义错误提示页面

​        error_page 500 502 503 504 /50x.html;

​        location = /50x.html {

​            root html;

​        }

​        \#静态文件，nginx自己处理

​        location ~ ^/(images|javascript|js|css|flash|media|static)/{

​            root /var/www/virtual/htdocs;

​            \#过期时间1天

​            expires 1d;

​            \#关闭媒体文件日志

​            access_log off;

​            log_not_found off;

​        }

​        \#设定查看Nginx状态的地址

​        location /NginxStatus {

​            \#!stub_status on; #无此关键字

​            access_log off;

​            auth_basic "NginxStatus";

​            auth_basic_user_file conf/htpasswd;

​        }

​        \#禁止访问的文件.htxxx

​        location ~ /\.ht {

​            \#deny all;禁止访问，返回403

​            deny all;

​            \#allow all;允许访问

​        }

​    }

​    \#网站较多的情况下ngxin又不会请求瓶颈可以考虑挂多个站点，并把虚拟主机配置单独放在一个文件内，引入进来

​    \#include website.conf;

}

 