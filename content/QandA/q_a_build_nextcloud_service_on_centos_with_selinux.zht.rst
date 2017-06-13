========================================================================================================================
Q&A 啟用 SELinux 的情況下，在 CentOS 上搭建 NextCloud/ownCloud 服務
========================================================================================================================

:slug: q_a_build_nextcloud_service_on_centos_with_selinux
:date: 2017-06-12 21:21
:lang: zht
:tags: service, selinux, nginx, php-fpm, installation, redis, memcache

.. contents::

本文記錄了我在部署 ownCloud/NextCloud 時所遇到的問題，處理思路以及解決方案。

Q: 安裝 ownCloud 後不斷出現 SELinux 審計拒絕資訊
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

不斷出現類似這樣子的審計資訊: 

::

  type=PROCTITLE msg=audit(05/27/2017 00:26:03.559:129906) : proctitle=find /usr/local/bin /usr/bin /bin -name sendmail
  type=SYSCALL msg=audit(05/27/2017 00:26:03.559:129906) : arch=x86_64 syscall=newfstatat success=no exit=EACCES(Permission denied) a0=0x9 a1=0x19baf08 a2=0x7fff31a85990 a3=0x100 items=0 ppid=28746 pid=28747 auid=unset uid=php-fpm gid=www euid=php-fpm suid=php-fpm fsuid=php-fpm egid=www sgid=www fsgid=www tty=(none) ses=unset comm=find exe=/usr/bin/find subj=system_u:system_r:httpd_t:s0 key=(null)
  type=AVC msg=audit(05/27/2017 00:26:03.559:129906) : avc:  denied  { getattr } for  pid=28747 comm=find path=/usr/bin/redis-server dev="sda1" ino=248278 scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:object_r:redis_exec_t:s0 tclass=file permissive=0

還會出現類似上述的一個會出現使用 find 查詢 smbclient 被審計拒絕的資訊，這兩個問題都是在訪問 ownCloud 設定頁面時所碰到的。即使我把傳送郵件改為 smtp 後依舊有這個問題。

**A:** 感覺可能是在一開始安裝 owncloud 過程中因為某些檔案的許可權沒有配置好而導致的檔案丟失引起了，隧重新安裝了一下，並將 PHP-FPM 配置檔案 :code:`www.conf` 下的 :code:`env[PATH]` 的預設配置改成了針對當前系統環境的 :code:`/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin` 後問題解決，應該是後者配置不當引起的。

Q: 在 ownCloud 的管理員設定介面，無法編輯 Email Template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

選擇了模板後，出現訪問 :code:`https://c.ume.ink/apps/templateeditor/settings/mailtemplate?theme=&template=core%2Ftemplates%2Fmail.php 403` 報錯，單獨訪問後發現是 :code:`Access forbidden` 和 :code:`CSRF check failed` 。 在禁用了 CSRF 檢查後依舊有 Access forbidden 的報錯。

這個連結實際經過 nginx 配置重寫後應該為 :code:`https://c.ume.ink/index.php/apps/templateeditor/settings/mailtemplate?theme=&template=core%2Ftemplates%2Fmail.php` 。 類似這個 issue https://github.com/owncloud/core/issues/27628 ，等待更新後再看。


Q: 提醒重新整理請求日誌檔案太多
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**A:** nginx 訪問日誌會記錄 :code:`https://c.ume.ink//ocs/v2.php/apps/notifications/api/v1/notifications?format=json` 這個每隔 10 秒的提醒重新整理請求，通過在 

.. code-block:: nginx

  location ~ ^/(?:index|remote|public|cron|core/ajax/update|status|ocs/v[12]|updater/.+|ocs-provider/.+|core/templates/40[34])\.php(?:$|/) {
    ...
  }

塊中新增如下後解決:

.. code-block:: nginx

  if ($fastcgi_path_info = /apps/notifications/api/v1/notifications) {
    access_log off;
  } 

.. _`Q: smtp 發信失敗，提示連線到 smtp.mailgun.org 超時，無 SELinux 審計相關資訊`:

Q: smtp 發信失敗，提示連線到 smtp.mailgun.org 超時，無 SELinux 審計相關資訊
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

通過 tcpdump 抓包後發現在與 :code:`smtp.mailgun.org` 握手時，只有從本地伺服器傳送出去的 SYN 包，遲遲收不到 ACK 從而導致的超時。即使關閉了防火牆也是一樣的效果，替換 mailgun 埠 25/465/587 都無效，懷疑 mailgun 對 Google Cloud 某些 IP 進行了遮蔽。

同時看到 GCP 也對虛擬機器的預設 smtp 埠有限制，詳細看 https://cloud.google.com/compute/docs/tutorials/sending-mail/ 。

關於 sendmail，其實當前環境是沒有安裝的，sendmail 這個命令是呼叫了 postfix 的功能，而 postfix 是 sendmail 的一個替代品，繼承了 sendmail 的命令和引數。GCP 對預設的 smtp 埠進行了禁用處理因為出現了大量對該類埠濫用的情況。可以通過第三方的郵件服務上來發送郵件，比如 SendGrid/Mailgun./Mailjet ，如果需要用到自己企業內部的發信服務，那就需要利用 VPN 來解決了。比如針對 Mailgun 的配置可以看 https://cloud.google.com/compute/docs/tutorials/sending-mail/using-mailgun ，**A: 通過如上配置，最後也成功使用 php 模式發信了。**

Q: Redis 無法使用 unix socket 檔案與 PHP-FPM 通訊
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

這是一個暫時不想去解決的問題，原來是想使用 unix domain socket 檔案來使得 php-fpm 與 redis 之間進行通訊的，但是目前給 php-fpm  使用的限制性域類為 :code:`httpd_t` ，而 redis 的則為 :code:`redis_t` ， :code:`httpd_t` 完全沒有可以對 :code:`redis_t` 所對應的目前檔案 type 有讀寫許可權的預設規則，比如一般 redis 的 socket 檔案是標記為 :code:`redis_var_run_t` ，但是 :code:`httpd_t` 沒有對其的預設規則。同時， :code:`redis_t` 域執行的程序沒有對非 :code:`redis_` 字首的檔案/資料夾有讀寫許可權，所以也沒有辦法生成為 :code:`var_run_t` 型別的 redis.sock 檔案。

**A:** 在不新建規則的情況下，替換使用 tcp socket 即可。但是替換使用了 tcp socket 後，默認出現了 :code:`httpd_t` 對 :code:`redis_port_t` 的 name_connect denied，設定：

.. code-block:: bash

  setsebool -P httpd_can_network_connect on

後解決。

Q: Redis systemd 服務指令碼無法啟動，錯誤資訊為無法停止服務
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Redis 在改動為不進行 tcp 埠監聽後，出現預設指令碼無法啟動的問題，總是提示無法停止服務，有點迷。後查得原因是因為使用了 :code:`/usr/bin/redis-shutdown` 來作為停止服務的命令，而這個命令預設是使用 6379 埠來與 redis 服務通訊並通知其停止服務的，在改為了 unix domain socket 檔案通訊並關閉了 tcp socket 後出現連線 refuse 而導致報錯，從而導致服務指令碼執行異常。

**A:** 解決方法是寫一個單獨的 bash 指令碼，然後使用 :code:`/usr/bin/redis-cli` 來指定為 unix domain socket 檔案通訊，並傳遞 shutdown 操作，以這個 bash 指令碼作為 systemd 服務檔案的停止命令即可。

*注意， systemd 服務啟動 redis 不能使用 redis 的 daemon 模式，不然會出現奇怪的問題，暫時不知道原因，不過先跳過。*


Q: ownCloud 建議的使用系統的 crond 計劃任務執行失敗
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

這個是每隔 15 分鐘執行一遍 :code:`/path/to/owncloud/cron.php` 以實現定時檢查的功能。我也根據提示並通過命令 :code:`crontab -u php-fpm -e` 開啟並添加了 :code:`*/15  *  *  *  * /opt/local/php/bin/php -f /path/to/owncloud/cron.php` ，但是就是不執行，php-fpm 的組使用者為 www， :code:`/opt/local/php/bin/php` 檔案是可以被 php-fpm 讀取並執行的，其 SELinux type 為 :code:`httpd_exec_t` ， :code:`/path/to/owncloud/cron.php`  所對應的目錄許可權為 750 目錄組為 www，檔案許可權為 640 ，檔案組為 www，後檢視日誌報錯為 :code:`(CRON) ERROR chdir failed (/home/php-fpm): No such file or directory` 。

**A:** 建立 php-fpm 家目錄，修改許可權，SELinux content type 改為 :code:`httpd_sys_rw_content_t` 後解決


Q: SELinux 拒絕 execmem 操作
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

一開始安裝好並開啟 owncloud 主頁後出現了

::

  type=AVC msg=audit(1495804058.069:129092): avc:  denied  { execmem } for  pid=26255 comm="php-fpm" scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:system_r:httpd_t:s0 tclass=process permissive=0

**A:** 雖然通過 :code:`setsebool -P httpd_execmem on` 解決了，但是還是應該去看看這個報 https://bugzilla.redhat.com/show_bug.cgi?id=1380930 的 bug 以獲取更詳盡的資訊，不止一種解決方法。也和 php 的 jit 啟用與否有關。

Q: 大量國際化報錯資訊
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

最開始安裝 PHP 的時候，很多模組沒有裝好，其中 **intl 的沒有裝好** 導致了大量 :code:`You are using a fallback implementation of the intl extension. Installing the native one is highly recommended instead.` 這個報錯資訊出現在 owncloud.log 檔案中，關於 owncloud 所需要的 PHP 模組可以看 ownCloud 的說明 `prerequisites-label`_ ，我對其稍作整理了一下: `owncloudPHPExtensions.txt`_

Q: 啟用 imap 情況下編譯 PHP 報錯
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在編譯 PHP 的時候，當啟用了 imap 的情況下，會出現 :code:`utf8_mime2text() has new signature, but U8T_CANONICAL is missing. This should not happen.` 這個報錯，使用 yum 安裝了 libc-client 後也沒有用，且在 CentOS 7 下沒有查到 libc-client-devel 包很奇怪，看網上有人說還需要編譯安裝 imap-2007f 的包，感覺是不是太舊了，而且 imap 的需求僅僅在用需要整合 imap app 的情況下才會用到，暫時就不去理會，去掉了這個模組。

Q: 啟用了 APCu 下編譯 PHP 報 apc_arginfo.h 檔案缺失
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**A:** PHP 7 是有單獨的 acpu 模組包的，看官方文件 https://secure.php.net/manual/en/apcu.installation.php 上寫了可以在 pecl 檔案庫下載，但是實際使用後發現缺失檔案，報 apc_arginfo.h 檔案沒有，所以直接從 github 下載並解壓後到 PHPSRCROOT/ext  下後編譯安裝，相關說明可以看 https://secure.php.net/manual/en/install.pecl.static.php

Q: 使用 sendmail 方式傳送郵件報錯
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

「相關問題」繼問題 `Q: smtp 發信失敗，提示連線到 smtp.mailgun.org 超時，無 SELinux 審計相關資訊`_ 重新安裝後，還需要的其它一些問題，解決方案直接看上文。

1. 設定裡的 Mail Server 的 send mode 多了一個 sendmail 選項，選擇其傳送測試郵件出現  :code:`(Error: Expected response code 220 but got code "", with message "")` 報錯，SELinux 規則審計為：

::

  type=PROCTITLE msg=audit(05/27/2017 13:03:35.266:131989) : proctitle=/usr/sbin/sendmail -bs
  type=SYSCALL msg=audit(05/27/2017 13:03:35.266:131989) : arch=x86_64 syscall=open success=no exit=EACCES(Permission denied) a0=0x55a1c79309e0 a1=O_RDONLY a2=0x0 a3=0x3 items=0 ppid=26861 pid=26866 auid=unset uid=php-fpm gid=www euid=php-fpm suid=php-fpm fsuid=php-fpm egid=www sgid=www fsgid=www tty=(none) ses=unset comm=sendmail exe=/usr/sbin/sendmail.postfix subj=system_u:system_r:httpd_t:s0 key=(null)
  type=AVC msg=audit(05/27/2017 13:03:35.266:131989) : avc:  denied  { read } for  pid=26866 comm=sendmail name=main.cf dev="sda1" ino=17007198 scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:object_r:postfix_etc_t:s0 tclass=file permissive=0 

目前認為這個是 SELinux 的規則配置問題，改 php 模式可以傳送成功，不再另行配置。

2. 改用 PHP 模式傳送郵件，在 SELinux 設定了 httpd_can_sendmail 為 on 後不再出現 :code:`avc:  denied  { read } for  pid=27097 comm=sendmail name=main.cf` 報錯，但是收不到訊息，是伺服器的 postfix 服務沒有啟用，且配置不正確導致的.

3. 改用 sendmail 模式傳送郵件，即使 SELinux 設定了 :code:`httpd_can_sendmail 為 on`，卻依舊出現了：

::

  type=PROCTITLE msg=audit(05/27/2017 13:49:02.605:132083) : proctitle=/usr/sbin/sendmail -bs
  type=SYSCALL msg=audit(05/27/2017 13:49:02.605:132083) : arch=x86_64 syscall=execve success=no exit=EACCES(Permission denied) a0=0x55d80dc4a7e0 a1=0x55d80dc4a780 a2=0x55d80dc4ec40 a3=0x4 items=0 ppid=26738 pid=27266 auid=unset uid=php-fpm gid=www euid=php-fpm suid=php-fpm fsuid=php-fpm egid=www sgid=www fsgid=www tty=(none) ses=unset comm=sendmail exe=/usr/sbin/sendmail.postfix subj=system_u:system_r:system_mail_t:s0 key=(null)
  type=AVC msg=audit(05/27/2017 13:49:02.605:132083) : avc:  denied  { execute } for  pid=27266 comm=sendmail name=smtpd dev="sda1" ino=34131935 scontext=system_u:system_r:system_mail_t:s0 tcontext=system_u:object_r:postfix_smtpd_exec_t:s0 tclass=file permissive=0

的報錯，懷疑是 postfix 設定問題。

Q: 替換 NextCloud 後，設定介面提示 PHP Opcache 配置不正確
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

替換為 nextcloud 正常配置後，設定介面提示 :code:`The PHP Opcache is not properly configured. For better performance we recommend ↗ https://docs.nextcloud.com/server/12/go.php?to=admin-php-opcache  to use following settings in the php.ini: opcache.enable=1 opcache.enable_cli=1 opcache.interned_strings_buffer=8 opcache.max_accelerated_files=10000 opcache.memory_consumption=128 opcache.save_comments=1 opcache.revalidate_freq=1` ，但是設定了也啟用了 opcache 後，依舊有這樣子的提示，phpinfo() 也看不到 opcache 的引數，但是 :code:`php-fpm -v` 可以看到已經有啟用了 opcache 的了。

查找了 php 官方說明發現如果編譯時候使用了 --disable-all 禁用了預設的擴充套件的話，需要使用 --enable-opcache 來啟用 opcache 的支援，但是我並沒有禁用，不過還是添加了這個引數後重新編譯試了一下，但是並沒有效果。

**A:** 最後發現是 selinux 標籤配置不當。我之前檢查了 audit 日誌，但是並沒有相關報錯提示，最後發現在 systemd 日誌下有一個許可權錯誤 :code:`failed to map segment from shared	object: Permission denied` ，臨時把 selinux 改成 permissive mode 後重啟 php-fpm 就一切正常了。多次嘗試下，是 :code:`httpd_t` 類域下程序缺少對 :code:`opcache.so` 檔案的 execute 許可權，給 :code:`PHPLOCAL/lib/php/extensions` 目錄統一改 selinux 標籤為 :code:`httpd_sys_script_exec_t` 後，恢復為 enforcing mode 再重啟 php-fpm 一切正常。

Q: NextCloud 下即使配置了 X-Frame-Option 但是依舊提示為配置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

明明 nginx 配置檔案下已經添加了 X-Frame-Option 的頭為  SAMEORIGIN 但是依舊出現了這個提示 :code:`The "X-Frame-Options" HTTP header is not configured to equal to "SAMEORIGIN". This is a potential security or privacy risk and we recommend adjusting this setting.` 

**A:** 需要從 Nginx 配置中移除改選項，詳細的看 https://github.com/nextcloud/server/issues/4764 和 https://docs.nextcloud.com/server/12/admin_manual/release_notes.html 


Q: NextCloud 預覽視訊檔案報錯
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NextCloud 預覽視訊檔案報錯 :code:`Uncaught ReferenceError: videojs is not defined  at Object.show (viewer.js?v=3bdb93f…-0:39)  at Object.<anonymous> (viewer.js?v=3bdb93f…-0:82)  at Object.<anonymous> (core.js?v=3bdb93f…-0:2) ...`

**A:** 已經有解決方案，看這裡: https://github.com/nextcloud/files_videoplayer/pull/26/commits/37c2866e319e0e8ff1b2f70da3a1d8c7cd21697b 。但是會導致改視訊預覽 app 的簽名檔案異常，因為我沒有作者的私鑰，所以也沒有辦法，自己籤也不可以，因為需要由 nextCloud 來發證書，而 app 並不是我的。 nextCloud 與 ownCloud 有一個區別是對於 app 的簽名檔案，當簽名 hash 與檔案不匹配時，nextCloud 並不會提示，而 ownCloud 會。

Q: 檢查 NextCloud 日誌發現提示 APCu 不可用
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

檢查 nextCloud 日誌發現提示資訊::

  Memcache \OC\Memcache\APCu not available for local cache Memcache \OC\Memcache\APCu not available for distributed cache

在每 15 分鐘一次的計劃任務執行後生成。

**A:** 最後排查發現是因為雖然編譯進了 apcu 但是配置並沒有啟用，在 php.ini 中加入 :code:`apc.enabled=1` 和 :code:`apc.enable_cli=1` 後即可

Q: NextCloud 上傳檔案時， FileHooks.php 報錯
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NextCloud 上傳檔案時經常性出現 :code:`Undefined offset: 3 at /data/0/www/nextcloud/apps/activity/lib/FilesHooks.php#620` 報錯，系 bug 在此 https://github.com/nextcloud/server/issues/4971 ，臨時解決方法： https://github.com/nextcloud/activity/pull/156/commits/0b627d63349d035c0282f0984f7e2519d6ec57b3 


Q: 在每次使用 cron 執行 cron.php 時出現的一個 SELinux 拒絕審計資訊
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在每次使用 cron 執行 cron.php 時出現的一個 SELinux 拒絕審計資訊

::

  type=PROCTITLE msg=audit(05/29/2017 02:00:03.782:137263) : proctitle=local -t unix
  type=SYSCALL msg=audit(05/29/2017 02:00:03.782:137263) : arch=x86_64 syscall=lstat success=no exit=EACCES(Permission denied) a0=0x55fd699c9080 a1=0x7fff3971e260 a2=0x7fff3971e260 a3=0x7f1c14c362e0 items=0 ppid=31757 pid=18374 auid=unset uid=root gid=root euid=php-fpm suid=root fsuid=php-fpm egid=www sgid=root fsgid=www tty=(none) ses=unset comm=local exe=/usr/libexec/postfix/local subj=system_u:system_r:postfix_local_t:s0 key=(null)
  type=AVC msg=audit(05/29/2017 02:00:03.782:137263) : avc:  denied  { search } for  pid=18374 comm=local name=php-fpm dev="sda1" ino=37082976 scontext=system_u:system_r:postfix_local_t:s0 tcontext=unconfined_u:object_r:httpd_sys_rw_content_t:s0 tclass=dir permissive=0 
  
最後發現是在 php.ini 下配置了錯誤的 zend_extension 而導致在執行 cron 時去做了預設情況下不允許做的操作而被審計了，在 journal 和 /var/mail/php-fpm 下都可以看到，相關錯誤資訊為 :code:`/opt/local/php/lib/php/extensions/no-debug-non-zts-20160303/apcu.so doesn't appear to be a valid Zend extension` 。 這個其實我有點迷，因為我在編譯時其實已經編譯進了 apcu 了，但是後來搗鼓的時候又使用 pecl 安裝了一個，有機會再繼續就這個問題分析吧。

Q: 客戶端每次都需要輸入密碼，報錯 No keychain service available
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在 Gentoo 上 AwesomeWM 下使用 NextCloud 客戶端，每次開啟都會提示 :code:`No keychain service available` ，顧名思義是 keychain 的問題。

安裝上了 kwalletd 後提示資訊出現了區別 :code:`Failed to execute program org.kde.kwalletd: No such file or directory` 。單獨執行 kwalletd5 也是一樣的問題。

後看到 archwiki 上有一個說明:  https://wiki.archlinux.org/index.php/Nextcloud#.22Reading_from_keychain_failed_with_error:_.27No_keychain_service_available.27.22 。東西我是已經裝好了，再根據 gentoowiki 上 SLiM（我當前用的 DM） 自動解鎖 gnome-keyring 配置好後 https://wiki.gentoo.org/wiki/SLiM#Unlock_keyrings，重新登入試試，無效。

在 https://wiki.gnome.org/Projects/GnomeKeyring/Pam  https://wiki.gentoo.org/wiki/SLiM#Unlock_keyrings 上有寫關於 gnome-keyring 的設定，因為我的不是 Gnome，是 SLiM 這個 DM，一般建議是 gnome-keyring-daemon 隨登入啟動，在 :code:`/etc/pam.d/slim` 下設定:

::

  auth optional pam_gnome_keyring autostart
  session optional pam_gnome_keyring autostart

（autostart 選項可以在判斷該 daemon 沒有啟動時自動啟動），同時在 :code:`/etc/pam.d/passwd`  下設定 :code:`passwd optional pam_gnome_keyring` （這裡不需要 autostart，因為 passwd 下當檢測 daemon 未執行時會自動開啟，並在結束 passwd 命令後停止，而一旦設定了 autostart ，則會一直開啟，容易導致多個 daemon），重啟後重新使用 SLiM 登入，自動運行了 gnome-keyring-daemon，chain 也自動解鎖了，但是開啟 nextcloud-client 依舊提示無 keychain 服務。

去 #archlinux-cn Telegram 群詢問了一下被告知使用 dbus-monitor 檢視是否有 :code:`org.freedesktop.secrets` 相關資訊，但是並沒有。

後嘗試安裝 kwalletd 能否解決。 **確實解決了**，而且只能在啟用了 kwalletd 的情況下有效，也就是不支援 KDE5 的 kwalletd...... 

最後對 3 種情況下的 dbus-monitor 資訊進行了對比，發現 NextCloud-Client 根本不請求 gnome-keyring ，只請求 org.kde.kwalletd。簡直了，估計是會先讀取當前環境，不匹配兩者的情況下就預設請求 kwalletd 了... 真的不能太笨了。對比資訊：

1. 未安裝 kwalletd https://p.ume.ink/t/cbb0  
2. 安裝了 kwalletd 並啟動了 https://p.ume.ink/t/cbby 
3. 安裝了 kwalletd 啟動了之後手動停止，不重啟 dbus 的情況下 https://p.ume.ink/t/cbbz

Q: 對 NextCloud 配置自定義主題失效
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

禁用了 theming app ，並設定了自定義的 theme 且在 config.php 下設定了自定義 theme 後，無效，也無報錯，後發現是 DAC 許可權問題... 

不過又出現僅應用了 default.php 配置，未應用相關 css，且 chromium 控制檯下無報錯，有一個討論在這裡 https://github.com/nextcloud/server/issues/5036。

**A:** 一個解決方案看 https://github.com/nextcloud/server/pull/5061 ，然後如果要修改登入介面的某些樣式的話，需要新增 guest.css 。

咱寫了一個成品的主題在 https://github.com/Bekcpear/UMECloudTheme 。

Q: NextCloud 檔案上傳結束後開啟 NextCloud Web 介面檢視，磁碟 IO 直接堵死
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

上傳結束後，開啟 NextCloud 檢視檔案就出現了後臺對磁碟的瘋狂讀寫（GCE 低容量磁碟 IO 本來就不行），原因不明。等待較長一段時間後恢復正常，看到 NextCloud 錯誤日誌 :code:`Allowed memory size of 536870912 bytes exhausted (tried to allocate 254868480 bytes) at /path/to/my/nextcloud/lib/private/legacy/image.php#576` 。

原因應該是在生成圖片的縮圖快取，因為圖片比較大，分配記憶體份額不足導致的，系程式執行機制優化不好，看 https://help.nextcloud.com/t/nc-box-memory-exhausted/4183 和 https://github.com/nextcloud/server/issues/1732 。

同時也有配置不當的問題。我在 php.ini 下限制了記憶體最大分配 128M，但是在 :code:`NEXTCLOUDROOT/.user.ini` 下確實預設的 512M 需要修改一致。

原來以為改成了 128M 後應該不會有一樣的報錯了，但是還是有，只是數字變了一下，奇怪中。然後我嘗試上傳更大的圖片檔案，卻沒有報錯... 多試了幾次其它的都沒有問題，那麼那張圖的問題就先不處理了，可能是長寬比太奇怪了？ Orz 曾經有針對這個問題進行過修復 https://github.com/nextcloud/server/pull/3778。 後來使用過程中還是有這個問題...

Q: 上傳檔案到伺服器中斷報錯
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

上傳檔案到伺服器時，出現這個報錯::

  Sabre\DAV\Exception\BadRequest: HTTP/1.1 400 expected filesize 10000000 got 2981888

原因和配置以及網路環境都有關係，可以看 https://forum.owncloud.org/viewtopic.php?f=17&t=32517 和 https://github.com/owncloud/core/issues/9832#issuecomment-112305152 ，不再過多糾纏。偶爾有之，最後也成功上傳了，客戶端並沒有上傳檔案失敗的報錯。

當使用網頁上傳檔案失敗或者取消上傳時，也會記錄到這個報錯，可能和程式本身設計有關係咯？

Q: 上傳檔案時剩餘時間顯示異常
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

上傳檔案時剩餘時間顯示異常，看 issue 曾經有過類似這個問題且已經修復，但是現在又這樣子了。https://github.com/nextcloud/server/issues/3647 。

**A:** 自己修復了，並提交了 PR https://github.com/nextcloud/server/pull/5177

Q: 不斷出現這個報錯 pcre_exec() failed: -2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

不斷出現這個報錯 :code:`pcre_exec() failed: -2 on "" using "^/(?:apps/notifications/api/v[12]/notifications|dav/files/ruz/)(?:$)", client: xxx, server: xxx, request: "GET /status.php HTTP/1.1", host: "xxx"` ，懷疑可能是空字元無法做匹配。

**A:** Google 到 -2 確實代表 PCRE_ERROR_NULL，即 the argument code was NULL。詳細程式碼可以看 http://pcre.sourceforge.net/pcre.txt ，而 nginx 下 if 不能巢狀，不能用 || && 這種，那麼就簡單而蠢一點直接多些幾句 if 用 = 來判斷吧


.. _`prerequisites-label`: https://doc.owncloud.org/server/10.0/admin_manual/installation/source_installation.html#prerequisites-label
.. _`owncloudPHPExtensions.txt`: https://gist.github.com/Bekcpear/cacfd013833c2974f70540dff7621603