========================================
初識 SELinux
========================================

:slug: understanding_selinux
:date: 2017-06-22 18:21
:lang: zht
:tags: selinux

.. contents::

這是我第一次寫關於 SELinux 的文章， SELinux 是一個比較龐大的強制訪問控制方案，單單就控制原理而言是相對簡單易懂的，複雜的是各種規則間的聯絡和束縛，以及如何選擇。本文會從我對其理解的角度進行書寫，關注點主要是實現和應用。

我是看的 Red Hat 的 `SELinux User's and Administrator's Guide`_ 入的門，本文則會使用我自己的話來進行總結和概括，以便於快速入門，看源連結的文件則可以更詳細的瞭解到 SELinux，但有些內容比如各種策略的選擇，工具的選擇和介紹卻是上文所缺乏的，我單獨整理的也會在下文描述。

鑑於本文很基礎，所以幾個基本的名詞我都會在文中以適當的形式說明。

| *注： 關於部分有爭議的名詞我不準備用中文表示，比如 type,class,subject 等等，被寫成中文的均是我力所能及下認為絕對不會有爭議或者本身就可以用中文描述的*
| *注： 本文不會涉及到 SELinux 的 MLS 策略*

什麼是 SELinux 以及如何理解它
==================================================

:ruby:`安全增強型 Linux| Security-Enhanced Linux` 是 Linux 核心下的一個安全模組，它在 Linux :ruby:`自主訪問控制|Discretionary Access Control` [1]_ 的基礎上提供了額外的訪問控制安全策略，它提供的控制組合為 :ruby:`以角色為基礎的訪問控制|Role-Based Access Control` (RBAC)， Type Enforcement (TE) 和可選的 Multi-Level Security (MLS)。需要明確的是 SELinux 是用來強化已有的安全系統的，而絕對不是用來替代的。

列出一條檢視當前檔案（夾） SELinux 上下文屬性的命令:

.. code-block:: bash

  ls -Z test
  -rwxr-xr-x. root root unconfined_u:object_r:admin_home_t:s0 test

一個相當熟悉的命令 :code:`ls` ，就像平常使用 :code:`ls -l` 檢視檔案的詳細資訊一樣。所以由此讓我對 SELinux 的理解變成了其為組成 Linux 系統安全的最基本的一部分，必須掌握。

明確兩個名詞:

Object
  所有的檔案，包括資料夾、軟連結、裝置等，都被理解為 Object。

Subject
  Linux 下的程序。

簡述許可權審查過程
------------------------------------------------------------

.. ditaa::

                      +-------------------------------------------------------------------+
     User Space       |                              Kernel Space                         |    User Space
                      |                                                                   |
                      |                                                                   |
                      |                                 deny                              |
                      |                          /----------------------------------\     |   
                      |                          |                                  |     |
                      |                       +-----+   allow     +---------+       |     |   allow/deny
  exec a command ---> | --> system call ----> | DAC | ----------> | SELinux | ------+---> | -------------->
                      |                       +-----+             +---------+             |
                      |                                              ^   |                |
                      |                                              :   :                |
                      |                                              |   v                |
                      |                                             /-=---\               |
                      |                                             | AVC |               |
                      |                                             \-----/               |
                      |                                              ^   |                |
                      |                                              :   :                |
                      |                                              |   v                |
                      |                                           /----------\            |
                      |                                           | Policies |            |
                      |                                           \----------/            |
                      |                                                                   |
                      +-------------------------------------------------------------------+

上圖是在啟用 SELinux 情況下的一個 Linux 許可權審查過程，當用戶空間下的一個程序需要系統呼叫時，首先會進行 DAC 檢查，只有 DAC 檢查通過的才會進行 SELinux 的策略驗證，最後判斷是否允許被呼叫。針對 SELinux 的策略所決定的是否允許執行的某一操作，會被快取在 :ruby:`訪問向量快取|Access Vector Cache` (AVC) 內，以提高執行效率。

SELinux 的預設策略為 targeted （也是推薦的），在這個策略下，Type Enforcement (TE) 是主要的的許可權控制手段，大多數情況下， SELinux 使用者和角色都是可以忽略的。也就是說關注點在 :code:`admin_home_t` 這個 type 屬性上。

擁有相同域型別的程序運行於同一個域下，不同域下的程序在沒有相應的 SELinux 策略允許的情況下是不能互相訪問和操作的。注意的是，預設情況下的 Linux 使用者執行在 :code:`unconfined_t` 域（後文以非非限制性域描述）下，而由該域下使用者所直接執行的命令對應的程序大部分同樣是處於該域的，雖然對於非限制性域下的程序而言，SELinux 策略也是會起作用的，但目前存在的策略規則對非限制性域下程序開放幾乎所有的訪問許可權，相當於 SELinux 不起作用了，僅靠 DAC 來做許可權控制。所以這邊就引入到一個處理方式，叫做 :ruby:`域過渡|Domain transitions` ，會在下文詳細描述用法。

簡而言之就是，程序所屬的域型別確定了該程序所擁有的許可權，由 SELinux 策略規則來控制。

CentOS 下 SELinux 工具及對應的包
==================================================

`本人整理的工具列表`_ ，一般來說就是 Red Hat 系所通用的了，其它發行版大致也應該一樣。

其中， :code:`semodule_unpackage`, :code:`sepolicy`, :code:`sefcontext_compile`, :code:`selabel_digest`, :code:`selabel_lookup`, :code:`selabel_lookup_best_match`, :code:`selabel_partial_match`, :code:`selinuxexeccon`, :code:`selinux_restorecon` 這些工具我在 CentOS 6 下則並未找到， CentOS 7 下才可以安裝到。

CentOS 7 下的 :code:`sepolicy` 這一套件對於查詢布林值的說明、域之間通訊情況等非常方便，可以查 man 手冊以詳細瞭解。還有命令的替換關係，比如 :code:`sepolicy generate` 替換了之前的 :code:`sepolgen`。

常用的最最基本的工具，大概是 :code:`semanage`, :code:`restorecon`, :code:`chcon`, :code:`fixfiles`, :code:`setsebool`, :code:`getsebool`, :code:`sestatus`, :code:`avcstat`, :code:`setenforce`, :code:`getenforce`, :code:`sesearch`, :code:`sepolicy`, :code:`matchpathcon`.

還有一個 :code:`ausearch` 屬於審計一塊的，但是用於查詢 SELinux 的報錯非常有效，需要查 man 手冊詳細瞭解記住，並活用。

SELinux 配置檔案
==================================================

以 CentOS 7 為例， :code:`/etc/selinux/config` 為 SELinux 的主配置檔案，它控制著 SELinux 的啟用與禁用，啟用的模式和使用的策略。

以預設的 enforcing 模式和 targeted 策略為例，該策略的配置檔案在 :code:`/etc/selinux/targeted` 目錄下，如果是其它的策略的話，配置檔案同樣需要在 :code:`/etc/selinux/{對應策略名}` 目錄下。

比如預設已經配置好的檔案 SELinux 上下文屬性分配規則在 :code:`/etc/selinux/targeted/contexts/files/file_contexts` 檔案內，而如果使用了 :code:`semanage` 自定義了的話，則會在 :code:`/etc/selinux/targeted/contexts/files/file_contexts.local` 檔案內。注意的是不要直接去修改檔案內的內容。

SELinux 上下文組成
==================================================

SELinux 上下文格式為 :code:`se_user:role:type:level` ，也就是由這四個欄位組成，可以看本文最開始那條命令的輸出，以下是欄位說明：

se_user
  SELinux user 是被策略已知的身份，該身份確定了一組特定的規則和一個 MLS/MSC 範圍。每個 Linux 使用者都會通過 SELinux 策略被對映到一個 SELinux 使用者，這使得 Linux 使用者繼承了對應 SELinux 使用者的一些限制。SELinux 使用者身份被用在其會話裡程序的 SELinux 上下文資訊中，用於定義該程序以什麼規則和級別執行。
  
  以 root 使用者執行以下命令：

  .. code-block:: shell-session

    # semanage login -l

    Login Name           SELinux User         MLS/MCS Range        Service

    __default__          unconfined_u         s0-s0:c0.c1023       *
    root                 unconfined_u         s0-s0:c0.c1023       *
    system_u             system_u             s0-s0:c0.c1023       *

  可以看到顯示了 Linux 使用者和 SELinux 的對映關係。如果系統不支援 MLS/MCS 的話，那麼最後兩列則應該不會顯示（查到的資料上示例是在這樣子的，我並沒有不支援 MLS/MCS 的環境來測試驗證），以下是每個欄位的介紹：

  * Login Name 表示匹配的 Linux 使用者，以 :code:`%` 開頭的代表匹配到一個組。如果沒有任何匹配項則匹配 :code:`__default__` 行的規則。
  * SELinux User 表示匹配到的 Linux 使用者所對應的 SELinux 使用者，這裡的使用者必須是已經有配置好存在的，可以在 :code:`/etc/selinux/{POLICYNAME}/contexts/users/` 目錄下找到。
  * MLS/MCS Range 則表示 Multi-Level Security 和 Multi-Category Security 所使用的級別，下文將詳細描述。
  * Service 列則是用於判斷從什麼服務（這裡的服務需要是可以以之登入的 PAM 服務）登入的使用者採用什麼 SELinux 上下文屬性，不過 :code:`semanage` 工具是沒有提供相應的設定的，但可以直接修改 :code:`/etc/selinux/{POLICYNAME}/logins/` 資料夾下的對應使用者名稱的檔案，比如要修改從 sshd 登入的 root 使用者的 SELinux user 為 :code:`user_u` 的話，新建一個 :code:`/etc/selinux/targeted/logins/root` 檔案，新增內容 :code:`sshd:user_u:s0` 到檔案內，詳細的可以看 `Google Books 上`_ 搜尋到的說明。

  :code:`system_u` 行是給系統程序所使用的，一般不用去考慮它。而登入時使用者的上下文確認則依賴於 :code:`/etc/selinux/{POLICYNAME}/contexts/users/` 目錄下的配置檔案，執行 :code:`man user_contexts` 檢視詳細的說明。如果說在 :code:`/etc/selinux/{POLICYNAME}/contexts/users/` 目錄下的配置檔案配置不正確，那麼會從 :code:`/etc/selinux/{POLICYNAME}/contexts/default_context` 檔案下獲取預設的配置。

role
  Role-Based Access Control 是 SELinux 的一部分，role 就是其屬性。其根據 SELinux user 來確定 role，再根據 role 來確定一個域。所以 role 相當於是 SELinux 使用者與各類域間的服務體，確定了 role 就可以確定程序所屬域，最終控制何種 object type 可以被訪問。這一系列的判斷降低了提權攻擊的風險。注意的是 RBAC 是用於程序而並非檔案的，對於檔案來說，角色並沒有什麼意義，檔案上所賦予的 :code:`object_r` role 是持久化儲存和網路檔案系統上給檔案的一個通用化角色，不過在 :code:`/proc` 資料夾下，一些和程序相關的檔案的角色可能是 :code:`system_r` 。
  
  SElinux user 與 role 的對應策略可以通過如下命令檢視：

  .. code-block:: shell-session

    # semanage user -l

                    Labeling   MLS/       MLS/                          
    SELinux User    Prefix     MCS Level  MCS Range                      SELinux Roles

    guest_u         user       s0         s0                             guest_r
    root            user       s0         s0-s0:c0.c1023                 staff_r sysadm_r system_r unconfined_r
    staff_u         user       s0         s0-s0:c0.c1023                 staff_r sysadm_r system_r unconfined_r
    sysadm_u        user       s0         s0-s0:c0.c1023                 sysadm_r
    system_u        user       s0         s0-s0:c0.c1023                 system_r unconfined_r
    unconfined_u    user       s0         s0-s0:c0.c1023                 system_r unconfined_r
    user_u          user       s0         s0                             user_r
    xguest_u        user       s0         s0                             xguest_r
  
  一條記錄對應有多個 roles 則意味著該 SELinux user 可以在記錄的 roles 之間切換，可以使用 :code:`newrole` 命令來切換。

  而 role 所允許被分配的域型別則可以通過如下命令來檢視：

  .. code-block:: shell-session

    # seinfo -ruser_r -x
       user_r
           Dominated Roles:
             user_r
           Types:
             abrt_helper_t
             alsa_home_t
             antivirus_home_t
             httpd_user_content_t
             httpd_user_htaccess_t
             ...

  舉個許可權的例子，比如需要執行 :code:`sudo` 命令，可以看到其 SELinux 上下文下的 object type 為 :code:`sudo_exec_t` ，然後來做以下幾個資訊的查詢（這邊感謝 irc 頻道 #selinux 裡的 grift 提點關聯屬性概念）：

  * :code:`sudo_exec_t` 的關聯屬性有哪些：

    .. code-block:: shell-session

      # seinfo -xtsudo_exec_t
         sudo_exec_t
             application_exec_type
             entry_type
             exec_type
             file_type
             non_auth_file_type
             non_security_file_type

  * :code:`user_r` 角色對應的 :code:`user_t` 域是否有對該 object type 的直接規則以允許其執行許可權：

    .. code-block:: shell-session

      # sesearch -A -suser_t -d -tsudo_exec_t

      #

  * :code:`user_t` 域是否有對該 object type 關聯屬性的規則來執行：

    .. code-block:: shell-session

      # sesearch -ASCT -suser_t -tsudo_exec_t
      Found 3 semantic av rules:
        allow user_t application_exec_type : file { ioctl read getattr lock execute execute_no_trans open } ; 
        allow user_usertype file_type : filesystem getattr ; 
        allow user_usertype application_exec_type : file { ioctl read getattr lock execute execute_no_trans open } ; 

    所以雖然該域沒有對該 object type 的直接規則用於執行，但是該域本身被賦予了對具有 :code:`application_exec_type` 屬性的 object type 的執行等許可權，所以執行是沒有問題：

    .. code-block:: shell-session

      $ sudo -i
      sudo: PERM_SUDOERS: setresuid(-1, 1, -1): Operation not permitted
    
    但是操作還是被拒絕了，從提示資訊就可以看到是 setuid 操作被拒，進一步檢視詳細資訊：

    .. code-block:: shell-session

      # audit2why -al | tail
                      Missing type enforcement (TE) allow rule.

                      You can use audit2allow to generate a loadable module to allow this access.

      type=AVC msg=audit(1498119023.011:274): avc:  denied  { setuid } for  pid=2944 comm="sudo" capability=7  scontext=user_u:user_r:user_t:s0 tcontext=user_u:user_r:user_t:s0 tclass=capability
              Was caused by:
                      Missing type enforcement (TE) allow rule.

                      You can use audit2allow to generate a loadable module to allow this access.
    
    很明確地說明了 :code:`user_t` 域下是沒有 setuid 的能力的，如下命令檢視其擁有的能力：

    .. code-block:: shell-session

      # sesearch -ASCT -suser_t -tuser_t | grep capability
         allow user_t user_t : capability { chown fowner setgid net_bind_service sys_chroot audit_write } ; 
      DT allow user_t user_t : capability sys_chroot ; [ selinuxuser_use_ssh_chroot ]
    
    所以 :code:`user_r` 這個角色預設是不能執行 :code:`sudo` 的。而 :code:`staff_r` 這個角色可以，但是參考上述規則檢視後會發現其同樣沒有對自身域 :code:`staff_t` 的 setuid 能力，可以執行的原因是當其在執行 :code:`sudo` 命令時，有域過渡規則規定其過渡到 :code:`staff_sudo_t` 域下（這邊同樣需要注意該 role 是否允許被分配該域，參考上文命令），該域則有 setuid 的能力。以下命令檢視過渡規則：

    .. code-block:: shell-session

      # sesearch -T -sstaff_t | grep sudo_exec_t
         type_transition staff_t sudo_exec_t : process staff_sudo_t;
  
  本段連帶著也解釋了下 type 的相關用法，它們本就是需要互相結合使用的。

type
  Type 是 Type Enforcement (TE) 的屬性，為程序定義了域，為檔案定義了型別。SELinux 策略規則定義了什麼樣的型別可以互相訪問，無論是域去訪問型別，還是域之間的訪問。只有當 SELinux 策略規則顯示的定義了的時候，訪問才被允許。注意的是 TE 是 SELinux 的主要控制手段，大部分情況下， SELinux user 和 role 是可以被忽略的。下文有一個例子是圍繞 TE 做詳細介紹的。

level
  Level 是 Multi-Level Security (MLS) 和 Multi-Category Security (MCS) 的屬性，其中 MCS 是 MLS 的特殊實現。一個 MLS 範圍是一對級別，當兩個級別不同時的書寫格式為 :code:`低級別-高級別` ；當兩個級別相同時可直接書寫為 :code:`低級別` ( :code:`s0-s0` 和 :code:`s0` 是一樣的)。每一個 level 都是靈敏度-分類 (sensitivity-category) 的組合， category 是可選的。當存在有 category 的時候，level 的格式為 :code:`sensitivity:category-set`，如果 category 不存在，那麼僅寫作 :code:`sensitivity`。 

  如果 category 是一系列連續的，那麼可以簡寫，比如 :code:`c0.c3` 和 :code:`c0,c1,c2,c3` 是相同的。人性化的等級對映關係在檔案 :code:`/etc/selinux/targeted/setrans.conf` 下配置。在 RHEL 系列中，預設的 targeted 策略是強制執行 MCS 的，僅有一個靈敏度 s0，有 1024 個不同的 categories，從 c0 到 c1023。 s0-s0:c0.c1023 是針對所有 categories 的 sensitivity 0 級別。

  本文不會涉及 MLS/MCS 這一塊的詳細說明。

舉個例子來解釋 TE 為主的基本用法/原理
==================================================

之前 `有一篇文章`_ 寫的是在啟用 SELinux 情況下部署 NextCloud 的，這裡詳細說明配置 SELinux 部分，並介紹一些基本原理。

* 環境： CentOS 7， 原始碼編譯安裝的 Nginx 以及 PHP-FPM， 匯入官方倉庫後使用 :code:`yum` 命令安裝的 MariaDB 10.1
* 目的： 配置好 SELinux 上下文屬性，使得網站得以正常執行
* 總覽：

  * MariaDB 是使用 :code:`yum` 直接從匯入的 MariaDB 官方倉庫下安裝的，所有的檔案的安裝路徑包含在預配置好的 SELinux 上下文內，而我對其資料庫檔案儲存路徑進行了自定義，所以只需要對新的資料庫檔案儲存路徑進行配置即可。
  * Nginx 和 PHP-FPM 是從原始碼編譯安裝的，且路徑設定都不為預設，所以相應的全部檔案的 SELinux 上下文都需要進行配置。
  * 此處不考慮任何 DAC 方面的問題，假定 DAC 均為允許。

* 步驟：

  * **配置 MariaDB 資料庫儲存路徑的 SELinux 上下文資訊**

    我自定義的 MariaDB 資料庫儲存路徑為 :code:`/o/db/data/mariadb` ，可以顯而易見的是 mariadb 程序需要對這個路徑有可讀可寫的許可權，那先來看一下 mariadb 守護程序執行工具的 SELinux 上下文資訊：

    .. code-block:: shell-session

      # ls -Z /usr/sbin/mysqld 
      -rwxr-xr-x. root root system_u:object_r:mysqld_exec_t:s0 /usr/sbin/mysqld

    把關注點放在 :code:`mysqld_exec_t` 這個 SELinux object type 上，是否有對一個檔案進行讀寫執行等各種各樣的許可權是要以程序所在的域型別（也就是 subject type）來進行判斷的，擁有正確的 SELinux 上下文的可執行檔案，在執行時會因為當前所在域不同而使執行程序進入到不同的域下，這便是域過渡。可以通過命令來檢視到過渡規則：

    .. code-block:: shell-session

      # sesearch -T -tmysqld_exec_t
      Found 11 semantic te rules:
        type_transition openshift_initrc_t mysqld_exec_t : process mysqld_t; 
        type_transition piranha_pulse_t mysqld_exec_t : process mysqld_t; 
        type_transition init_t mysqld_exec_t : process mysqld_t; 
        type_transition kdumpctl_t mysqld_exec_t : process mysqld_t; 
        type_transition condor_startd_t mysqld_exec_t : process mysqld_t; 
        type_transition cluster_t mysqld_exec_t : process mysqld_t; 
        type_transition svc_run_t mysqld_exec_t : process mysqld_t; 
        type_transition mysqld_safe_t mysqld_exec_t : process mysqld_t; 
        type_transition glusterd_t mysqld_exec_t : process mysqld_t; 
        type_transition mysqlmanagerd_t mysqld_exec_t : process mysqld_t; 
        type_transition initrc_t mysqld_exec_t : process mysqld_t; 

    可以看到只有上述 :code:`cluster_t`, :code:`init_t` 等 11 個域才有與 :code:`mysqld_exec_t` 相關的域過渡規則，且只能過渡到 :code:`mysqld_t` 下。然後再來看當前 bash 程序的域型別和當前使用者的 SELinux 上下文：

    .. code-block:: shell-session

      # ps auxfZ | grep bash
      unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023 uuu 6243 0.0  0.5 115392 3100 pts/0 Ss 19:04   0:00          \_ -bash
      unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023 root 6267 0.0  0.5 115484 3276 pts/0 S 19:04   0:00                  \_ -bash
      # id -Z
      unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023

    當前 bash 程序所在域由其對應的使用者所確定，在沒有配置的情況下，所在域型別便是 :code:`unconfined_t` 了，很明顯 :code:`mysqld_exec_t` 沒有針對 :code:`unconfined_t` 域的過渡規則，那麼直接執行就會導致其程序所在域仍然處於 :code:`unconfined_t` 域下：

    .. code-block:: shell-session

      # sed -i '/\[mysqld\]/auser=root' /etc/my.cnf.d/server.cnf
      # /usr/sbin/mysqld > /dev/null 2>&1 &
      [1] 10210
      # ps -eZ | grep mysqld
      unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023 10210 pts/0 00:00:00 mysqld
      # sed -i '/user=root/d' /etc/my.cnf.d/server.cnf
    
    雖然不會影響到正常執行，但預設情況下在這個域下程序基本相當於和沒有 SELinux 一樣了，很不安全。

    不過通常情況下都是使用 systemdctl 來呼叫 systemd daemon 來執行的，檢視 systemd 程序的 SELinux 上下文資訊，可以看到：

    .. code-block:: shell-session

      # ps -eZ | grep systemd
      system_u:system_r:init_t:s0         1 ?        00:01:51 systemd

    其域型別便是 :code:`init_t` ，所以由它執行的 mysqld 可以過渡到 :code:`mysqld_t` 域下：

    .. code-block:: shell-session

      # systemctl start mariadb
      # ps -eZ | grep mysqld
      system_u:system_r:mysqld_t:s0    7385 ?        00:00:00 mysqld
    
    明確了 mariadb 執行程序所在的域，接下來就是明確需要給自定義資料庫路徑設定的 SELinux 上下文的 object type 了。同樣可以先通過命令來檢視哪個 type 符合要求：

    .. code-block:: shell-session

      # sesearch -A -d -s mysqld_t | egrep ' file | dir ' | grep 'read write'
         allow mysqld_t mysqld_tmp_t : file { ioctl read write create getattr setattr lock append unlink link rename open } ; 
         allow mysqld_t mysqld_var_run_t : dir { ioctl read write create getattr setattr lock unlink link rename add_name remove_name reparent search rmdir open } ; 
         allow mysqld_t mysqld_log_t : dir { ioctl read write create getattr setattr lock unlink link rename add_name remove_name reparent search rmdir open } ; 
         allow mysqld_t var_run_t : dir { ioctl read write getattr lock add_name remove_name search open } ; 
         allow mysqld_t mysqld_log_t : file { ioctl read write create getattr setattr lock append unlink link rename open } ; 
         allow mysqld_t mysqld_tmp_t : dir { ioctl read write create getattr setattr lock unlink link rename add_name remove_name reparent search rmdir open } ; 
         allow mysqld_t mysqld_var_run_t : file { ioctl read write create getattr setattr lock append unlink link rename open } ; 
         allow mysqld_t tmp_t : dir { ioctl read write getattr lock add_name remove_name search open } ; 
         allow mysqld_t var_log_t : dir { ioctl read write getattr lock add_name remove_name search open } ; 
         allow mysqld_t faillog_t : dir { ioctl read write create getattr setattr lock unlink link rename add_name remove_name reparent search rmdir open } ; 
         allow mysqld_t mysqld_t : file { ioctl read write getattr lock append open } ; 
         allow mysqld_t hugetlbfs_t : file { ioctl read write getattr lock append open } ; 
         allow mysqld_t mysqld_db_t : file { ioctl read write create getattr setattr lock append unlink link rename open } ; 
         allow mysqld_t var_lib_t : dir { ioctl read write getattr lock add_name remove_name search open } ; 
         allow mysqld_t faillog_t : file { ioctl read write create getattr setattr lock append unlink link rename open } ; 
         allow mysqld_t lastlog_t : file { ioctl read write create getattr setattr lock append open } ; 
         allow mysqld_t mysqld_db_t : dir { ioctl read write create getattr setattr lock unlink link rename add_name remove_name reparent search rmdir open } ; 
         allow mysqld_t krb5_host_rcache_t : dir { ioctl read write getattr lock add_name remove_name search open } ; 
         allow mysqld_t krb5_host_rcache_t : file { ioctl read write create getattr setattr lock append unlink link rename open } ; 
         allow mysqld_t tmp_t : dir { ioctl read write getattr lock add_name remove_name search open } ; 
         allow mysqld_t security_t : file { ioctl read write getattr lock append open } ;
    
    可以看到有很多的 object type 都滿足我的 read, write 許可權的要求，其中有一個 type 的名稱為 :code:`mysqld_db_t` ，很能說明問題，從其擁有的許可權來看，很明顯 read, write 兩個許可權是不夠用的（關於許可權所對應的各種操作以後再說），那麼就用它了。接下來就是對新路徑配置 SELinux 上下文資訊了：

    .. code-block:: shell-session

      # semanage fcontext -a -t mysqld_db_t '/o/db/data/mariadb(/.*)?'
      # restorecon -Rv /o/db/data/mariadb
    
    第一條命令是對 :code:`/o/db/data/mariadb` 資料夾及其所有子內容持久化設定相應的 SELinux 上下文的 object type，因為這條命令不會使之及時生效，所以需要第二條命令配合，使得其及時生效。

    這樣子對於 MariaDB 下自定義的資料庫儲存路徑的設定就好了。

  * **配置 Nginx 的 SELinux 上下文資訊**

    在這裡雖然沒有現有的執行檔案可以用來做參考，但是預設的規則卻是在的。所以搜尋檔案 :code:`/etc/selinux/targeted/contexts/files/file_contexts` 下的 :code:`/usr/sbin/nginx` 欄位，就可以知道預設情況下對 nginx 分配的執行域是什麼了。參考上述 MariaDB 過程，可以查到其執行域型別為 :code:`httpd_t` ，同樣參考上述 MariaDB 過程可以對 Nginx 程序需要的指定系統檔案配置 object type 為 :code:`httpd_sys_content_t` ，而對需要讀寫的系統檔案配置 object type 為 :code:`httpd_sys_rw_content_t` ，需要可以讓 :code:`httpd_t` 域直接執行的檔案配置 object type 為 :code:`httpd_sys_script_exec_t` 。如何配置的話，同樣是使用 :code:`semanage` 命令。

    可能在這裡會需要複製幾個原先配置好的配置檔案到當前 Nginx 的配置目錄，那麼就需要注意在檔案複製/移動過程中的 SELinux 上下文變化，比如：

    .. code-block:: shell-session

      # ls -Z ~/i.conf 
      -rw-r--r--. root root unconfined_u:object_r:admin_home_t:s0 /root/i.conf
      # ls -dZ /o/conf/nginx/conf.d
      drwxr-xr-x. root root unconfined_u:object_r:httpd_sys_content_t:s0 /o/conf/nginx/conf.d
      # cp ~/i.conf /o/conf/nginx/conf.d/
      # ls -Z /o/conf/nginx/conf.d/i.conf 
      -rw-r--r--. root root unconfined_u:object_r:httpd_sys_content_t:s0 /o/conf/nginx/conf.d/i.conf
      # rm /o/conf/nginx/conf.d/i.conf 
      rm: remove regular file ‘/o/conf/nginx/conf.d/i.conf’? y
      # mv i.conf /o/conf/nginx/conf.d/
      # ls -Z /o/conf/nginx/conf.d/i.conf 
      -rw-r--r--. root root unconfined_u:object_r:admin_home_t:s0 /o/conf/nginx/conf.d/i.conf
      # mv /o/conf/nginx/conf.d/i.conf ~/
      # touch /o/conf/nginx/conf.d/i.conf
      # chcon -t etc_t /o/conf/nginx/conf.d/i.conf 
      # ls -Z /o/conf/nginx/conf.d/i.conf 
      -rw-r--r--. root root unconfined_u:object_r:etc_t:s0   /o/conf/nginx/conf.d/i.conf
      # ls -Z ~/i.conf 
      -rw-r--r--. root root unconfined_u:object_r:admin_home_t:s0 /root/i.conf
      # cp ~/i.conf /o/conf/nginx/conf.d/i.conf 
      cp: overwrite ‘/o/conf/nginx/conf.d/i.conf’? y
      # ls -Z /o/conf/nginx/conf.d/i.conf 
      -rw-r--r--. root root unconfined_u:object_r:etc_t:s0   /o/conf/nginx/conf.d/i.conf
      # cp --preserve=context ~/i.conf /o/conf/nginx/conf.d/i.conf 
      cp: overwrite ‘/o/conf/nginx/conf.d/i.conf’? y
      # ls -Z /o/conf/nginx/conf.d/i.conf 
      -rw-r--r--. root root unconfined_u:object_r:admin_home_t:s0 /o/conf/nginx/conf.d/i.conf
      # chcon -t etc_t /o/conf/nginx/conf.d/i.conf 
      # ls -Z /o/conf/nginx/conf.d/i.conf 
      -rw-r--r--. root root unconfined_u:object_r:etc_t:s0   /o/conf/nginx/conf.d/i.conf
      # mv ~/i.conf /o/conf/nginx/conf.d/i.conf 
      mv: overwrite ‘/o/conf/nginx/conf.d/i.conf’? y
      # ls -Z /o/conf/nginx/conf.d/i.conf 
      -rw-r--r--. root root unconfined_u:object_r:admin_home_t:s0 /o/conf/nginx/conf.d/i.conf
    
    可以看到，在複製檔案的時候，如果目標檔案不存在，則會保留原始檔的 SELinux 上下文資訊，而如果目標檔案存在，則會保留原目標檔案的 SELinux 上下文資訊，不過也可以通過使用引數 :code:`--preserve=context` 保留原始檔的 SELinux 上下文資訊。

    在移動檔案的時候，則是保留原始檔的 SELinux 上下文資訊而不管目標檔案是否存在。

    命令 :code:`matchpathcon` 可以方便地檢查檔案（夾）的 SELinux 上下文與系統配置是否一致，比如：

    .. code-block:: shell-session

      # matchpathcon -V /o/conf/nginx/conf.d/* | grep -v 'verified\.$'
      /o/conf/nginx/conf.d/i.conf has context unconfined_u:object_r:admin_home_t:s0, should be system_u:object_r:httpd_sys_content_t:s0

  * **配置 PHP-FPM 的 SELinux 上下文資訊**

    PHP-FPM 所預設的執行域同樣是 :code:`httpd_t` ，上述類似的不再說明。不過在這裡有一個需求是，在 web 應用執行的過程中，需要和資料庫進行通訊，如果資料庫有監聽著的 unix socket 檔案的話，那麼直接設定好改檔案的 SELinux 許可權就可以讓 PHP-FPM 來通訊了，可如果是監聽的 tcp socket 的話，那麼就依賴 SELinux 的另一個屬性，布林值。布林值的設定允許在執行時修改部分 SELinux 策略，而不需要任何 SELinux 策略的書寫知識（那我的理解就是這些個屬性所控制的許可權在沒有布林值的情況下只能通過修改 SELinux 策略來修改而不是簡單配置幾下就行的了）。檢視布林值可以使用如下命令：

    .. code-block:: shell-session

      # getsebool -a | grep <pattern or str>
    
    還有一個命令可以很方便的檢視對應布林值的說明：

    .. code-block:: shell-session

      # sepolicy booleans -a | grep httpd_can
      httpd_can_check_spam=_("Allow http daemon to check spam")
      httpd_can_connect_ftp=_("Allow httpd to act as a FTP client connecting to the ftp port and ephemeral ports")
      httpd_can_connect_ldap=_("Allow httpd to connect to the ldap port")
      ...
      # sepolicy booleans -b httpd_can_network_connect
      httpd_can_network_connect=_("Allow HTTPD scripts and modules to connect to the network using TCP.")

    這樣子就一目瞭然了，以下命令用於設定布林值：

    .. code-block:: shell-session

      # setsebool -P httpd_can_network_connect on
    
    :code:`-P` 選項是對其進行持久化儲存到硬碟上的，不然重啟後設置就失效了。這幾個命令的選項都很少， man 一下就可以看得很清楚。

  * **查錯**

    一次性可能不會完全配置正確且無遺漏，那麼檢視 SELinux 的審計日誌就非常重要了。

    CentOS 7 下預設是有執行 auditd 的，所以一般而言可以使用如下命令來檢視有的報錯：

    .. code-block:: bash

      ausearch -i -m AVC,USER_AVC,SELINUX_ERR -ts today

    其日誌檔案的位置預設為 :code:`/var/log/audit/audit.log` ，而關於其各欄位的含義，可以看這篇文章 `UNDERSTANDING AUDIT LOG FILES`_ 。

    還有一個命令是 :code:`audit2why` 可以方便的把拒絕日誌資訊轉化為更易讀的格式。

* 總結： 通過上述的各種工具進行組合重複，就可以完成實現目的的所有設定。所以單就配置本身而言， SELinux 還是比較簡單的，但是如果各種服務一多，功能一複雜，所需要考慮的屬性，檔案擴充套件屬性，各種域之間的聯絡就會使配置 SELinux 變得複雜。那麼在不考慮編寫 SELinux 策略而僅僅是實用現有策略的情況下，掌握 SELinux 更多的就是靠經驗積累了。

而更多的配置/說明/例子，比如限制與非限制使用者， :code:`file_t` 和 :code:`default_t` ，檔案系統掛載配置，檔名過渡，禁用 ptrace()， sVirt 等等很多內容，可以看本文最開始提到的那篇文章，或者其它更深入描述的文章。

以上。

.. [1] Linux 下的自主訪問控制就是平常最基本的對檔案（夾）進行設定使用者名稱/組以及相應的 :code:`wrxst` 許可權，然後以使用者身份來執行，這樣子的一種訪問控制管理簡單但安全係數不高，一旦獲取某一個使用者的許可權就可以做該使用者能做的任何事情，還可以較為簡單地進行提權攻擊等。

.. _`SELinux User's and Administrator's Guide`: https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/SELinux_Users_and_Administrators_Guide/index.html
.. _`本人整理的工具列表`: https://gist.github.com/Bekcpear/590580d46bf739d3a58675212a2e7316
.. _`Google Books 上`: https://books.google.com/books?id=E8_cDgAAQBAJ&pg=PA70&dq=%22semanage+login+-l%22+Service&hl=en&sa=X&ved=0ahUKEwjN4LWN883UAhUP5WMKHZFrCK0Q6AEINTAC#v=onepage&q=%22semanage%20login%20-l%22%20Service&f=false
.. _`有一篇文章`: /build_nextcloud_service_on_centos_with_selinux.html#selinux-nextcloud
.. _`UNDERSTANDING AUDIT LOG FILES`: https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Security_Guide/sec-Understanding_Audit_Log_Files.html
.. _`SELinux User's and Administrator's Guide 第二章節 SELINUX CONTEXTS 的部分內容`: https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/SELinux_Users_and_Administrators_Guide/chap-Security-Enhanced_Linux-SELinux_Contexts.html
.. _`Creative Commons Attribution-ShareAlike 3.0 Unported License`: http://creativecommons.org/licenses/by-sa/3.0/
