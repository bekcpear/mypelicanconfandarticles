========================================================================
CentOS7通过源码编译安装Zabbix3.0（PHP+Mysql+Nginx）
========================================================================

:slug: build_zabbix_3_0_from_source_code
:lang: zh
:date: 2016-08-22 22:05
:tags: zabbix, service, installation

.. contents::

开始学习如何使用Zabbix，从最基础的安装做起。CentOS上默认的Zabbix是默认Apache的，且版本较低，我比较追求新版本，明明白白安装软件的感觉，遂自行编译更加合适。

准备工作
------------------------------------------------------

* yum 安装的mysql（mariadb-server），这个不多说。
* 编译安装的php7.0.10 和 nginx1.10

Q：如何编译安装php7呢？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A：难点在于编译选项和依赖关系，整理步骤如下：

1. 下载 `PHP源码包 <http://cn.php.net/distributions/php-7.0.10.tar.xz>`_ 到 :code:`/usr/local/src` 目录下，解压后进入安装目录。（sha256sum：348476ff7ba8d95a1e28e1059430c10470c5f8110f6d9133d30153dda4cdf56a）
2. 使用yum安装epel-release
3. 编译安装我写了一个脚本如下（php-fpm）：

.. code-block:: bash

  #!/bin/bash
  #
  # created by Bekcpear
  # 2016-08-21 CST(China Standard Time)
  # 
  # This script is created to configuring and install php-7.0.10 from source code. 
  # When installation finished, the php installed will meet the requirments of the Laravel framework 5.2.
  # It's my first shell script, being served for my Blog with nginx.

  # update 160822 add support function for Zabbix 3.0.4

  # !Make sure you have installed mariadb-server

  # If you installed mariadb/mysql server from source code, please uncomment the line below and modify to correct path to mysql/mariadb. This is wrong. Ignore it.
  # CUS_MYSQLPATH = /usr/local/mysql

  CONF="--prefix=/usr/local/php/ \
    --enable-fpm \
    --with-config-file-path=/usr/local/php/etc \
    --with-fpm-user=php-fpm \
    --with-fpm-group=php-fpm \
    --with-mysql-sock=/var/run/mysql.sock \
    --with-mysqli \
    --with-libxml-dir \
    --with-gd \
    --with-jpeg-dir \
    --with-png-dir \
    --with-freetype-dir \
    --with-iconv-dir \
    --with-zlib-dir \
    --with-mcrypt \
    --with-curl \
    --with-pear \
    --with-gettext \
    --enable-bcmath \
    --enable-sockets \
    --enable-soap \
    --enable-gd-native-ttf \
    --enable-ftp \
    --enable-exif \
    --enable-tokenizer \
    --with-pdo-mysql \
    --enable-mbstring \
    --with-openssl"   
  CONF_0=" --with-pdo-mysql"
  CONF_1=" --with-pdo-mysql="$CUS_MYSQLPATH
  # last 4 parameters are needed by Laravel

  if [ -z $CUS_MYSQLPATH ]; then
    CONF=$CONF$CONF_0;
  else
    CONF=$CONF$CONF_1;
  fi


  # Please install epel-release first.
  PREBUILD="\
    gcc \
    libxml2 \
    libxml2-devel \
    openssl \
    openssl-devel \
    bzip2 \
    bzip2-devel \
    libjpeg \
    libjpeg-devel \
    libpng \
    libpng-devel \
    gettext \
    gettext-devel \
    freetype \
    freetype-devel \
    libmcrypt \
    libmcrypt-devel \
    libcurl \
    libcurl-devel"

  yum install -y $PREBUILD;

  if [ $? -eq 0 ];then
    ./configure $CONF && make && make install
  fi

Q：如何配置php并使之适合zabbix3.0.4？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A：配置项目其实很少，如下：

1. 复制启动文件 :code:`/usr/local/src/php-7.0.10/sapi/fpm/php-fpm.service` 到 :code:`/lib/systemd/system/php-fpm.service` ，并修改里面的路径到程序主目录
2. 新建用户php-fpm和组php-fpm
3. 两个示例文件 :code:`/usr/local/php/etc/php-fpm.conf.example` 和 :code:`/usr/local/php/etc/php-fpm.d/www.conf.example` ，去掉example字样
4. 一些基本的修改不赘述了，应zabbix要求，需要在 :code:`/usr/local/php/etc/php-fpm.d/www.conf` 结尾加入如下内容，之后就可以运行了：

::

  php_value[max_execution_time] = 300
  php_value[post_max_size] = 16M
  php_value[date.timezone] = "Asia/Shanghai"

Q：如何编译安装nginx1.10stable？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A：这个相对来说就很简单了，如下：

1. 下载 `Nginx源码包 <http://nginx.org/download/nginx-1.10.1.tar.gz>`_ 并解压。关于校验，官网有 `pgp文件 <http://nginx.org/download/nginx-1.10.1.tar.gz.asc>`_ ，公钥用 `这个 <http://nginx.org/keys/mdounin.key>`_ 。
2. 进入源码目录下编译，可能需要解决写依赖关系：

::

  CUS_CONF="\
    --prefix=/usr/local/nginx/ \
    --with-http_realip_module \
    --with-http_sub_module \
    --with-http_gzip_static_module \
    --with-http_stub_status_module \
    --with-http_ssl_module \
    --with-pcre"

  ./configure $CUS_CONF && make && make install

Q：如何配置启动nginx？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A：依旧是nginx配置文件 + systemd启动服务文件。

1. 启动服务文件可以从 `nginx.com <https://www.nginx.com/resources/wiki/start/topics/examples/systemd/>`_ 上复制：
2. 配置文件在 :code:`/usr/local/nginx/conf/nginx.conf` ，安装需求修改，比如针对Zabbix的一段内容，之后就可以启动nginx了：


.. code-block:: nginx

  server {
      listen 8080;

      access_log  /usr/local/nginx/logs/1.access.log  main;
      error_log  /usr/local/nginx/logs/1.error.log;
      root   /home/html/1;

      location / {
          index index.php index.html;
      }

      #error_page  404              /404.html;

      # redirect server error pages to the static page /50x.html
      #
      error_page   500 502 503 504  /50x.html;
      location = /50x.html {
          root   /usr/local/nginx/html;
      }

      # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
      #
      location ~ \.php$ {
          fastcgi_pass   127.0.0.1:9000;
          fastcgi_param  SCRIPT_FILENAME $document_root$fastcgi_script_name;
          include        fastcgi_params;
      }
  }

准备工作结束了，如何编译安装Zabbix呢？
------------------------------------------------------

其实可以参考 `官方网站 <https://www.zabbix.com/documentation/3.0/manual/installation/install#installation_from_sources>`_ 的内容，也很简单。

整理了一下如下：

下载
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Zabbix源码包 <http://sourceforge.net/projects/zabbix/files/ZABBIX%20Latest%20Stable/3.0.4/zabbix-3.0.4.tar.gz/download>`_ ，解压并进入。这个我没有找到校验文件...

创建用户
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

一般就创建一个组为zabbix的zabbix用户即可，注意的是，当Zabbix的server和agent同时运行在一台主机上时，推荐是将server的运行用户独立于agent的运行用户的，不然agent可以访问server的配置文件，甚至数据库。

创建数据库
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

这个在源码包里面有现成的脚本，一般这样子使用（针对我的Mysql数据库）：

.. code-block:: mysql

  shell> mysql -uroot -p<password>
  mysql> create database zabbix character set utf8 collate utf8_bin;
  mysql> grant all privileges on zabbix.* to zabbix@localhost identified by '<password>';
  mysql> quit;
  shell> cd database/mysql
  shell> mysql -uzabbix -p<password> zabbix < schema.sql
  # 如果仅仅是运行一个agent代理的话，下面的数据库文件不需要导入
  shell> mysql -uzabbix -p<password> zabbix < images.sql
  shell> mysql -uzabbix -p<password> zabbix < data.sql

配置编译安装
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

配置选项

::

  --prefix=/usr/local/zabbix --enable-server --enable-agent --with-mysql --enable-ipv6 --with-net-snmp --with-libcurl --with-libxml2

将安装上server和agent两个功能

编辑Zabbix目录etc目录下的配置文件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

因为我是在一台机器上同时运行服务器和代理的，所以两个配置文件都需要配置。这边贴出来的删除了大量没有配置的选项及其注释，但是对于已经配置的选项的注释并没有删除。

::

  ##/usr/local/zabbix/etc/zabbix_agentd.conf
  # This is a configuration file for Zabbix agent daemon (Unix)
  # To get more information about Zabbix, visit http://www.zabbix.com

  ############ GENERAL PARAMETERS #################

  ### Option: PidFile
  #	Name of PID file.
  #
  # Mandatory: no
  # Default:
  PidFile=/tmp/zabbix_agentd.pid

  ### Option: LogFile
  #	Log file name for LogType 'file' parameter.
  #
  # Mandatory: no
  # Default:
  # LogFile=

  LogFile=/var/log/zabbix/zabbix_agentd.log

  ### Option: LogFileSize
  #	Maximum size of log file in MB.
  #	0 - disable automatic log rotation.
  #
  # Mandatory: no
  # Range: 0-1024
  # Default:
  LogFileSize=5

  ### Option: Server
  #	List of comma delimited IP addresses (or hostnames) of Zabbix servers.
  #	Incoming connections will be accepted only from the hosts listed here.
  #	If IPv6 support is enabled then '127.0.0.1', '::127.0.0.1', '::ffff:127.0.0.1' are treated equally.
  #
  # Mandatory: no
  # Default:
  # Server=

  Server=127.0.0.1

  ### Option: ListenPort
  #	Agent will listen on this port for connections from the server.
  #
  # Mandatory: no
  # Range: 1024-32767
  # Default:
  ListenPort=10050

  ### Option: ListenIP
  #	List of comma delimited IP addresses that the agent should listen on.
  #	First IP address is sent to Zabbix server if connecting to it to retrieve list of active checks.
  #
  # Mandatory: no
  # Default:
  ListenIP=127.0.0.1

  ### Option: ServerActive
  #	List of comma delimited IP:port (or hostname:port) pairs of Zabbix servers for active checks.
  #	If port is not specified, default port is used.
  #	IPv6 addresses must be enclosed in square brackets if port for that host is specified.
  #	If port is not specified, square brackets for IPv6 addresses are optional.
  #	If this parameter is not specified, active checks are disabled.
  #	Example: ServerActive=127.0.0.1:20051,zabbix.domain,[::1]:30051,::1,[12fc::1]
  #
  # Mandatory: no
  # Default:
  # ServerActive=

  ServerActive=127.0.0.1:10051

  ### Option: Hostname
  #	Unique, case sensitive hostname.
  #	Required for active checks and must match hostname as configured on the server.
  #	Value is acquired from HostnameItem if undefined.
  #
  # Mandatory: no
  # Default:
  # Hostname=

  Hostname=your hostname

  ### Option: AllowRoot
  #	Allow the agent to run as 'root'. If disabled and the agent is started by 'root', the agent
  #	will try to switch to the user specified by the User configuration option instead.
  #	Has no effect if started under a regular user.
  #	0 - do not allow
  #	1 - allow
  #
  # Mandatory: no
  # Default:
  # AllowRoot=0

  ### Option: User
  #	Drop privileges to a specific, existing user on the system.
  #	Only has effect if run as 'root' and AllowRoot is disabled.
  #
  # Mandatory: no
  # Default:
  User=zabbix-agent

  ##/usr/local/zabbix/etc/zabbix_server.conf
  # This is a configuration file for Zabbix server daemon
  # To get more information about Zabbix, visit http://www.zabbix.com

  ############ GENERAL PARAMETERS #################

  ### Option: ListenPort
  #	Listen port for trapper.
  #
  # Mandatory: no
  # Range: 1024-32767
  # Default:
  ListenPort=10051

  ### Option: LogFile
  #	Log file name for LogType 'file' parameter.
  #
  # Mandatory: no
  # Default:
  # LogFile=

  LogFile=/var/log/zabbix/zabbix_server.log

  ### Option: LogFileSize
  #	Maximum size of log file in MB.
  #	0 - disable automatic log rotation.
  #
  # Mandatory: no
  # Range: 0-1024
  # Default:
  LogFileSize=5

  ### Option: PidFile
  #	Name of PID file.
  #
  # Mandatory: no
  # Default:
  PidFile=/tmp/zabbix_server.pid

  ### Option: DBName
  #	Database name.
  #	For SQLite3 path to database file must be provided. DBUser and DBPassword are ignored.
  #
  # Mandatory: yes
  # Default:
  # DBName=

  DBName=zabbix

  ### Option: DBUser
  #	Database user. Ignored for SQLite.
  #
  # Mandatory: no
  # Default:
  # DBUser=

  DBUser=zabbix

  ### Option: DBPassword
  #	Database password. Ignored for SQLite.
  #	Comment this line if no password is used.
  #
  # Mandatory: no
  # Default:
  DBPassword=passwd

  ### Option: DBSocket
  #	Path to MySQL socket.
  #
  # Mandatory: no
  # Default:
  DBSocket=/var/lib/mysql/mysql.sock

  ### Option: DBPort
  #	Database port when not using local socket. Ignored for SQLite.
  #
  # Mandatory: no
  # Range: 1024-65535
  # Default (for MySQL):
  DBPort=3306

  ############ ADVANCED PARAMETERS ################

  ### Option: ListenIP
  #	List of comma delimited IP addresses that the trapper should listen on.
  #	Trapper will listen on all network interfaces if this parameter is missing.
  #
  # Mandatory: no
  # Default:
  # ListenIP=0.0.0.0

  ListenIP=127.0.0.1

  ### Option: Timeout
  #	Specifies how long we wait for agent, SNMP device or external check (in seconds).
  #
  # Mandatory: no
  # Range: 1-30
  # Default:
  # Timeout=3

  Timeout=4

  ### Option: LogSlowQueries
  #	How long a database query may take before being logged (in milliseconds).
  #	Only works if DebugLevel set to 3, 4 or 5.
  #	0 - don't log slow queries.
  #
  # Mandatory: no
  # Range: 1-3600000
  # Default:
  # LogSlowQueries=0

  LogSlowQueries=3000

  ### Option: AllowRoot
  #	Allow the server to run as 'root'. If disabled and the server is started by 'root', the server
  #	will try to switch to the user specified by the User configuration option instead.
  #	Has no effect if started under a regular user.
  #	0 - do not allow
  #	1 - allow
  #
  # Mandatory: no
  # Default:
  # AllowRoot=0

  ### Option: User
  #	Drop privileges to a specific, existing user on the system.
  #	Only has effect if run as 'root' and AllowRoot is disabled.
  #
  # Mandatory: no
  # Default:
  User=zabbix

启动 zabbix server 和 zabbix agentd
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  # zabbix_server
  # zabbix_agentd

接下来就是安装 Zabbix 的 Web 接口了
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

这个非常简单，把源码目录下的 :code:`frontends/php` 这个目录整个拷贝到 nginx 配置的根目录下，然后网页访问后，根据提示配置即可。注意防火墙权限，注意复制过去后，将目录权限开放给 PHP 的用户，我这里是 php-fpm 这个用户。不然可能无法配置成功。

配置安装时候遇到的几个问题
------------------------------------------------------

* "configure: error: MySQL library not found"，这个是因为没有安装 mariadb-devel 导致的。
* "configure: error: Invalid NET-SNMP directory - unable to find net-snmp-config"，这个是因为没有安装 net-snmp net-snmp-devel 导致的。
* 配置到数据库的时候，出现"Error connecting to database: No such file or directory"，最后发现是因为 mysqli 下使用 localhost 作为地址连接 mysql 数据库的问题，真奇怪，改成 127.0.0.1 就好了...

以上。
