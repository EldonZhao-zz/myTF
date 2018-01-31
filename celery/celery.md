# celery学习笔记

## 一、环境准备：
### 1、容器安装：
使用docker启动三个容器：

```shell
docker run -ti -d=true --name='celery-1' centos /bin/bash
docker run -ti -d=true --name='celery-2' centos /bin/bash
docker run -ti -d=true --name='celery-3' centos /bin/bash
```

### 2、RabbitMQ安装：

* 修改yum源：

```shell
vim /etc/yum.repos.d/rabbitmq_erlang.repo
```

>  
	# In /etc/yum.repos.d/rabbitmq-erlang.repo
	[rabbitmq-erlang]
	name=rabbitmq-erlang
	baseurl=https://dl.bintray.com/rabbitmq/rpm/erlang/20/el/7
	gpgcheck=1
	gpgkey=https://dl.bintray.com/rabbitmq/Keys/rabbitmq-release-signing-key.asc
	repo_gpgcheck=0
	enabled=1

* 安装rabbitmq：
	
```shell
yum search erlang
yum install erlang.x86_64 -y
rpm --import https://dl.bintray.com/rabbitmq/Keys/rabbitmq-release-signing-key.asc
wget https://dl.bintray.com/rabbitmq/all/rabbitmq-server/3.7.2/rabbitmq-server-3.7.2-1.el7.noarch.rpm
# this example assumes the CentOS 7 version of the package
yum install rabbitmq-server-3.7.2-1.el7.noarch.rpm
```

* 启动rabbitmq：

```shell
chkconfig rabbitmq-server on
rabbitmq-server -detached
```

* 查看rabbitmq信息：

```shell
[root@04dccb20f338 /]# rabbitmqctl status

  ##  ##
  ##  ##      RabbitMQ 3.7.2. Copyright (C) 2007-2017 Pivotal Software, Inc.
  ##########  Licensed under the MPL.  See http://www.rabbitmq.com/
  ######  ##
  ##########  Logs: /var/log/rabbitmq/rabbit@04dccb20f338.log
                    /var/log/rabbitmq/rabbit@04dccb20f338_upgrade.log

              Starting broker...
warning: the VM is running with native name encoding of latin1 which may cause Elixir to malfunction as it expects utf8. Please ensure your locale is set to UTF-8 (which can be verified by running "locale" in your shell)
 completed with 0 plugins.
Status of node rabbit@04dccb20f338 ...
[{pid,692},
 {running_applications,
     [{rabbit,"RabbitMQ","3.7.2"},
      {rabbit_common,
          "Modules shared by rabbitmq-server and rabbitmq-erlang-client",
          "3.7.2"},
      {ranch_proxy_protocol,"Ranch Proxy Protocol Transport","1.4.4"},
      {ranch,"Socket acceptor pool for TCP protocols.","1.4.0"},
      {ssl,"Erlang/OTP SSL application","8.2.3"},
      {public_key,"Public key infrastructure","1.5.2"},
      {asn1,"The Erlang ASN1 compiler version 5.0.4","5.0.4"},
      {inets,"INETS  CXC 138 49","6.4.5"},
      {recon,"Diagnostic tools for production use","2.3.2"},
      {os_mon,"CPO  CXC 138 46","2.4.4"},
      {mnesia,"MNESIA  CXC 138 12","4.15.3"},
      {jsx,"a streaming, evented json parsing toolkit","2.8.2"},
      {xmerl,"XML parser","1.3.16"},
      {crypto,"CRYPTO","4.2"},
      {lager,"Erlang logging framework","3.5.1"},
      {goldrush,"Erlang event stream processor","0.1.9"},
      {compiler,"ERTS  CXC 138 10","7.1.4"},
      {syntax_tools,"Syntax tools","2.1.4"},
      {sasl,"SASL  CXC 138 11","3.1.1"},
      {stdlib,"ERTS  CXC 138 10","3.4.3"},
      {kernel,"ERTS  CXC 138 10","5.4.1"}]},
 {os,{unix,linux}},
 {erlang_version,
     "Erlang/OTP 20 [erts-9.2] [source] [64-bit] [smp:2:2] [ds:2:2:10] [async-threads:64] [hipe] [kernel-poll:true]\n"},
 {memory,
     [{connection_readers,0},
      {connection_writers,0},
      {connection_channels,0},
      {connection_other,0},
      {queue_procs,0},
      {queue_slave_procs,0},
      {plugins,5864},
      {other_proc,24517672},
      {metrics,184488},
      {mgmt_db,0},
      {mnesia,73360},
      {other_ets,1847912},
      {binary,193168},
      {msg_index,45280},
      {code,24905932},
      {atom,1041593},
      {other_system,21722235},
      {allocated_unused,17147360},
      {reserved_unallocated,1294336},
      {strategy,rss},
      {total,[{erlang,74537504},{rss,92979200},{allocated,91684864}]}]},
 {alarms,[]},
 {listeners,[{clustering,25672,"::"},{amqp,5672,"::"}]},
 {vm_memory_calculation_strategy,rss},
 {vm_memory_high_watermark,0.4},
 {vm_memory_limit,838464307},
 {disk_free_limit,50000000},
 {disk_free,61833433088},
 {file_descriptors,
     [{total_limit,1048476},
      {total_used,2},
      {sockets_limit,943626},
      {sockets_used,0}]},
 {processes,[{limit,1048576},{used,201}]},
 {run_queue,0},
 {uptime,5},
 {kernel,{net_ticktime,60}}]
```

### 3、celery安装：

* pip安装：

```shell
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
```

* celery安装：

```shell
pip install celery
```

## 二、初级应用：
* 编码：

```python
from celery import Celery


app = Celery('tasks', broker='amqp://guest@172.17.0.2//')


@app.task
def add(x, y):
    return x + y
```

* 启动：

```shell
[root@04dccb20f338 celery]# celery -A tasks worker --loglevel=info &
[1] 4106
[root@04dccb20f338 celery]# /usr/lib/python2.7/site-packages/celery/platforms.py:795: RuntimeWarning: You're running the worker with superuser privileges: this is
absolutely not recommended!

Please specify a different user using the -u option.

User information: uid=0 euid=0 gid=0 egid=0

  uid=uid, euid=euid, gid=gid, egid=egid,

 -------------- celery@04dccb20f338 v4.1.0 (latentcall)
---- **** -----
--- * ***  * -- Linux-4.9.49-moby-x86_64-with-centos-7.4.1708-Core 2018-01-29 12:48:31
-- * - **** ---
- ** ---------- [config]
- ** ---------- .> app:         tasks:0x1f63050
- ** ---------- .> transport:   amqp://guest:**@localhost:5672//
- ** ---------- .> results:     disabled://
- *** --- * --- .> concurrency: 2 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** -----
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery


[tasks]
  . tasks.add

[2018-01-29 12:48:31,598: INFO/MainProcess] Connected to amqp://guest:**@127.0.0.1:5672//
[2018-01-29 12:48:31,613: INFO/MainProcess] mingle: searching for neighbors
[2018-01-29 12:48:32,652: INFO/MainProcess] mingle: all alone
[2018-01-29 12:48:32,681: INFO/MainProcess] celery@04dccb20f338 ready.
```

* 验证：

```python
Python 2.7.5 (default, Aug  4 2017, 00:39:18)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-16)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from tasks import add
>>> add.delay(4, 4)
<AsyncResult: 069f69f7-fb90-4a8a-ae6d-306c527a250f>
[2018-01-29 12:49:36,615: INFO/MainProcess] Received task: tasks.add[069f69f7-fb90-4a8a-ae6d-306c527a250f]
>>> [2018-01-29 12:49:36,617: INFO/ForkPoolWorker-2] Task tasks.add[069f69f7-fb90-4a8a-ae6d-306c527a250f] succeeded in 0.000560471999052s: 8
```

## 三、高级应用：
* 后台启动以及重启：

```shell
celery multi start w1 -A tasks -l info --pidfile=/var/run/celery/%n.pid --logfile=/var/log/celery/%n.pid
celery multi restart w1 -A tasks -l info
celery multi stop w1 -A tasks -l info
```

* 工作流：

```shell
>>> from tasks import add
>>> s1 = add.s(2, 2)
>>> type(s1)
<class 'celery.canvas.Signature'>
>>> res = s1.delay()
>>> type(res)
<class 'celery.result.AsyncResult'>
>>> res.get(0)
4
>>> s2 = add.s(5)
>>> res = s2.delay(5)
>>> res.get()
10
```

* 其他高级方法（Groups\Chains\Chords等）：

略

## 四、rabbitmq集群：
### 1、作用：
* 允许消费者和生产者在rabbitmq节点崩溃的情况下继续运行；
* 增加更多的节点来扩展消息通信的吞吐量；

### 2、集群配置方式：
* cluster：
	* 不支持跨网段，用于同一网段内的局域网；
	* 可以随意动态增加或者减少；
	* 节点之间需要运行相同版本的rabbitmq和erlang；

* federation：
	* 用于广域网；
	* 消息在联盟队列之间转发任意次，直到被消费者接受；
	* 通常用于连接internet上的中间服务器，用于订阅分发消息或工作队列；

* shovel：
	* 与federation类似；
	* 可以应用于广域网；

### 3、节点类型：
* ram node：内存节点，可以使操作更加快速；
* disk node：存储在磁盘中，单节点只允许磁盘类型的节点，防止重启时丢失系统配置信息；

### 4、Erlang Cookie：
要保证不同节点可以互相通信，必须在不同节点间共享相同的Erlang Cookie，目录为`/var/lib/rabbitmq/.erlang.cookie`。

### 5、集群模式：
* 普通模式：
* 镜像模式： 

### 6、多机多节点部署：
* 确定节点一ErlangCookie：

```shell
[root@04dccb20f338 /]# cat /var/lib/rabbitmq/.erlang.cookie
DZJDLMNUZRRWXRPNWIYE
```

* 参考之前步骤在节点二、三部署rabbitmq：

```shell
[root@04dccb20f338 /]# vim /etc/hosts
172.17.0.2	04dccb20f338
172.17.0.4	b1cb66d1b9f6
172.17.0.4	9f33aa7ce70e
```

* 设置节点二、三Erlang Cookie值以及权限：

```shell
[root@b1cb66d1b9f6 /]# vim /var/lib/rabbitmq/.erlang.cookie
[root@b1cb66d1b9f6 /]# chown rabbitmq:rabbitmq /var/lib/rabbitmq/.erlang.cookie
[root@b1cb66d1b9f6 /]# ll -a /var/lib/rabbitmq/
total 16
drwxr-xr-x 3 rabbitmq rabbitmq 4096 Jan 31 03:32 .
drwxr-xr-x 1 root     root     4096 Jan 31 03:27 ..
-rw-r--r-- 1 rabbitmq rabbitmq   21 Jan 31 03:32 .erlang.cookie
drwxr-x--- 2 rabbitmq rabbitmq 4096 Dec 23 07:00 mnesia
[root@9f33aa7ce70e tmp]# chmod 400 /var/lib/rabbitmq/.erlang.cookie
[root@9f33aa7ce70e tmp]# rabbitmq-server -detached
Warning: PID file not written; -detached was passed.
```

* 查看节点状态：

```shell
[root@b1cb66d1b9f6 /]# rabbitmqctl cluster_status
warning: the VM is running with native name encoding of latin1 which may cause Elixir to malfunction as it expects utf8. Please ensure your locale is set to UTF-8 (which can be verified by running "locale" in your shell)
Cluster status of node rabbit@b1cb66d1b9f6 ...
[{nodes,[{disc,[rabbit@b1cb66d1b9f6]}]},
 {running_nodes,[rabbit@b1cb66d1b9f6]},
 {cluster_name,<<"rabbit@b1cb66d1b9f6">>},
 {partitions,[]},
 {alarms,[{rabbit@b1cb66d1b9f6,[]}]}]
```

* 各节点加入集群：

```shell
[root@9f33aa7ce70e tmp]# rabbitmqctl stop_app
[root@9f33aa7ce70e tmp]# rabbitmqctl join_cluster rabbit@04dccb20f338
[root@9f33aa7ce70e tmp]# rabbitmqctl start_app
[root@9f33aa7ce70e tmp]# rabbitmqctl cluster_status
Cluster status of node rabbit@9f33aa7ce70e ...
[{nodes,[{disc,[rabbit@04dccb20f338,rabbit@9f33aa7ce70e,
                rabbit@b1cb66d1b9f6]}]},
 {running_nodes,[rabbit@04dccb20f338,rabbit@b1cb66d1b9f6,rabbit@9f33aa7ce70e]},
 {cluster_name,<<"rabbit@04dccb20f338">>},
 {partitions,[]},
 {alarms,[{rabbit@04dccb20f338,[]},
          {rabbit@b1cb66d1b9f6,[]},
          {rabbit@9f33aa7ce70e,[]}]}]
```

### 7、HaProxy使用：

## 参考资料：
* [Celery Docs](http://docs.jinkan.org/docs/celery/getting-started/next-steps.html)
* [RabbitMQ分布式集群架构](http://blog.csdn.net/woogeyu/article/details/51119101)
* [Rabbitmq集群高可用测试](http://www.cnblogs.com/flat_peach/archive/2013/04/07/3004008.html)
* [深度解析rabbitmq集群](http://www.iteye.com/news/31429)


