========================================================================================================================
啟用 SELinux 的情況下，在 CentOS 上搭建 NextCloud/ownCloud 服務
========================================================================================================================

:slug: build_nextcloud_service_on_centos_with_selinux
:date: 2017-06-12 17:01
:lang: zht
:tags: service, selinux, nginx, php-fpm, installation, redis, memcache

.. contents::

因為 AWS 下的服務到期了，速度太慢也不準備繼續使用，轉而更換到 Google TW 線路。也準備在啟用 SELinux 的情況下重新搭一下 ownCloud 服務，之後又經 `KayMW`_ 推薦換搭了 NextCloud ，兩者配置基本相同，少許的我發現的配置差異會在文中說明。

本次搭建同時使用 redis 作為 Transactional Locking 的資料庫，並使用 APCu 作為本地 memcache 過程。

因為篇幅問題，所以肯定不可能把所有的都說的很細，主要是重點。

選擇 VPS
========================================

每次選 VPS 都是一個痛苦的過程，既要保證穩定性，又要求價格合理，到大陸的速度也不能太慢.. 我個人更追求穩定，速度其次。幾番比較下來，選擇 Google Cloud Platform 的原因在於其家大業大比較放心，操作面板確實非常方便（除了竟然沒有原生 IPv6 外），TW 機房的線路到大陸的速度也相當不錯，唯一就是網路使用按流量計費，尤其到大陸價格太貴，好在我也用不了多少流量。

系統確定為 CentOS 7
========================================

原來我是打算安裝 Archlinux 作為伺服器系統的，沒想到 Google 把計算引擎的這個系統預設映象給砍掉了.. 我也不想自己再另外裝以免玄學問題。所以就還是 CentOS 7 吧。

確定部署方案
========================================

ownCloud/NextCloud 的部署方案一般推薦都是 Nginx + PHP-FPM + Mysql/MariaDB ，這次我也準備在不關閉 SELinux 的情況下部署，同時安裝 Redis 作為給 Transactional Locking 使用的資料庫， APCu 用於本地 memcache。 Nginx 版本採用的是 1.12， PHP 版本採用的是 7.1，這兩者都通過原始碼編譯來安裝，其中 Nginx 同時編譯進 ct-nginx 模組以實現證書透明度支援。 MariaDB 則直接使用現成的官方源。

開始部署
========================================

VPS 安裝
--------------------------------------------------------------------------------

Google Cloud Platform 操作很簡單，選擇了一個最低的配置，選擇系統，確定隨機/固定外網 IP，傳上 ssh 公鑰，開啟 80 & 443 防火牆埠，點選完成後稍等片刻即可。

基本的系統設定
--------------------------------------------------------------------------------

* :code:`yum update -y` 更新一下系統
* 安裝必要的工具做基本的系統配置，比如啟用 fail2ban, vnstat 服務，開啟防火牆的 80 & 443 埠，安裝 sysstat，或者啟用個 BBR 協議等。
* :code:`getenforce` 確認 SELinux 處於 Enforcing 模式下，如果不在這個模式下，先檢查 :code:`/var/log/audit/audit.log` 檔案下是否有拒絕什麼的審計資訊，也可以使用 :code:`ausearch -i -m AVC,USER_AVC,SELINUX_ERR -ts today` 命令檢視，解決掉問題後輸入 :code:`setenforce 1` 以設定 SELinux 到 Enforcing 模式下，並編輯 :code:`/etc/selinux/config` 檔案，確認修改 :code:`SELINUX=` 值為 :code:`enforcing` ，同時執行一下 :code:`fixfiles onboot` 命令以使得下次重啟後的檔案擁有非錯誤的 SELinux 標籤。以上命令都需要以 root 身份執行。注意，這邊需要同時確認 SELinux 啟用型別為 targeted，反正預設都是的，如果不是，參考 `Enabling MLS in SELinux`_ 反過來修改。

編譯安裝 Nginx 和 PHP-FPM
--------------------------------------------------------------------------------

關於這兩者的編譯安裝，我有寫過一個現成的指令碼 `install nginx and php-fpm from source`_ ，不過其中就 PHP 的編譯配置選項需要有針對性的配置（除卻了基本的路徑和使用者名稱配置）::

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

除了腳本里面需要安裝的依賴關係外，大概還需要這麼幾個包的存在 :code:`libwebp libwebp-devel libXpm libXpm-devel gmp gmp-devel libc-client icu libicu libicu-devel`

其中 APCu (PHP7) 以及 Redis 的啟用需要另外下載包到 :code:`/path/to/php/source/code/ext` 目錄下，可以參考 `PHP 官方說明文件`_ ，獲取也可以在安裝好之後使用 :code:`pecl` 命令來安裝，不過我並沒有這樣子嘗試，詳細文件也可以在該頁面找到。 

* APCu 原始碼包在 https://github.com/krakjoe/apcu
* Redis 原始碼包在 https://github.com/phpredis/phpredis/

安裝 MariaDB Server
--------------------------------------------------------------------------------

請看 `Setting up MariaDB Repositories`_ 

安裝 Redis
--------------------------------------------------------------------------------

:code:`yum install -y redis`

NextCloud 下載及整體配置 
--------------------------------------------------------------------------------

NextCloud 是在 ownCloud 的基礎上修改演變的，關於瞭解其歷史可以看 `History_of_the_fork`_ 。 目前的最新穩定版為 `v12.0.0`_ ，下載解壓後的資料夾即充當 NextCloud web 服務主目錄。 更詳細的配置可以直接看 `NextCloud 官方說明文件`_ 。

配置 Nginx
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

參照 NextCloud 官方示例配置修改版在 `nginx-conf-example-for-nextcloud.conf`_ 。

  注意的是， ownCloud 的 Nginx 配置示例下因為 ETag header 的問題禁用了 gzip。

相較 NextCloud 配置示例而言，主要是添加了證書透明度和 HKPK 頭的選項，關於證書透明度的配置問題，可以看 `imququ`_ 的部落格， HPKP 的配置則可以看 `HTTP Public Key Pinning`_ 。針對這個我也有寫了一個指令碼用於獲取相關必要的資訊，在 `for_generating_additional_security_information_of_SSL_certificate`_ 。

配置 PHP-FPM
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* 複製原始碼目錄下 :code:`php.ini-production` 到編譯時指定的 PHP 系統配置目錄下 :code:`php.ini` 
* 對 APCu 配置為啟用（ :code:`apc.enable_cli` 和 :code:`apc.enable` 均設定為 :code:`1` ）。關於支援最大上傳檔案大小，可以儘可能配置大一點（ :code:`post_max_size` 和 :code:`upload_max_filesize` ），因為在 NextCloud 資料夾下還有配置檔案可以用於限制，且支援直接在 web 控制檯下修改，會在下文說明。
* 設定好使用者名稱 使用者組 日誌路徑等
* 在 :code:`/path/to/php-configuration_dir/php-fpm.d/www.conf` 下如果配置了監聽的為 socket 檔案的話，不要忘記設定正確的 :code:`listen.owner` :code:`listen.group` :code:`listen.mode` ， SELinux 的標籤配置下文一起說明。 
* 取消如下幾項的註釋，並設定 PATH 到系統正確的值，詳細原因看 `php-fpm Configuration Notes`_

::

  env[HOSTNAME] = $HOSTNAME
  env[PATH] = /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
  env[TMP] = /tmp
  env[TMPDIR] = /tmp
  env[TEMP] = /tmp

配置 MariaDB
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

並沒有特別特殊的要求，我在 [mysqld] section 下設定了一個 :code:`skip-networking` 以使其只監聽 socket 檔案，別忘記設定 :code:`socket=/path/to/your/sock/file` 以確定你的 socket 檔案路徑，預設的路徑可能會因為發行版的不同而不同；設定了 :code:`datadir=/path/to/your/data/dir` 以替換預設的資料庫儲存路徑。

NextCloud 同時支援儲存 emoji unicode，但是資料庫表的格式需要修改，如果需要，詳細的看 `Enabling MySQL 4-byte support`_ 。在這裡執行 MariaDB 後建立好給 NextCloud 用的 資料庫和資料庫使用者名稱。

配置 Redis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

主要注意監聽地址，因為其一般是沒有許可權控制的，所以監聽在本地 127.0.0.1 上為可。雖然也可以監聽為 unix socket 檔案，但是後來出了問題，詳細的在下一篇問題整理裡面說明。其它在這裡預設配置即可。

配置 SELinux 標籤和 NextCloud 下屬檔案許可權
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**MariaDB** 因為是通過 yum 來安裝的，其安裝路徑為預設，而預配置好的 SELinux 上下文已經包含了常用的軟體了，所以預設情況下是不需要配置的。但是因為我替換了其資料資料夾的地址，所以對新的地址需要進行配置。給新路徑的資料夾及其子檔案（夾）配置規則設定其 SELinux 上下文型別為 :code:`mysqld_db_t` ，即（ :code:`semanage` 命令配置後不會及時生效但是會持久儲存，使之生效則使用 :code:`restorecon` 命令）：

.. code-block:: bash

  semanage fcontent -a -t mysqld_db_t '/path/to/your/db/dir(/.*)?'
  restorecon -R /path/to/your/db/dir

之後別忘記檢查 DAC(Discretionary Access Control) 許可權配置，然後執行 :code:`mysql_install_db` 命令來安裝資料庫基本檔案。之後就是正常的資料庫/表建立了。


**Nginx 和 PHP-FPM** 因為是我從原始碼編譯安裝的，所以一個 SELinux 上下文資訊都沒有配置，下面說明。

SELinux 下預設對 http 服務有一系列的策略，我簡單歸納為屬於 httpd_t 域下，也就是說可以把 Nginx 和 PHP-FPM 配置為到 httpd_t 域下執行。而過度到這個域下所需要配置給 :code:`nginx` 和 :code:`php-fpm` 命令的 SELinux 上下文型別為 httpd_exec_t，同時也需要對相關的其它需求資訊設定為 httpd_t 域可都，特定資訊可寫。預設配置策略下，可讀的對應 SELinux 上下文型別有 httpd_sys_content_t/httpd_user_content_t、可讀可寫的對應 SELinux 上下文型別有 httpd_sys_rw_content_t/httpd_user_rw_content_t（或者其它），還需要給 PHP 的擴充套件設定指令碼可執行許可權，對應的 SELinux 上下文型別為 httpd_sys_script_exec_t，即：

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

之後稍微整合一下，處理一下 DAC 許可權就應該可以跑起來了。

**NextCloud** 的配置的話，主要分三個步驟：

1. 所有檔案的 DAC 許可權重新配置，這個有現成的 ownCloud 提供的指令碼 `post-installation-steps`_ （NextCloud 下雖然沒有找到，但是通用）。
2. 處理好 SELinux 的檔案上下文資訊，NextCloud 下有相關說明 `NextCloud SELinux Configuration`_ 。簡而言之就是給整個資料夾及其子檔案（夾）先設定 httpd_sys_content_t 型別，然後就需要寫許可權的設定 httpd_sys_rw_content_t 型別，這樣子基本功能就可以用了。之後再對某些需要的功能單獨啟用相關設定。
3. 配置引數:

* 到這裡就可以直接執行起來 NextCloud 了，所以啟動了服務後，使用瀏覽器開啟本 NextCloud 服務 web 介面，進行初始化配置，主要就是 **管理員使用者名稱**，**管理員使用者密碼**，**雲資料儲存路徑**，**資料庫選擇**，**資料庫使用者名稱**，**資料庫使用者密碼**，**資料庫名**，**資料庫連結地址**。 其中連結地址，如果是使用的 unix socket 檔案的話，格式是 :code:`localhost:/path/to/your/mysql.sock` 。如果是使用的 TCP 連線的話，注意可能需要另外配置 httpd_t 域的相關布林值允許訪問網路，嘗試設定這兩個布林值或其中之一為 :code:`on` : :code:`httpd_can_network_connect/httpd_can_network_connect` ，我沒有實際試驗，因為我用的是 unix socket 檔案，且設定了 MariaDB 不啟用 TCP 監聽功能，以後有機會再確認。
* 之後再手動對 :code:`/path/to/NextCloud/webroot/config/config.php` 檔案進行修改，配置其本地的 memcache 為 APCu，配置 Transactional Locking 使用 Redis 作為資料庫，主要新增如下內容（redis 埠號這邊是預設的並沒有修改）:

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

* 注意別忘記了 /path/to/NextCloud/webroot/.user.ini 下的配置也會對 NextCloud 造成影響。

到這裡所有配置基本就完成了， NextCloud 就已經搭好了。

部署完成 & 後續
========================================

之後可以查 :code:`/path/to/NextCloud/data/nextcloud.log` 這個 nextcloud 日誌檔案和 Nginx 以及 PHP-FPM 的日誌檔案來排錯。 同時擅用 :code:`ausearch` 命令來解決 SELinux 的問題。

關於 NextCloud 的郵件配置，一些應用的配置，以及遇到的相關問題，在另外一篇文章內： 「 `Q&A 啟用 SELinux 的情況下，在 CentOS 上搭建 NextCloud/ownCloud 服務`_ 」

以上。


.. _`KayMW`: https://v2bv.win/about/
.. _`Enabling MLS in SELinux`: https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/SELinux_Users_and_Administrators_Guide/mls.html#enabling-mls-in-selinux
.. _`Setting up MariaDB Repositories`: https://downloads.mariadb.org/mariadb/repositories/#mirror=tuna&distro=CentOS
.. _`install nginx and php-fpm from source`: https://github.com/Bekcpear/my-bash-scripts/tree/master/nginx_and_php-fpm_install_from_source_with_verification
.. _`PHP 官方說明文件`: https://secure.php.net/manual/zh/install.pecl.static.php
.. _`History_of_the_fork`: https://en.wikipedia.org/wiki/Nextcloud#History_of_the_fork
.. _`v12.0.0`: https://github.com/nextcloud/server/releases
.. _`NextCloud 官方說明文件`: https://docs.nextcloud.com/server/12/admin_manual/
.. _`nginx-conf-example-for-nextcloud.conf`: https://gist.github.com/Bekcpear/cfa2045ca4050238e83256ee2726bd5e
.. _`imququ`: https://imququ.com/post/certificate-transparency.html
.. _`HTTP Public Key Pinning`: https://developer.mozilla.org/en-US/docs/Web/HTTP/Public_Key_Pinning
.. _`for_generating_additional_security_information_of_SSL_certificate`: https://github.com/Bekcpear/my-bash-scripts/tree/master/for_generating_additional_security_information_of_SSL_certificate
.. _`php-fpm Configuration Notes`: https://docs.nextcloud.com/server/12/admin_manual/installation/source_installation.html#php-fpm-tips-label
.. _`Enabling MySQL 4-byte support`: https://docs.nextcloud.com/server/12/admin_manual/configuration_database/mysql_4byte_support.html
.. _`post-installation-steps`: https://doc.owncloud.org/server/10.0/admin_manual/installation/installation_wizard.html#post-installation-steps
.. _`NextCloud SELinux Configuration`: https://docs.nextcloud.com/server/12/admin_manual/installation/selinux_configuration.html
.. _`Q&A 啟用 SELinux 的情況下，在 CentOS 上搭建 NextCloud/ownCloud 服務`: /q_a_build_nextcloud_service_on_centos_with_selinux.html