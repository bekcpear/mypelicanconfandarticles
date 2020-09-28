========================================================================================================================
启用 SELinux 的情况下，在 CentOS 上搭建 NextCloud/ownCloud 服务
========================================================================================================================

:slug: build_nextcloud_service_on_centos_with_selinux
:date: 2017-06-12 17:01
:lang: zh-Hans
:tags: service, selinux, nginx, php-fpm, installation, redis, memcache
:description: 如果你需要搭建 NextCloud 或者 ownCloud 服务，那本文是一篇非常好的参考文。
:color: #0082c9

.. contents::

因为 AWS 下的服务到期了，速度太慢也不准备继续使用，转而更换到 Google TW 线路。也准备在启用 SELinux 的情况下重新搭一下 ownCloud 服务，之后又经 `Kay`_ 推荐换搭了 NextCloud ，两者配置基本相同，少许的我发现的配置差异会在文中说明。

本次搭建同时使用 redis 作为 Transactional Locking 的数据库，并使用 APCu 作为本地 memcache 过程。

因为篇幅问题，所以肯定不可能把所有的都说的很细，主要是重点。

选择 VPS
========================================

每次选 VPS 都是一个痛苦的过程，既要保证稳定性，又要求价格合理，到大陆的速度也不能太慢.. 我个人更追求稳定，速度其次。几番比较下来，选择 Google Cloud Platform 的原因在于其家大业大比较放心，操作面板确实非常方便（除了竟然没有原生 IPv6 外），TW 机房的线路到大陆的速度也相当不错，唯一就是网络使用按流量计费，尤其到大陆价格太贵，好在我也用不了多少流量。

系统确定为 CentOS 7
========================================

原来我是打算安装 Archlinux 作为服务器系统的，没想到 Google 把计算引擎的这个系统默认镜像给砍掉了.. 我也不想自己再另外装以免玄学问题。所以就还是 CentOS 7 吧。

确定部署方案
========================================

ownCloud/NextCloud 的部署方案一般推荐都是 Nginx + PHP-FPM + Mysql/MariaDB ，这次我也准备在不关闭 SELinux 的情况下部署，同时安装 Redis 作为给 Transactional Locking 使用的数据库， APCu 用于本地 memcache。 Nginx 版本采用的是 1.12， PHP 版本采用的是 7.1，这两者都通过源码编译来安装，其中 Nginx 同时编译进 ct-nginx 模块以实现证书透明度支持。 MariaDB 则直接使用现成的官方源。

开始部署
========================================

VPS 安装
--------------------------------------------------------------------------------

Google Cloud Platform 操作很简单，选择了一个最低的配置，选择系统，确定随机/固定外网 IP，传上 ssh 公钥，打开 80 & 443 防火墙端口，点击完成后稍等片刻即可。

基本的系统设置
--------------------------------------------------------------------------------

* :code:`yum update -y` 更新一下系统
* 安装必要的工具做基本的系统配置，比如启用 fail2ban, vnstat 服务，开启防火墙的 80 & 443 端口，安装 sysstat，或者启用个 BBR 协议等。
* :code:`getenforce` 确认 SELinux 处于 Enforcing 模式下，如果不在这个模式下，先检查 :code:`/var/log/audit/audit.log` 文件下是否有拒绝什么的审计信息，也可以使用 :code:`ausearch -i -m AVC,USER_AVC,SELINUX_ERR -ts today` 命令查看，解决掉问题后输入 :code:`setenforce 1` 以设置 SELinux 到 Enforcing 模式下，并编辑 :code:`/etc/selinux/config` 文件，确认修改 :code:`SELINUX=` 值为 :code:`enforcing` ，同时运行一下 :code:`fixfiles onboot` 命令以使得下次重启后的文件拥有非错误的 SELinux 标签。以上命令都需要以 root 身份运行。注意，这边需要同时确认 SELinux 启用类型为 targeted，反正默认都是的，如果不是，参考 `Enabling MLS in SELinux`_ 反过来修改。

编译安装 Nginx 和 PHP-FPM
--------------------------------------------------------------------------------

关于这两者的编译安装，我有写过一个现成的脚本 `install nginx and php-fpm from source`_ ，不过其中就 PHP 的编译配置选项需要有针对性的配置（除却了基本的路径和用户名配置）::

  --enable-fpm \
  --with-curl \
  --with-gd \
  --enable-mbstring \
  --enable-zip \
  --with-zlib \
  --with-pdo-mysql \
  --with-bz2 \
  --enable-intl \
  --with-mcrypt \
  --with-openssl \
  --enable-exif \
  --with-gmp \
  --enable-redis \
  --enable-apcu \
  --enable-pcntl \
  --with-mysqli \
  --with-jpeg-dir \
  --with-png-dir \
  --with-xpm-dir \
  --with-webp-dir \
  --with-freetype-dir \
  --with-pear \
  --with-gettext \
  --enable-bcmath \
  --enable-sockets \
  --enable-opcache \                                                                                                   
  --enable-soap

除了脚本里面需要安装的依赖关系外，大概还需要这么几个包的存在 :code:`libwebp libwebp-devel libXpm libXpm-devel gmp gmp-devel libc-client icu libicu libicu-devel`

其中 APCu (PHP7) 以及 Redis 的启用需要另外下载包到 :code:`/path/to/php/source/code/ext` 目录下，可以参考 `PHP 官方说明文档`_ ，获取也可以在安装好之后使用 :code:`pecl` 命令来安装，不过我并没有这样子尝试，详细文档也可以在该页面找到。 

* APCu 源码包在 https://github.com/krakjoe/apcu
* Redis 源码包在 https://github.com/phpredis/phpredis/

安装 MariaDB Server
--------------------------------------------------------------------------------

请看 `Setting up MariaDB Repositories`_ 

安装 Redis
--------------------------------------------------------------------------------

:code:`yum install -y redis`

NextCloud 下载及整体配置 
--------------------------------------------------------------------------------

NextCloud 是在 ownCloud 的基础上修改演变的，关于了解其历史可以看 `History_of_the_fork`_ 。 目前的最新稳定版为 `v12.0.0`_ ，下载解压后的文件夹即充当 NextCloud web 服务主目录。 更详细的配置可以直接看 `NextCloud 官方说明文档`_ 。

配置 Nginx
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

参照 NextCloud 官方示例配置修改版在 `nginx-conf-example-for-nextcloud.conf`_ 。

  注意的是， ownCloud 的 Nginx 配置示例下因为 ETag header 的问题禁用了 gzip。

相较 NextCloud 配置示例而言，主要是添加了证书透明度和 HKPK 头的选项，关于证书透明度的配置问题，可以看 `imququ`_ 的博客， HPKP 的配置则可以看 `HTTP Public Key Pinning`_ 。针对这个我也有写了一个脚本用于获取相关必要的信息，在 `for_generating_additional_security_information_of_SSL_certificate`_ 。

配置 PHP-FPM
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* 复制源码目录下 :code:`php.ini-production` 到编译时指定的 PHP 系统配置目录下 :code:`php.ini` 
* 对 APCu 配置为启用（ :code:`apc.enable_cli` 和 :code:`apc.enable` 均设置为 :code:`1` ）。关于支持最大上传文件大小，可以尽可能配置大一点（ :code:`post_max_size` 和 :code:`upload_max_filesize` ），因为在 NextCloud 文件夹下还有配置文件可以用于限制，且支持直接在 web 控制台下修改，会在下文说明。
* 设置好用户名 用户组 日志路径等
* 在 :code:`/path/to/php-configuration_dir/php-fpm.d/www.conf` 下如果配置了监听的为 socket 文件的话，不要忘记设定正确的 :code:`listen.owner` :code:`listen.group` :code:`listen.mode` ， SELinux 的标签配置下文一起说明。 
* 取消如下几项的注释，并设置 PATH 到系统正确的值，详细原因看 `php-fpm Configuration Notes`_

::

  env[HOSTNAME] = $HOSTNAME
  env[PATH] = /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
  env[TMP] = /tmp
  env[TMPDIR] = /tmp
  env[TEMP] = /tmp

配置 MariaDB
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

并没有特别特殊的要求，我在 [mysqld] section 下设置了一个 :code:`skip-networking` 以使其只监听 socket 文件，别忘记设置 :code:`socket=/path/to/your/sock/file` 以确定你的 socket 文件路径，默认的路径可能会因为发行版的不同而不同；设置了 :code:`datadir=/path/to/your/data/dir` 以替换默认的数据库存储路径。

NextCloud 同时支持存储 emoji unicode，但是数据库表的格式需要修改，如果需要，详细的看 `Enabling MySQL 4-byte support`_ 。在这里运行 MariaDB 后创建好给 NextCloud 用的 数据库和数据库用户名。

配置 Redis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

主要注意监听地址，因为其一般是没有权限控制的，所以监听在本地 127.0.0.1 上为可。虽然也可以监听为 unix socket 文件，但是后来出了问题，详细的在下一篇问题整理里面说明。其它在这里默认配置即可。

配置 SELinux 标签和 NextCloud 下属文件权限
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**MariaDB** 因为是通过 yum 来安装的，其安装路径为默认，而预配置好的 SELinux 上下文已经包含了常用的软件了，所以默认情况下是不需要配置的。但是因为我替换了其数据文件夹的地址，所以对新的地址需要进行配置。给新路径的文件夹及其子文件（夹）配置规则设置其 SELinux 上下文类型为 :code:`mysqld_db_t` ，即（ :code:`semanage` 命令配置后不会及时生效但是会持久保存，使之生效则使用 :code:`restorecon` 命令）：

.. code-block:: bash

  semanage fcontent -a -t mysqld_db_t '/path/to/your/db/dir(/.*)?'
  restorecon -R /path/to/your/db/dir

之后别忘记检查 DAC(Discretionary Access Control) 权限配置，然后运行 :code:`mysql_install_db` 命令来安装数据库基本文件。之后就是正常的数据库/表建立了。


**Nginx 和 PHP-FPM** 因为是我从源码编译安装的，所以一个 SELinux 上下文信息都没有配置，下面说明。

SELinux 下默认对 http 服务有一系列的策略，我简单归纳为属于 httpd_t 域下，也就是说可以把 Nginx 和 PHP-FPM 配置为到 httpd_t 域下运行。而过度到这个域下所需要配置给 :code:`nginx` 和 :code:`php-fpm` 命令的 SELinux 上下文类型为 httpd_exec_t，同时也需要对相关的其它需求信息设置为 httpd_t 域可都，特定信息可写。默认配置策略下，可读的对应 SELinux 上下文类型有 httpd_sys_content_t/httpd_user_content_t、可读可写的对应 SELinux 上下文类型有 httpd_sys_rw_content_t/httpd_user_rw_content_t（或者其它），还需要给 PHP 的扩展设置脚本可执行权限，对应的 SELinux 上下文类型为 httpd_sys_script_exec_t，即：

.. code-block:: bash

  semanage fcontent -a -t httpd_exec_t /path/to/nginx/installation/dir/sbin/nginx
  semanage fcontent -a -t httpd_sys_content_t '/path/to/nginx/installation(/.*)?'
  semanage fcontent -a -t httpd_sys_content_t '/path/to/nginx/config/dir(/.*)?'
  semanage fcontent -a -t httpd_sys_rw_content_t '/path/to/nginx/log(/.*)?'

  semanage fcontent -a -t httpd_exec_t /path/to/php/installation/dir/sbin/php-fpm
  semanage fcontent -a -t httpd_sys_content_t '/path/to/php/installation(/.*)?'
  semanage fcontent -a -t httpd_sys_content_t '/path/to/php/config/dir(/.*)?'
  semanage fcontent -a -t httpd_sys_rw_content_t '/path/to/php/log(/.*)?'
  semanage fcontent -a -t httpd_sys_script_exec_t '/path/to/php/installation/lib/php/extensions(/.*)?'

  semanage fcontent -a -t var_run_t '/path/to/run/dir(/.*)?' # for nginx pid file, php-fpm pid file and its socket file

  restorecon -R /path/to/nginx/installation
  restorecon -R /path/to/nginx/config
  restorecon -R /path/to/nginx/log

  restorecon -R /path/to/php/installation
  restorecon -R /path/to/php/config
  restorecon -R /path/to/php/log

之后稍微整合一下，处理一下 DAC 权限就应该可以跑起来了。

**NextCloud** 的配置的话，主要分三个步骤：

1. 所有文件的 DAC 权限重新配置，这个有现成的 ownCloud 提供的脚本 `post-installation-steps`_ （NextCloud 下虽然没有找到，但是通用）。
2. 处理好 SELinux 的文件上下文信息，NextCloud 下有相关说明 `NextCloud SELinux Configuration`_ 。简而言之就是给整个文件夹及其子文件（夹）先设置 httpd_sys_content_t 类型，然后就需要写权限的设置 httpd_sys_rw_content_t 类型，这样子基本功能就可以用了。之后再对某些需要的功能单独启用相关设置。
3. 配置参数:

* 到这里就可以直接运行起来 NextCloud 了，所以启动了服务后，使用浏览器打开本 NextCloud 服务 web 界面，进行初始化配置，主要就是 **管理员用户名**，**管理员用户密码**，**云数据存储路径**，**数据库选择**，**数据库用户名**，**数据库用户密码**，**数据库名**，**数据库链接地址**。 其中链接地址，如果是使用的 unix socket 文件的话，格式是 :code:`localhost:/path/to/your/mysql.sock` 。如果是使用的 TCP 连接的话，注意可能需要另外配置 httpd_t 域的相关布尔值允许访问网络，尝试设置这两个布尔值或其中之一为 :code:`on` : :code:`httpd_can_network_connect/httpd_can_network_connect` ，我没有实际试验，因为我用的是 unix socket 文件，且设置了 MariaDB 不启用 TCP 监听功能，以后有机会再确认。
* 之后再手动对 :code:`/path/to/NextCloud/webroot/config/config.php` 文件进行修改，配置其本地的 memcache 为 APCu，配置 Transactional Locking 使用 Redis 作为数据库，主要添加如下内容（redis 端口号这边是默认的并没有修改）:

::

  'memcache.local' => '\\OC\\Memcache\\APCu',
  'filelocking.enabled' => true,
  'memcache.locking' => '\\OC\\Memcache\\Redis',
  'redis' =>  
  array (
    'host' => '127.0.0.1',
    'port' => 6379,
    'timeout' => 0.0,
  ),

* 注意别忘记了 /path/to/NextCloud/webroot/.user.ini 下的配置也会对 NextCloud 造成影响。

到这里所有配置基本就完成了， NextCloud 就已经搭好了。

部署完成 & 后续
========================================

之后可以查 :code:`/path/to/NextCloud/data/nextcloud.log` 这个 nextcloud 日志文件和 Nginx 以及 PHP-FPM 的日志文件来排错。 同时擅用 :code:`ausearch` 命令来解决 SELinux 的问题。

关于 NextCloud 的邮件配置，一些应用的配置，以及遇到的相关问题，在另外一篇文章内： 「 `Q&A 启用 SELinux 的情况下，在 CentOS 上搭建 NextCloud/ownCloud 服务`_ 」

以上。


.. _`Kay`: /blogroll.html#saltedfish-redl0tus-kay
.. _`Enabling MLS in SELinux`: https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/SELinux_Users_and_Administrators_Guide/mls.html#enabling-mls-in-selinux
.. _`Setting up MariaDB Repositories`: https://downloads.mariadb.org/mariadb/repositories/#mirror=tuna&distro=CentOS
.. _`install nginx and php-fpm from source`: https://github.com/Bekcpear/my-bash-scripts/tree/master/nginx_and_php-fpm_install_from_source_with_verification
.. _`PHP 官方说明文档`: https://secure.php.net/manual/zh/install.pecl.static.php
.. _`History_of_the_fork`: https://en.wikipedia.org/wiki/Nextcloud#History_of_the_fork
.. _`v12.0.0`: https://github.com/nextcloud/server/releases
.. _`NextCloud 官方说明文档`: https://docs.nextcloud.com/server/12/admin_manual/
.. _`nginx-conf-example-for-nextcloud.conf`: https://gist.github.com/Bekcpear/cfa2045ca4050238e83256ee2726bd5e
.. _`imququ`: https://imququ.com/post/certificate-transparency.html
.. _`HTTP Public Key Pinning`: https://developer.mozilla.org/en-US/docs/Web/HTTP/Public_Key_Pinning
.. _`for_generating_additional_security_information_of_SSL_certificate`: https://github.com/Bekcpear/my-bash-scripts/tree/master/for_generating_additional_security_information_of_SSL_certificate
.. _`php-fpm Configuration Notes`: https://docs.nextcloud.com/server/12/admin_manual/installation/source_installation.html#php-fpm-tips-label
.. _`Enabling MySQL 4-byte support`: https://docs.nextcloud.com/server/12/admin_manual/configuration_database/mysql_4byte_support.html
.. _`post-installation-steps`: https://doc.owncloud.org/server/10.0/admin_manual/installation/installation_wizard.html#post-installation-steps
.. _`NextCloud SELinux Configuration`: https://docs.nextcloud.com/server/12/admin_manual/installation/selinux_configuration.html
.. _`Q&A 启用 SELinux 的情况下，在 CentOS 上搭建 NextCloud/ownCloud 服务`: /q_a_build_nextcloud_service_on_centos_with_selinux.html
