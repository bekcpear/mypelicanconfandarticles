========================================================================
CentOS7通過原始碼編譯安裝Zabbix3.0（PHP+Mysql+Nginx）
========================================================================

:slug: build_zabbix_3_0_from_source_code
:lang: zht
:date: 2016-08-22 22:05
:tags: zabbix, server, installation

.. contents::

開始學習如何使用Zabbix，從最基礎的安裝做起。CentOS上預設的Zabbix是預設Apache的，且版本較低，我比較追求新版本，明明白白安裝軟體的感覺，遂自行編譯更加合適。

準備工作
------------------------------------------------------

* yum 安裝的mysql（mariadb-server），這個不多說。
* 編譯安裝的php7.0.10 和 nginx1.10

Q：如何編譯安裝php7呢？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A：難點在於編譯選項和依賴關係，整理步驟如下：

1. 下載 `PHP原始碼包 <http://cn.php.net/distributions/php-7.0.10.tar.xz>`_ 到 :code:`/usr/local/src` 目錄下，解壓後進入安裝目錄。（sha256sum：348476ff7ba8d95a1e28e1059430c10470c5f8110f6d9133d30153dda4cdf56a）
2. 使用yum安裝epel-release
3. 編譯安裝我寫了一個指令碼如下（php-fpm）：

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

Q：如何配置php並使之適合zabbix3.0.4？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A：配置專案其實很少，如下：

1. 複製啟動檔案 :code:`/usr/local/src/php-7.0.10/sapi/fpm/php-fpm.service` 到 :code:`/lib/systemd/system/php-fpm.service` ，並修改裡面的路徑到程式主目錄
2. 新建使用者php-fpm和組php-fpm
3. 兩個示例檔案 :code:`/usr/local/php/etc/php-fpm.conf.example` 和 :code:`/usr/local/php/etc/php-fpm.d/www.conf.example` ，去掉example字樣
4. 一些基本的修改不贅述了，應zabbix要求，需要在 :code:`/usr/local/php/etc/php-fpm.d/www.conf` 結尾加入如下內容，之後就可以運行了：

::

  php_value[max_execution_time] = 300
  php_value[post_max_size] = 16M
  php_value[date.timezone] = "Asia/Shanghai"

Q：如何編譯安裝nginx1.10stable？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A：這個相對來說就很簡單了，如下：

1. 下載 `Nginx原始碼包 <http://nginx.org/download/nginx-1.10.1.tar.gz>`_ 並解壓。關於校驗，官網有 `pgp檔案 <http://nginx.org/download/nginx-1.10.1.tar.gz.asc>`_ ，公鑰用 `這個 <http://nginx.org/keys/mdounin.key>`_ 。
2. 進入原始碼目錄下編譯，可能需要解決寫依賴關係：

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

Q：如何配置啟動nginx？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A：依舊是nginx配置檔案 + systemd啟動服務檔案。

1. 啟動服務檔案可以從 `nginx.com <https://www.nginx.com/resources/wiki/start/topics/examples/systemd/>`_ 上覆制：
2. 配置檔案在 :code:`/usr/local/nginx/conf/nginx.conf` ，安裝需求修改，比如針對Zabbix的一段內容，之後就可以啟動nginx了：


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

準備工作結束了，如何編譯安裝Zabbix呢？
------------------------------------------------------

其實可以參考 `官方網站 <https://www.zabbix.com/documentation/3.0/manual/installation/install#installation_from_sources>`_ 的內容，也很簡單。

整理了一下如下：

下載
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Zabbix原始碼包 <http://sourceforge.net/projects/zabbix/files/ZABBIX%20Latest%20Stable/3.0.4/zabbix-3.0.4.tar.gz/download>`_ ，解壓並進入。這個我沒有找到校驗檔案...

建立使用者
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

一般就建立一個組為zabbix的zabbix使用者即可，注意的是，當Zabbix的server和agent同時執行在一臺主機上時，推薦是將server的執行使用者獨立於agent的執行使用者的，不然agent可以訪問server的配置檔案，甚至資料庫。

建立資料庫
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

這個在原始碼包裡面有現成的指令碼，一般這樣子使用（針對我的Mysql資料庫）：

.. code-block:: mysql

  shell> mysql -uroot -p<password>
  mysql> create database zabbix character set utf8 collate utf8_bin;
  mysql> grant all privileges on zabbix.* to zabbix@localhost identified by '<password>';
  mysql> quit;
  shell> cd database/mysql
  shell> mysql -uzabbix -p<password> zabbix < schema.sql
  # 如果僅僅是執行一個agent代理的話，下面的資料庫檔案不需要匯入
  shell> mysql -uzabbix -p<password> zabbix < images.sql
  shell> mysql -uzabbix -p<password> zabbix < data.sql

配置編譯安裝
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

配置選項

::

  --prefix=/usr/local/zabbix --enable-server --enable-agent --with-mysql --enable-ipv6 --with-net-snmp --with-libcurl --with-libxml2

將安裝上server和agent兩個功能

編輯Zabbix目錄etc目錄下的配置檔案
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

因為我是在一臺機器上同時執行伺服器和代理的，所以兩個配置檔案都需要配置。這邊貼出來的刪除了大量沒有配置的選項及其註釋，但是對於已經配置的選項的註釋並沒有刪除。

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

啟動 zabbix server 和 zabbix agentd
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  # zabbix_server
  # zabbix_agentd

接下來就是安裝 Zabbix 的 Web 介面了
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

這個非常簡單，把原始碼目錄下的 :code:`frontends/php` 這個目錄整個拷貝到 nginx 配置的根目錄下，然後網頁訪問後，根據提示配置即可。注意防火牆許可權，注意複製過去後，將目錄許可權開放給 PHP 的使用者，我這裡是 php-fpm 這個使用者。不然可能無法配置成功。

配置安裝時候遇到的幾個問題
------------------------------------------------------

* "configure: error: MySQL library not found"，這個是因為沒有安裝 mariadb-devel 導致的。
* "configure: error: Invalid NET-SNMP directory - unable to find net-snmp-config"，這個是因為沒有安裝 net-snmp net-snmp-devel 導致的。
* 配置到資料庫的時候，出現"Error connecting to database: No such file or directory"，最後發現是因為 mysqli 下使用 localhost 作為地址連線 mysql 資料庫的問題，真奇怪，改成 127.0.0.1 就好了...

以上。
