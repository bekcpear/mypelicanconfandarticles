========================================================================================================================
Q&A 启用 SELinux 的情况下，在 CentOS 上搭建 NextCloud/ownCloud 服务
========================================================================================================================

:slug: q_a_build_nextcloud_service_on_centos_with_selinux
:date: 2017-06-12 21:21
:modified: 2017-07-10 08:28
:tags: service, selinux, nginx, php-fpm, installation, redis, memcache, Q&A
:description: 整理了我在安装 NextCloud / ownCloud 服务时候遇到的各种问题，非常具有参考价值。

.. contents::

本文记录了我在部署 ownCloud/NextCloud 时所遇到的问题，处理思路以及解决方案。

Q: 安装 ownCloud 后不断出现 SELinux 审计拒绝信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

不断出现类似这样子的审计信息: 

::

  type=PROCTITLE msg=audit(05/27/2017 00:26:03.559:129906) : proctitle=find /usr/local/bin /usr/bin /bin -name sendmail
  type=SYSCALL msg=audit(05/27/2017 00:26:03.559:129906) : arch=x86_64 syscall=newfstatat success=no exit=EACCES(Permission denied) a0=0x9 a1=0x19baf08 a2=0x7fff31a85990 a3=0x100 items=0 ppid=28746 pid=28747 auid=unset uid=php-fpm gid=www euid=php-fpm suid=php-fpm fsuid=php-fpm egid=www sgid=www fsgid=www tty=(none) ses=unset comm=find exe=/usr/bin/find subj=system_u:system_r:httpd_t:s0 key=(null)
  type=AVC msg=audit(05/27/2017 00:26:03.559:129906) : avc:  denied  { getattr } for  pid=28747 comm=find path=/usr/bin/redis-server dev="sda1" ino=248278 scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:object_r:redis_exec_t:s0 tclass=file permissive=0

还会出现类似上述的一个会出现使用 find 查找 smbclient 被审计拒绝的信息，这两个问题都是在访问 ownCloud 设置页面时所碰到的。即使我把发送邮件改为 smtp 后依旧有这个问题。

**A:** 感觉可能是在一开始安装 owncloud 过程中因为某些文件的权限没有配置好而导致的文件丢失引起了，隧重新安装了一下，并将 PHP-FPM 配置文件 :code:`www.conf` 下的 :code:`env[PATH]` 的默认配置改成了针对当前系统环境的 :code:`/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin` 后问题解决，应该是后者配置不当引起的。

Q: 在 ownCloud 的管理员设置界面，无法编辑 Email Template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

选择了模板后，出现访问 :code:`https://c.ume.ink/apps/templateeditor/settings/mailtemplate?theme=&template=core%2Ftemplates%2Fmail.php 403` 报错，单独访问后发现是 :code:`Access forbidden` 和 :code:`CSRF check failed` 。 在禁用了 CSRF 检查后依旧有 Access forbidden 的报错。

这个链接实际经过 nginx 配置重写后应该为 :code:`https://c.ume.ink/index.php/apps/templateeditor/settings/mailtemplate?theme=&template=core%2Ftemplates%2Fmail.php` 。 类似这个 issue https://github.com/owncloud/core/issues/27628 ，等待更新后再看。


Q: 提醒刷新请求日志文件太多
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**A:** nginx 访问日志会记录 :code:`https://c.ume.ink//ocs/v2.php/apps/notifications/api/v1/notifications?format=json` 这个每隔 10 秒的提醒刷新请求，通过在 

.. code-block:: nginx

  location ~ ^/(?:index|remote|public|cron|core/ajax/update|status|ocs/v[12]|updater/.+|ocs-provider/.+|core/templates/40[34])\.php(?:$|/) {
    ...
  }

块中添加如下后解决:

.. code-block:: nginx

  if ($fastcgi_path_info = /apps/notifications/api/v1/notifications) {
    access_log off;
  } 

.. _`Q: smtp 发信失败，提示连接到 smtp.mailgun.org 超时，无 SELinux 审计相关信息`:

Q: smtp 发信失败，提示连接到 smtp.mailgun.org 超时，无 SELinux 审计相关信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

通过 tcpdump 抓包后发现在与 :code:`smtp.mailgun.org` 握手时，只有从本地服务器发送出去的 SYN 包，迟迟收不到 ACK 从而导致的超时。即使关闭了防火墙也是一样的效果，替换 mailgun 端口 25/465/587 都无效，怀疑 mailgun 对 Google Cloud 某些 IP 进行了屏蔽。

同时看到 GCP 也对虚拟机的默认 smtp 端口有限制，详细看 https://cloud.google.com/compute/docs/tutorials/sending-mail/ 。

关于 sendmail，其实当前环境是没有安装的，sendmail 这个命令是调用了 postfix 的功能，而 postfix 是 sendmail 的一个替代品，继承了 sendmail 的命令和参数。GCP 对默认的 smtp 端口进行了禁用处理因为出现了大量对该类端口滥用的情况。可以通过第三方的邮件服务上来发送邮件，比如 SendGrid/Mailgun./Mailjet ，如果需要用到自己企业内部的发信服务，那就需要利用 VPN 来解决了。比如针对 Mailgun 的配置可以看 https://cloud.google.com/compute/docs/tutorials/sending-mail/using-mailgun ，**A: 通过如上配置，最后也成功使用 php 模式发信了。**

Q: Redis 无法使用 unix socket 文件与 PHP-FPM 通讯
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

这是一个暂时不想去解决的问题，原来是想使用 unix domain socket 文件来使得 php-fpm 与 redis 之间进行通讯的，但是目前给 php-fpm  使用的限制性域类为 :code:`httpd_t` ，而 redis 的则为 :code:`redis_t` ， :code:`httpd_t` 完全没有可以对 :code:`redis_t` 所对应的目前文件 type 有读写权限的默认规则，比如一般 redis 的 socket 文件是标记为 :code:`redis_var_run_t` ，但是 :code:`httpd_t` 没有对其的默认规则。同时， :code:`redis_t` 域运行的进程没有对非 :code:`redis_` 前缀的文件/文件夹有读写权限，所以也没有办法生成为 :code:`var_run_t` 类型的 redis.sock 文件。

**A:** 在不新建规则的情况下，替换使用 tcp socket 即可。但是替换使用了 tcp socket 后，默认出现了 :code:`httpd_t` 对 :code:`redis_port_t` 的 name_connect denied，设置：

.. code-block:: bash

  setsebool -P httpd_can_network_connect on

后解决。

Q: Redis systemd 服务脚本无法启动，错误信息为无法停止服务
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Redis 在改动为不进行 tcp 端口监听后，出现默认脚本无法启动的问题，总是提示无法停止服务，有点迷。后查得原因是因为使用了 :code:`/usr/bin/redis-shutdown` 来作为停止服务的命令，而这个命令默认是使用 6379 端口来与 redis 服务通讯并通知其停止服务的，在改为了 unix domain socket 文件通讯并关闭了 tcp socket 后出现连接 refuse 而导致报错，从而导致服务脚本执行异常。

**A:** 解决方法是写一个单独的 bash 脚本，然后使用 :code:`/usr/bin/redis-cli` 来指定为 unix domain socket 文件通讯，并传递 shutdown 操作，以这个 bash 脚本作为 systemd 服务文件的停止命令即可。

*注意， systemd 服务启动 redis 不能使用 redis 的 daemon 模式，不然会出现奇怪的问题，暂时不知道原因，不过先跳过。*


Q: ownCloud 建议的使用系统的 crond 计划任务执行失败
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

这个是每隔 15 分钟执行一遍 :code:`/path/to/owncloud/cron.php` 以实现定时检查的功能。我也根据提示并通过命令 :code:`crontab -u php-fpm -e` 打开并添加了 :code:`*/15  *  *  *  * /opt/local/php/bin/php -f /path/to/owncloud/cron.php` ，但是就是不执行，php-fpm 的组用户为 www， :code:`/opt/local/php/bin/php` 文件是可以被 php-fpm 读取并执行的，其 SELinux type 为 :code:`httpd_exec_t` ， :code:`/path/to/owncloud/cron.php`  所对应的目录权限为 750 目录组为 www，文件权限为 640 ，文件组为 www，后查看日志报错为 :code:`(CRON) ERROR chdir failed (/home/php-fpm): No such file or directory` 。

**A:** 建立 php-fpm 家目录，修改权限，SELinux content type 改为 :code:`httpd_sys_rw_content_t` 后解决


Q: SELinux 拒绝 execmem 操作
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

一开始安装好并打开 owncloud 主页后出现了

::

  type=AVC msg=audit(1495804058.069:129092): avc:  denied  { execmem } for  pid=26255 comm="php-fpm" scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:system_r:httpd_t:s0 tclass=process permissive=0

**A:** 虽然通过 :code:`setsebool -P httpd_execmem on` 解决了，但是还是应该去看看这个报 https://bugzilla.redhat.com/show_bug.cgi?id=1380930 的 bug 以获取更详尽的信息，不止一种解决方法。也和 php 的 jit 启用与否有关。

Q: 大量国际化报错信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

最开始安装 PHP 的时候，很多模块没有装好，其中 **intl 的没有装好** 导致了大量 :code:`You are using a fallback implementation of the intl extension. Installing the native one is highly recommended instead.` 这个报错信息出现在 owncloud.log 文件中，关于 owncloud 所需要的 PHP 模块可以看 ownCloud 的说明 `prerequisites-label`_ ，我对其稍作整理了一下: `owncloudPHPExtensions.txt`_

Q: 启用 imap 情况下编译 PHP 报错
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在编译 PHP 的时候，当启用了 imap 的情况下，会出现 :code:`utf8_mime2text() has new signature, but U8T_CANONICAL is missing. This should not happen.` 这个报错，使用 yum 安装了 libc-client 后也没有用，且在 CentOS 7 下没有查到 libc-client-devel 包很奇怪，看网上有人说还需要编译安装 imap-2007f 的包，感觉是不是太旧了，而且 imap 的需求仅仅在用需要集成 imap app 的情况下才会用到，暂时就不去理会，去掉了这个模块。

Q: 启用了 APCu 下编译 PHP 报 apc_arginfo.h 文件缺失
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**A:** PHP 7 是有单独的 acpu 模块包的，看官方文档 https://secure.php.net/manual/en/apcu.installation.php 上写了可以在 pecl 档案库下载，但是实际使用后发现缺失文件，报 apc_arginfo.h 文件没有，所以直接从 github 下载并解压后到 PHPSRCROOT/ext  下后编译安装，相关说明可以看 https://secure.php.net/manual/en/install.pecl.static.php

Q: 使用 sendmail 方式发送邮件报错
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

「相关问题」继问题 `Q: smtp 发信失败，提示连接到 smtp.mailgun.org 超时，无 SELinux 审计相关信息`_ 重新安装后，还需要的其它一些问题，解决方案直接看上文。

1. 设置里的 Mail Server 的 send mode 多了一个 sendmail 选项，选择其发送测试邮件出现  :code:`(Error: Expected response code 220 but got code "", with message "")` 报错，SELinux 规则审计为：

::

  type=PROCTITLE msg=audit(05/27/2017 13:03:35.266:131989) : proctitle=/usr/sbin/sendmail -bs
  type=SYSCALL msg=audit(05/27/2017 13:03:35.266:131989) : arch=x86_64 syscall=open success=no exit=EACCES(Permission denied) a0=0x55a1c79309e0 a1=O_RDONLY a2=0x0 a3=0x3 items=0 ppid=26861 pid=26866 auid=unset uid=php-fpm gid=www euid=php-fpm suid=php-fpm fsuid=php-fpm egid=www sgid=www fsgid=www tty=(none) ses=unset comm=sendmail exe=/usr/sbin/sendmail.postfix subj=system_u:system_r:httpd_t:s0 key=(null)
  type=AVC msg=audit(05/27/2017 13:03:35.266:131989) : avc:  denied  { read } for  pid=26866 comm=sendmail name=main.cf dev="sda1" ino=17007198 scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:object_r:postfix_etc_t:s0 tclass=file permissive=0 

目前认为这个是 SELinux 的规则配置问题，改 php 模式可以发送成功，不再另行配置。

2. 改用 PHP 模式发送邮件，在 SELinux 设置了 httpd_can_sendmail 为 on 后不再出现 :code:`avc:  denied  { read } for  pid=27097 comm=sendmail name=main.cf` 报错，但是收不到消息，是服务器的 postfix 服务没有启用，且配置不正确导致的.

3. 改用 sendmail 模式发送邮件，即使 SELinux 设置了 :code:`httpd_can_sendmail 为 on`，却依旧出现了：

::

  type=PROCTITLE msg=audit(05/27/2017 13:49:02.605:132083) : proctitle=/usr/sbin/sendmail -bs
  type=SYSCALL msg=audit(05/27/2017 13:49:02.605:132083) : arch=x86_64 syscall=execve success=no exit=EACCES(Permission denied) a0=0x55d80dc4a7e0 a1=0x55d80dc4a780 a2=0x55d80dc4ec40 a3=0x4 items=0 ppid=26738 pid=27266 auid=unset uid=php-fpm gid=www euid=php-fpm suid=php-fpm fsuid=php-fpm egid=www sgid=www fsgid=www tty=(none) ses=unset comm=sendmail exe=/usr/sbin/sendmail.postfix subj=system_u:system_r:system_mail_t:s0 key=(null)
  type=AVC msg=audit(05/27/2017 13:49:02.605:132083) : avc:  denied  { execute } for  pid=27266 comm=sendmail name=smtpd dev="sda1" ino=34131935 scontext=system_u:system_r:system_mail_t:s0 tcontext=system_u:object_r:postfix_smtpd_exec_t:s0 tclass=file permissive=0

的报错，怀疑是 postfix 设置问题。

Q: 替换 NextCloud 后，设置界面提示 PHP Opcache 配置不正确
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

替换为 nextcloud 正常配置后，设置界面提示 :code:`The PHP Opcache is not properly configured. For better performance we recommend ↗ https://docs.nextcloud.com/server/12/go.php?to=admin-php-opcache  to use following settings in the php.ini: opcache.enable=1 opcache.enable_cli=1 opcache.interned_strings_buffer=8 opcache.max_accelerated_files=10000 opcache.memory_consumption=128 opcache.save_comments=1 opcache.revalidate_freq=1` ，但是设置了也启用了 opcache 后，依旧有这样子的提示，phpinfo() 也看不到 opcache 的参数，但是 :code:`php-fpm -v` 可以看到已经有启用了 opcache 的了。

查找了 php 官方说明发现如果编译时候使用了 --disable-all 禁用了默认的扩展的话，需要使用 --enable-opcache 来启用 opcache 的支持，但是我并没有禁用，不过还是添加了这个参数后重新编译试了一下，但是并没有效果。

**A:** 最后发现是 selinux 标签配置不当。我之前检查了 audit 日志，但是并没有相关报错提示，最后发现在 systemd 日志下有一个权限错误 :code:`failed to map segment from shared	object: Permission denied` ，临时把 selinux 改成 permissive mode 后重启 php-fpm 就一切正常了。多次尝试下，是 :code:`httpd_t` 类域下进程缺少对 :code:`opcache.so` 文件的 execute 权限，给 :code:`PHPLOCAL/lib/php/extensions` 目录统一改 selinux 标签为 :code:`httpd_sys_script_exec_t` 后，恢复为 enforcing mode 再重启 php-fpm 一切正常。

Q: NextCloud 下即使配置了 X-Frame-Option 但是依旧提示为配置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

明明 nginx 配置文件下已经添加了 X-Frame-Option 的头为  SAMEORIGIN 但是依旧出现了这个提示 :code:`The "X-Frame-Options" HTTP header is not configured to equal to "SAMEORIGIN". This is a potential security or privacy risk and we recommend adjusting this setting.` 

**A:** 需要从 Nginx 配置中移除改选项，详细的看 https://github.com/nextcloud/server/issues/4764 和 https://docs.nextcloud.com/server/12/admin_manual/release_notes.html 


Q: NextCloud 预览视频文件报错
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NextCloud 预览视频文件报错 :code:`Uncaught ReferenceError: videojs is not defined  at Object.show (viewer.js?v=3bdb93f…-0:39)  at Object.<anonymous> (viewer.js?v=3bdb93f…-0:82)  at Object.<anonymous> (core.js?v=3bdb93f…-0:2) ...`

**A:** 已经有解决方案，看这里: https://github.com/nextcloud/files_videoplayer/pull/26/commits/37c2866e319e0e8ff1b2f70da3a1d8c7cd21697b 。但是会导致改视频预览 app 的签名文件异常，因为我没有作者的私钥，所以也没有办法，自己签也不可以，因为需要由 nextCloud 来发证书，而 app 并不是我的。 nextCloud 与 ownCloud 有一个区别是对于 app 的签名文件，当签名 hash 与文件不匹配时，nextCloud 并不会提示，而 ownCloud 会。

Q: 检查 NextCloud 日志发现提示 APCu 不可用
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

检查 nextCloud 日志发现提示信息::

  Memcache \OC\Memcache\APCu not available for local cache Memcache \OC\Memcache\APCu not available for distributed cache

在每 15 分钟一次的计划任务执行后生成。

**A:** 最后排查发现是因为虽然编译进了 apcu 但是配置并没有启用，在 php.ini 中加入 :code:`apc.enabled=1` 和 :code:`apc.enable_cli=1` 后即可

Q: NextCloud 上传文件时， FileHooks.php 报错
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NextCloud 上传文件时经常性出现 :code:`Undefined offset: 3 at /data/0/www/nextcloud/apps/activity/lib/FilesHooks.php#620` 报错，系 bug 在此 https://github.com/nextcloud/server/issues/4971 ，临时解决方法： https://github.com/nextcloud/activity/pull/156/commits/0b627d63349d035c0282f0984f7e2519d6ec57b3 


Q: 在每次使用 cron 执行 cron.php 时出现的一个 SELinux 拒绝审计信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在每次使用 cron 执行 cron.php 时出现的一个 SELinux 拒绝审计信息

::

  type=PROCTITLE msg=audit(05/29/2017 02:00:03.782:137263) : proctitle=local -t unix
  type=SYSCALL msg=audit(05/29/2017 02:00:03.782:137263) : arch=x86_64 syscall=lstat success=no exit=EACCES(Permission denied) a0=0x55fd699c9080 a1=0x7fff3971e260 a2=0x7fff3971e260 a3=0x7f1c14c362e0 items=0 ppid=31757 pid=18374 auid=unset uid=root gid=root euid=php-fpm suid=root fsuid=php-fpm egid=www sgid=root fsgid=www tty=(none) ses=unset comm=local exe=/usr/libexec/postfix/local subj=system_u:system_r:postfix_local_t:s0 key=(null)
  type=AVC msg=audit(05/29/2017 02:00:03.782:137263) : avc:  denied  { search } for  pid=18374 comm=local name=php-fpm dev="sda1" ino=37082976 scontext=system_u:system_r:postfix_local_t:s0 tcontext=unconfined_u:object_r:httpd_sys_rw_content_t:s0 tclass=dir permissive=0 
  
最后发现是在 php.ini 下配置了错误的 zend_extension 而导致在执行 cron 时去做了默认情况下不允许做的操作而被审计了，在 journal 和 /var/mail/php-fpm 下都可以看到，相关错误信息为 :code:`/opt/local/php/lib/php/extensions/no-debug-non-zts-20160303/apcu.so doesn't appear to be a valid Zend extension` 。 这个其实我有点迷，因为我在编译时其实已经编译进了 apcu 了，但是后来捣鼓的时候又使用 pecl 安装了一个，有机会再继续就这个问题分析吧。

Q: 客户端每次都需要输入密码，报错 No keychain service available
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在 Gentoo 上 AwesomeWM 下使用 NextCloud 客户端，每次打开都会提示 :code:`No keychain service available` ，顾名思义是 keychain 的问题。

安装上了 kwalletd 后提示信息出现了区别 :code:`Failed to execute program org.kde.kwalletd: No such file or directory` 。单独运行 kwalletd5 也是一样的问题。

后看到 archwiki 上有一个说明:  https://wiki.archlinux.org/index.php/Nextcloud#.22Reading_from_keychain_failed_with_error:_.27No_keychain_service_available.27.22 。东西我是已经装好了，再根据 gentoowiki 上 SLiM（我当前用的 DM） 自动解锁 gnome-keyring 配置好后 https://wiki.gentoo.org/wiki/SLiM#Unlock_keyrings，重新登录试试，无效。

在 https://wiki.gnome.org/Projects/GnomeKeyring/Pam  https://wiki.gentoo.org/wiki/SLiM#Unlock_keyrings 上有写关于 gnome-keyring 的设置，因为我的不是 Gnome，是 SLiM 这个 DM，一般建议是 gnome-keyring-daemon 随登录启动，在 :code:`/etc/pam.d/slim` 下设置:

::

  auth optional pam_gnome_keyring autostart
  session optional pam_gnome_keyring autostart

（autostart 选项可以在判断该 daemon 没有启动时自动启动），同时在 :code:`/etc/pam.d/passwd`  下设置 :code:`passwd optional pam_gnome_keyring` （这里不需要 autostart，因为 passwd 下当检测 daemon 未运行时会自动开启，并在结束 passwd 命令后停止，而一旦设置了 autostart ，则会一直开启，容易导致多个 daemon），重启后重新使用 SLiM 登录，自动运行了 gnome-keyring-daemon，chain 也自动解锁了，但是打开 nextcloud-client 依旧提示无 keychain 服务。

去 #archlinux-cn Telegram 群询问了一下被告知使用 dbus-monitor 查看是否有 :code:`org.freedesktop.secrets` 相关信息，但是并没有。

后尝试安装 kwalletd 能否解决。 **确实解决了**，而且只能在启用了 kwalletd 的情况下有效，也就是不支持 KDE5 的 kwalletd...... (这边解释有问题)

最后对 3 种情况下的 dbus-monitor 信息进行了对比，发现 NextCloud-Client 根本不请求 gnome-keyring ，只请求 org.kde.kwalletd。简直了，估计是会先读取当前环境，不匹配两者的情况下就默认请求 kwalletd 了... 真的不能太笨了。对比信息：

1. 未安装 kwalletd https://p.ume.ink/t/cbb0  
2. 安装了 kwalletd 并启动了 https://p.ume.ink/t/cbby 
3. 安装了 kwalletd 启动了之后手动停止，不重启 dbus 的情况下 https://p.ume.ink/t/cbbz

Q: 对 NextCloud 配置自定义主题失效
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

禁用了 theming app ，并设置了自定义的 theme 且在 config.php 下设置了自定义 theme 后，无效，也无报错，后发现是 DAC 权限问题... 

不过又出现仅应用了 default.php 配置，未应用相关 css，且 chromium 控制台下无报错，有一个讨论在这里 https://github.com/nextcloud/server/issues/5036。

**A:** 一个解决方案看 https://github.com/nextcloud/server/pull/5061 ，然後如果要修改登錄界面的某些樣式的話，需要添加 guest.css 。

咱寫了一個成品的主題在 https://github.com/Bekcpear/UMECloudTheme 。

Q: NextCloud 文件上传结束后打开 NextCloud Web 界面查看，磁盘 IO 直接堵死
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

上传结束后，打开 NextCloud 查看文件就出现了后台对磁盘的疯狂读写（GCE 低容量磁盘 IO 本来就不行），原因不明。等待较长一段时间后恢复正常，看到 NextCloud 错误日志 :code:`Allowed memory size of 536870912 bytes exhausted (tried to allocate 254868480 bytes) at /path/to/my/nextcloud/lib/private/legacy/image.php#576` 。

原因应该是在生成图片的缩略图缓存，因为图片比较大，分配内存份额不足导致的，系程序运行机制优化不好，看 https://help.nextcloud.com/t/nc-box-memory-exhausted/4183 和 https://github.com/nextcloud/server/issues/1732 。

同时也有配置不当的问题。我在 php.ini 下限制了内存最大分配 128M，但是在 :code:`NEXTCLOUDROOT/.user.ini` 下确实默认的 512M 需要修改一致。

原来以为改成了 128M 后应该不会有一样的报错了，但是还是有，只是数字变了一下，奇怪中。然后我尝试上传更大的图片文件，却没有报错... 多试了几次其它的都没有问题，那么那张图的问题就先不处理了，可能是长宽比太奇怪了？ Orz 曾经有针对这个问题进行过修复 https://github.com/nextcloud/server/pull/3778。 后来使用过程中还是有这个问题...

Q: 上传文件到服务器中断报错
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

上传文件到服务器时，出现这个报错::

  Sabre\DAV\Exception\BadRequest: HTTP/1.1 400 expected filesize 10000000 got 2981888

原因和配置以及网络环境都有关系，可以看 https://forum.owncloud.org/viewtopic.php?f=17&t=32517 和 https://github.com/owncloud/core/issues/9832#issuecomment-112305152 ，不再过多纠缠。偶尔有之，最后也成功上传了，客户端并没有上传文件失败的报错。

当使用网页上传文件失败或者取消上传时，也会记录到这个报错，可能和程序本身设计有关系咯？

Q: 上传文件时剩余时间显示异常
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

上传文件时剩余时间显示异常，看 issue 曾经有过类似这个问题且已经修复，但是现在又这样子了。https://github.com/nextcloud/server/issues/3647 。

**A:** 自己修复了，并提交了 PR https://github.com/nextcloud/server/pull/5177

Q: 不断出现这个报错 pcre_exec() failed: -2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

不断出现这个报错 :code:`pcre_exec() failed: -2 on "" using "^/(?:apps/notifications/api/v[12]/notifications|dav/files/ruz/)(?:$)", client: xxx, server: xxx, request: "GET /status.php HTTP/1.1", host: "xxx"` ，怀疑可能是空字符无法做匹配。

**A:** Google 到 -2 确实代表 PCRE_ERROR_NULL，即 the argument code was NULL。详细代码可以看 http://pcre.sourceforge.net/pcre.txt ，而 nginx 下 if 不能嵌套，不能用 || && 这种，那么就简单而蠢一点直接多些几句 if 用 = 来判断吧


.. _`prerequisites-label`: https://doc.owncloud.org/server/10.0/admin_manual/installation/source_installation.html#prerequisites-label
.. _`owncloudPHPExtensions.txt`: https://gist.github.com/Bekcpear/cacfd013833c2974f70540dff7621603
