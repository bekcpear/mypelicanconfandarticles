========================================
初识 SELinux
========================================

:slug: understanding_selinux
:date: 2017-06-22 18:21
:lang: zh
:tags: selinux
:description: 以 CentOS 为平台整理了入门 SELinux 所需要掌握的最基本知识，围绕例子来进行说明。

.. contents::

这是我第一次写关于 SELinux 的文章， SELinux 是一个比较庞大的强制访问控制方案，单单就控制原理而言是相对简单易懂的，复杂的是各种规则间的联系和束缚，以及如何选择。本文会从我对其理解的角度进行书写，关注点主要是实现和应用。

我是看的 Red Hat 的 `SELinux User's and Administrator's Guide`_ 入的门，本文则会使用我自己的话来进行总结和概括，以便于快速入门，看源链接的文档则可以更详细的了解到 SELinux，但有些内容比如各种策略的选择，工具的选择和介绍却是上文所缺乏的，我单独整理的也会在下文描述。

鉴于本文很基础，所以几个基本的名词我都会在文中以适当的形式说明。

| *注： 关于部分有争议的名词我不准备用中文表示，比如 type,class,subject 等等，被写成中文的均是我力所能及下认为绝对不会有争议或者本身就可以用中文描述的*
| *注： 本文不会涉及到 SELinux 的 MLS 策略*

什么是 SELinux 以及如何理解它
==================================================

:ruby:`安全增强型 Linux| Security-Enhanced Linux` 是 Linux 内核下的一个安全模块，它在 Linux :ruby:`自主访问控制|Discretionary Access Control` [1]_ 的基础上提供了额外的访问控制安全策略，它提供的控制组合为 :ruby:`以角色为基础的访问控制|Role-Based Access Control` (RBAC)， Type Enforcement (TE) 和可选的 Multi-Level Security (MLS)。需要明确的是 SELinux 是用来强化已有的安全系统的，而绝对不是用来替代的。

列出一条查看当前文件（夹） SELinux 上下文属性的命令:

.. code-block:: shell-session

  # ls -Z test
  -rwxr-xr-x. root root unconfined_u:object_r:admin_home_t:s0 test

一个相当熟悉的命令 :code:`ls` ，就像平常使用 :code:`ls -l` 查看文件的详细信息一样。所以由此让我对 SELinux 的理解变成了其为组成 Linux 系统安全的最基本的一部分，必须掌握。

明确两个名词:

Object
  所有的文件，包括文件夹、软链接、设备等，都被理解为 Object。

Subject
  Linux 下的进程。

简述权限审查过程
------------------------------------------------------------

.. ditaa::
  :alt: selinux 处理流程

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

上图是在启用 SELinux 情况下的一个 Linux 权限审查过程，当用户空间下的一个进程需要系统调用时，首先会进行 DAC 检查，只有 DAC 检查通过的才会进行 SELinux 的策略验证，最后判断是否允许被调用。针对 SELinux 的策略所决定的是否允许执行的某一操作，会被缓存在 :ruby:`访问向量缓存|Access Vector Cache` (AVC) 内，以提高执行效率。

SELinux 的默认策略为 targeted （也是推荐的），在这个策略下，Type Enforcement (TE) 是主要的的权限控制手段，大多数情况下， SELinux 用户和角色都是可以忽略的。也就是说关注点在 :code:`admin_home_t` 这个 type 属性上。

拥有相同域类型的进程运行于同一个域下，不同域下的进程在没有相应的 SELinux 策略允许的情况下是不能互相访问和操作的。注意的是，默认情况下的 Linux 用户运行在 :code:`unconfined_t` 域（后文以非非限制性域描述）下，而由该域下用户所直接执行的命令对应的进程大部分同样是处于该域的，虽然对于非限制性域下的进程而言，SELinux 策略也是会起作用的，但目前存在的策略规则对非限制性域下进程开放几乎所有的访问权限，相当于 SELinux 不起作用了，仅靠 DAC 来做权限控制。所以这边就引入到一个处理方式，叫做 :ruby:`域过渡|Domain transitions` ，会在下文详细描述用法。

简而言之就是，进程所属的域类型确定了该进程所拥有的权限，由 SELinux 策略规则来控制。

CentOS 下 SELinux 工具及对应的包
==================================================

`本人整理的工具列表`_ ，一般来说就是 Red Hat 系所通用的了，其它发行版大致也应该一样。

其中， :code:`semodule_unpackage`, :code:`sepolicy`, :code:`sefcontext_compile`, :code:`selabel_digest`, :code:`selabel_lookup`, :code:`selabel_lookup_best_match`, :code:`selabel_partial_match`, :code:`selinuxexeccon`, :code:`selinux_restorecon` 这些工具我在 CentOS 6 下则并未找到， CentOS 7 下才可以安装到。

CentOS 7 下的 :code:`sepolicy` 这一套件对于查询布尔值的说明、域之间通讯情况等非常方便，可以查 man 手册以详细了解。还有命令的替换关系，比如 :code:`sepolicy generate` 替换了之前的 :code:`sepolgen`。

常用的最最基本的工具，大概是 :code:`semanage`, :code:`restorecon`, :code:`chcon`, :code:`fixfiles`, :code:`setsebool`, :code:`getsebool`, :code:`sestatus`, :code:`avcstat`, :code:`setenforce`, :code:`getenforce`, :code:`sesearch`, :code:`sepolicy`, :code:`matchpathcon`.

还有一个 :code:`ausearch` 属于审计一块的，但是用于查询 SELinux 的报错非常有效，需要查 man 手册详细了解记住，并活用。

SELinux 配置文件
==================================================

以 CentOS 7 为例， :code:`/etc/selinux/config` 为 SELinux 的主配置文件，它控制着 SELinux 的启用与禁用，启用的模式和使用的策略。

以默认的 enforcing 模式和 targeted 策略为例，该策略的配置文件在 :code:`/etc/selinux/targeted` 目录下，如果是其它的策略的话，配置文件同样需要在 :code:`/etc/selinux/{对应策略名}` 目录下。

比如默认已经配置好的文件 SELinux 上下文属性分配规则在 :code:`/etc/selinux/targeted/contexts/files/file_contexts` 文件内，而如果使用了 :code:`semanage` 自定义了的话，则会在 :code:`/etc/selinux/targeted/contexts/files/file_contexts.local` 文件内。注意的是不要直接去修改文件内的内容。

SELinux 上下文组成
==================================================

SELinux 上下文格式为 :code:`se_user:role:type:level` ，也就是由这四个字段组成，可以看本文最开始那条命令的输出，以下是字段说明：

se_user
  SELinux user 是被策略已知的身份，该身份确定了一组特定的规则和一个 MLS/MSC 范围。每个 Linux 用户都会通过 SELinux 策略被映射到一个 SELinux 用户，这使得 Linux 用户继承了对应 SELinux 用户的一些限制。SELinux 用户身份被用在其会话里进程的 SELinux 上下文信息中，用于定义该进程以什么规则和级别运行。
  
  以 root 用户执行以下命令：

  .. code-block:: shell-session

    # semanage login -l

    Login Name           SELinux User         MLS/MCS Range        Service

    __default__          unconfined_u         s0-s0:c0.c1023       *
    root                 unconfined_u         s0-s0:c0.c1023       *
    system_u             system_u             s0-s0:c0.c1023       *

  可以看到显示了 Linux 用户和 SELinux 的映射关系。如果系统不支持 MLS/MCS 的话，那么最后两列则应该不会显示（查到的资料上示例是在这样子的，我并没有不支持 MLS/MCS 的环境来测试验证），以下是每个字段的介绍：

  * Login Name 表示匹配的 Linux 用户，以 :code:`%` 开头的代表匹配到一个组。如果没有任何匹配项则匹配 :code:`__default__` 行的规则。
  * SELinux User 表示匹配到的 Linux 用户所对应的 SELinux 用户，这里的用户必须是已经有配置好存在的，可以在 :code:`/etc/selinux/{POLICYNAME}/contexts/users/` 目录下找到。
  * MLS/MCS Range 则表示 Multi-Level Security 和 Multi-Category Security 所使用的级别，下文将详细描述。
  * Service 列则是用于判断从什么服务（这里的服务需要是可以以之登录的 PAM 服务）登录的用户采用什么 SELinux 上下文属性，不过 :code:`semanage` 工具是没有提供相应的设置的，但可以直接修改 :code:`/etc/selinux/{POLICYNAME}/logins/` 文件夹下的对应用户名的文件，比如要修改从 sshd 登录的 root 用户的 SELinux user 为 :code:`user_u` 的话，新建一个 :code:`/etc/selinux/targeted/logins/root` 文件，添加内容 :code:`sshd:user_u:s0` 到文件内，详细的可以看 `Google Books 上`_ 搜索到的说明。

  :code:`system_u` 行是给系统进程所使用的，一般不用去考虑它。而登录时用户的上下文确认则依赖于 :code:`/etc/selinux/{POLICYNAME}/contexts/users/` 目录下的配置文件，运行 :code:`man user_contexts` 查看详细的说明。如果说在 :code:`/etc/selinux/{POLICYNAME}/contexts/users/` 目录下的配置文件配置不正确，那么会从 :code:`/etc/selinux/{POLICYNAME}/contexts/default_context` 文件下获取默认的配置。

role
  Role-Based Access Control 是 SELinux 的一部分，role 就是其属性。其根据 SELinux user 来确定 role，再根据 role 来确定一个域。所以 role 相当于是 SELinux 用户与各类域间的服务体，确定了 role 就可以确定进程所属域，最终控制何种 object type 可以被访问。这一系列的判断降低了提权攻击的风险。注意的是 RBAC 是用于进程而并非文件的，对于文件来说，角色并没有什么意义，文件上所赋予的 :code:`object_r` role 是持久化存储和网络文件系统上给文件的一个通用化角色，不过在 :code:`/proc` 文件夹下，一些和进程相关的文件的角色可能是 :code:`system_r` 。
  
  SElinux user 与 role 的对应策略可以通过如下命令查看：

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
  
  一条记录对应有多个 roles 则意味着该 SELinux user 可以在记录的 roles 之间切换，可以使用 :code:`newrole` 命令来切换。

  而 role 所允许被分配的域类型则可以通过如下命令来查看：

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

  举个权限的例子，比如需要执行 :code:`sudo` 命令，可以看到其 SELinux 上下文下的 object type 为 :code:`sudo_exec_t` ，然后来做以下几个信息的查询（这边感谢 irc 频道 #selinux 里的 grift 提点关联属性概念）：

  * :code:`sudo_exec_t` 的关联属性有哪些：

    .. code-block:: shell-session

      # seinfo -xtsudo_exec_t
         sudo_exec_t
             application_exec_type
             entry_type
             exec_type
             file_type
             non_auth_file_type
             non_security_file_type

  * :code:`user_r` 角色对应的 :code:`user_t` 域是否有对该 object type 的直接规则以允许其执行权限：

    .. code-block:: shell-session

      # sesearch -A -suser_t -d -tsudo_exec_t

      #

  * :code:`user_t` 域是否有对该 object type 关联属性的规则来执行：

    .. code-block:: shell-session

      # sesearch -ASCT -suser_t -tsudo_exec_t
      Found 3 semantic av rules:
        allow user_t application_exec_type : file { ioctl read getattr lock execute execute_no_trans open } ; 
        allow user_usertype file_type : filesystem getattr ; 
        allow user_usertype application_exec_type : file { ioctl read getattr lock execute execute_no_trans open } ; 

    所以虽然该域没有对该 object type 的直接规则用于执行，但是该域本身被赋予了对具有 :code:`application_exec_type` 属性的 object type 的执行等权限，所以执行是没有问题：

    .. code-block:: shell-session

      $ sudo -i
      sudo: PERM_SUDOERS: setresuid(-1, 1, -1): Operation not permitted
    
    但是操作还是被拒绝了，从提示信息就可以看到是 setuid 操作被拒，进一步查看详细信息：

    .. code-block:: shell-session

      # audit2why -al | tail
                      Missing type enforcement (TE) allow rule.

                      You can use audit2allow to generate a loadable module to allow this access.

      type=AVC msg=audit(1498119023.011:274): avc:  denied  { setuid } for  pid=2944 comm="sudo" capability=7  scontext=user_u:user_r:user_t:s0 tcontext=user_u:user_r:user_t:s0 tclass=capability
              Was caused by:
                      Missing type enforcement (TE) allow rule.

                      You can use audit2allow to generate a loadable module to allow this access.
    
    很明确地说明了 :code:`user_t` 域下是没有 setuid 的能力的，如下命令查看其拥有的能力：

    .. code-block:: shell-session

      # sesearch -ASCT -suser_t -tuser_t | grep capability
         allow user_t user_t : capability { chown fowner setgid net_bind_service sys_chroot audit_write } ; 
      DT allow user_t user_t : capability sys_chroot ; [ selinuxuser_use_ssh_chroot ]
    
    所以 :code:`user_r` 这个角色默认是不能执行 :code:`sudo` 的。而 :code:`staff_r` 这个角色可以，但是参考上述规则查看后会发现其同样没有对自身域 :code:`staff_t` 的 setuid 能力，可以执行的原因是当其在执行 :code:`sudo` 命令时，有域过渡规则规定其过渡到 :code:`staff_sudo_t` 域下（这边同样需要注意该 role 是否允许被分配该域，参考上文命令），该域则有 setuid 的能力。以下命令查看过渡规则：

    .. code-block:: shell-session

      # sesearch -T -sstaff_t | grep sudo_exec_t
         type_transition staff_t sudo_exec_t : process staff_sudo_t;
  
  本段连带着也解释了下 type 的相关用法，它们本就是需要互相结合使用的。

type
  Type 是 Type Enforcement (TE) 的属性，为进程定义了域，为文件定义了类型。SELinux 策略规则定义了什么样的类型可以互相访问，无论是域去访问类型，还是域之间的访问。只有当 SELinux 策略规则显示的定义了的时候，访问才被允许。注意的是 TE 是 SELinux 的主要控制手段，大部分情况下， SELinux user 和 role 是可以被忽略的。下文有一个例子是围绕 TE 做详细介绍的。

level
  Level 是 Multi-Level Security (MLS) 和 Multi-Category Security (MCS) 的属性，其中 MCS 是 MLS 的特殊实现。一个 MLS 范围是一对级别，当两个级别不同时的书写格式为 :code:`低级别-高级别` ；当两个级别相同时可直接书写为 :code:`低级别` ( :code:`s0-s0` 和 :code:`s0` 是一样的)。每一个 level 都是灵敏度-分类 (sensitivity-category) 的组合， category 是可选的。当存在有 category 的时候，level 的格式为 :code:`sensitivity:category-set`，如果 category 不存在，那么仅写作 :code:`sensitivity`。 

  如果 category 是一系列连续的，那么可以简写，比如 :code:`c0.c3` 和 :code:`c0,c1,c2,c3` 是相同的。人性化的等级映射关系在文件 :code:`/etc/selinux/targeted/setrans.conf` 下配置。在 RHEL 系列中，默认的 targeted 策略是强制执行 MCS 的，仅有一个灵敏度 s0，有 1024 个不同的 categories，从 c0 到 c1023。 s0-s0:c0.c1023 是针对所有 categories 的 sensitivity 0 级别。

  本文不会涉及 MLS/MCS 这一块的详细说明。

举个例子来解释 TE 为主的基本用法/原理
==================================================

之前 `有一篇文章`_ 写的是在启用 SELinux 情况下部署 NextCloud 的，这里详细说明配置 SELinux 部分，并介绍一些基本原理。

* 环境： CentOS 7， 源码编译安装的 Nginx 以及 PHP-FPM， 导入官方仓库后使用 :code:`yum` 命令安装的 MariaDB 10.1
* 目的： 配置好 SELinux 上下文属性，使得网站得以正常运行
* 总览：

  * MariaDB 是使用 :code:`yum` 直接从导入的 MariaDB 官方仓库下安装的，所有的文件的安装路径包含在预配置好的 SELinux 上下文内，而我对其数据库文件存储路径进行了自定义，所以只需要对新的数据库文件存储路径进行配置即可。
  * Nginx 和 PHP-FPM 是从源码编译安装的，且路径设置都不为默认，所以相应的全部文件的 SELinux 上下文都需要进行配置。
  * 此处不考虑任何 DAC 方面的问题，假定 DAC 均为允许。

* 步骤：

  * **配置 MariaDB 数据库存储路径的 SELinux 上下文信息**

    我自定义的 MariaDB 数据库存储路径为 :code:`/o/db/data/mariadb` ，可以显而易见的是 mariadb 进程需要对这个路径有可读可写的权限，那先来看一下 mariadb 守护进程执行工具的 SELinux 上下文信息：

    .. code-block:: shell-session

      # ls -Z /usr/sbin/mysqld 
      -rwxr-xr-x. root root system_u:object_r:mysqld_exec_t:s0 /usr/sbin/mysqld

    把关注点放在 :code:`mysqld_exec_t` 这个 SELinux object type 上，是否有对一个文件进行读写执行等各种各样的权限是要以进程所在的域类型（也就是 subject type）来进行判断的，拥有正确的 SELinux 上下文的可执行文件，在执行时会因为当前所在域不同而使执行进程进入到不同的域下，这便是域过渡。可以通过命令来查看到过渡规则：

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

    可以看到只有上述 :code:`cluster_t`, :code:`init_t` 等 11 个域才有与 :code:`mysqld_exec_t` 相关的域过渡规则，且只能过渡到 :code:`mysqld_t` 下。然后再来看当前 bash 进程的域类型和当前用户的 SELinux 上下文：

    .. code-block:: shell-session

      # ps auxfZ | grep bash
      unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023 uuu 6243 0.0  0.5 115392 3100 pts/0 Ss 19:04   0:00          \_ -bash
      unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023 root 6267 0.0  0.5 115484 3276 pts/0 S 19:04   0:00                  \_ -bash
      # id -Z
      unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023

    当前 bash 进程所在域由其对应的用户所确定，在没有配置的情况下，所在域类型便是 :code:`unconfined_t` 了，很明显 :code:`mysqld_exec_t` 没有针对 :code:`unconfined_t` 域的过渡规则，那么直接执行就会导致其进程所在域仍然处于 :code:`unconfined_t` 域下：

    .. code-block:: shell-session

      # sed -i '/\[mysqld\]/auser=root' /etc/my.cnf.d/server.cnf
      # /usr/sbin/mysqld > /dev/null 2>&1 &
      [1] 10210
      # ps -eZ | grep mysqld
      unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023 10210 pts/0 00:00:00 mysqld
      # sed -i '/user=root/d' /etc/my.cnf.d/server.cnf
    
    虽然不会影响到正常运行，但默认情况下在这个域下进程基本相当于和没有 SELinux 一样了，很不安全。

    不过通常情况下都是使用 systemdctl 来调用 systemd daemon 来执行的，查看 systemd 进程的 SELinux 上下文信息，可以看到：

    .. code-block:: shell-session

      # ps -eZ | grep systemd
      system_u:system_r:init_t:s0         1 ?        00:01:51 systemd

    其域类型便是 :code:`init_t` ，所以由它执行的 mysqld 可以过渡到 :code:`mysqld_t` 域下：

    .. code-block:: shell-session

      # systemctl start mariadb
      # ps -eZ | grep mysqld
      system_u:system_r:mysqld_t:s0    7385 ?        00:00:00 mysqld
    
    明确了 mariadb 运行进程所在的域，接下来就是明确需要给自定义数据库路径设置的 SELinux 上下文的 object type 了。同样可以先通过命令来查看哪个 type 符合要求：

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
    
    可以看到有很多的 object type 都满足我的 read, write 权限的要求，其中有一个 type 的名称为 :code:`mysqld_db_t` ，很能说明问题，从其拥有的权限来看，很明显 read, write 两个权限是不够用的（关于权限所对应的各种操作以后再说），那么就用它了。接下来就是对新路径配置 SELinux 上下文信息了：

    .. code-block:: shell-session

      # semanage fcontext -a -t mysqld_db_t '/o/db/data/mariadb(/.*)?'
      # restorecon -Rv /o/db/data/mariadb
    
    第一条命令是对 :code:`/o/db/data/mariadb` 文件夹及其所有子内容持久化设置相应的 SELinux 上下文的 object type，因为这条命令不会使之及时生效，所以需要第二条命令配合，使得其及时生效。

    这样子对于 MariaDB 下自定义的数据库存储路径的设置就好了。

  * **配置 Nginx 的 SELinux 上下文信息**

    在这里虽然没有现有的执行文件可以用来做参考，但是默认的规则却是在的。所以搜索文件 :code:`/etc/selinux/targeted/contexts/files/file_contexts` 下的 :code:`/usr/sbin/nginx` 字段，就可以知道默认情况下对 nginx 分配的执行域是什么了。参考上述 MariaDB 过程，可以查到其执行域类型为 :code:`httpd_t` ，同样参考上述 MariaDB 过程可以对 Nginx 进程需要的指定系统文件配置 object type 为 :code:`httpd_sys_content_t` ，而对需要读写的系统文件配置 object type 为 :code:`httpd_sys_rw_content_t` ，需要可以让 :code:`httpd_t` 域直接执行的文件配置 object type 为 :code:`httpd_sys_script_exec_t` 。如何配置的话，同样是使用 :code:`semanage` 命令。

    可能在这里会需要复制几个原先配置好的配置文件到当前 Nginx 的配置目录，那么就需要注意在文件复制/移动过程中的 SELinux 上下文变化，比如：

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
    
    可以看到，在复制文件的时候，如果目标文件不存在，则会保留源文件的 SELinux 上下文信息，而如果目标文件存在，则会保留原目标文件的 SELinux 上下文信息，不过也可以通过使用参数 :code:`--preserve=context` 保留源文件的 SELinux 上下文信息。

    在移动文件的时候，则是保留源文件的 SELinux 上下文信息而不管目标文件是否存在。

    命令 :code:`matchpathcon` 可以方便地检查文件（夹）的 SELinux 上下文与系统配置是否一致，比如：

    .. code-block:: shell-session

      # matchpathcon -V /o/conf/nginx/conf.d/* | grep -v 'verified\.$'
      /o/conf/nginx/conf.d/i.conf has context unconfined_u:object_r:admin_home_t:s0, should be system_u:object_r:httpd_sys_content_t:s0

  * **配置 PHP-FPM 的 SELinux 上下文信息**

    PHP-FPM 所默认的执行域同样是 :code:`httpd_t` ，上述类似的不再说明。不过在这里有一个需求是，在 web 应用运行的过程中，需要和数据库进行通讯，如果数据库有监听着的 unix socket 文件的话，那么直接设置好改文件的 SELinux 权限就可以让 PHP-FPM 来通讯了，可如果是监听的 tcp socket 的话，那么就依赖 SELinux 的另一个属性，布尔值。布尔值的设定允许在运行时修改部分 SELinux 策略，而不需要任何 SELinux 策略的书写知识（那我的理解就是这些个属性所控制的权限在没有布尔值的情况下只能通过修改 SELinux 策略来修改而不是简单配置几下就行的了）。查看布尔值可以使用如下命令：

    .. code-block:: shell-session

      # getsebool -a | grep <pattern or str>
    
    还有一个命令可以很方便的查看对应布尔值的说明：

    .. code-block:: shell-session

      # sepolicy booleans -a | grep httpd_can
      httpd_can_check_spam=_("Allow http daemon to check spam")
      httpd_can_connect_ftp=_("Allow httpd to act as a FTP client connecting to the ftp port and ephemeral ports")
      httpd_can_connect_ldap=_("Allow httpd to connect to the ldap port")
      ...
      # sepolicy booleans -b httpd_can_network_connect
      httpd_can_network_connect=_("Allow HTTPD scripts and modules to connect to the network using TCP.")

    这样子就一目了然了，以下命令用于设置布尔值：

    .. code-block:: shell-session

      # setsebool -P httpd_can_network_connect on
    
    :code:`-P` 选项是对其进行持久化存储到硬盘上的，不然重启后设置就失效了。这几个命令的选项都很少， man 一下就可以看得很清楚。

  * **查错**

    一次性可能不会完全配置正确且无遗漏，那么查看 SELinux 的审计日志就非常重要了。

    CentOS 7 下默认是有运行 auditd 的，所以一般而言可以使用如下命令来查看有的报错：

    .. code-block:: bash

      ausearch -i -m AVC,USER_AVC,SELINUX_ERR -ts today

    其日志文件的位置默认为 :code:`/var/log/audit/audit.log` ，而关于其各字段的含义，可以看这篇文章 `UNDERSTANDING AUDIT LOG FILES`_ 。

    还有一个命令是 :code:`audit2why` 可以方便的把拒绝日志信息转化为更易读的格式。

* 总结： 通过上述的各种工具进行组合重复，就可以完成实现目的的所有设置。所以单就配置本身而言， SELinux 还是比较简单的，但是如果各种服务一多，功能一复杂，所需要考虑的属性，文件扩展属性，各种域之间的联系就会使配置 SELinux 变得复杂。那么在不考虑编写 SELinux 策略而仅仅是实用现有策略的情况下，掌握 SELinux 更多的就是靠经验积累了。

而更多的配置/说明/例子，比如限制与非限制用户， :code:`file_t` 和 :code:`default_t` ，文件系统挂载配置，文件名过渡，禁用 ptrace()， sVirt 等等很多内容，可以看本文最开始提到的那篇文章，或者其它更深入描述的文章。

以上。

.. [1] Linux 下的自主访问控制就是平常最基本的对文件（夹）进行设置用户名/组以及相应的 :code:`wrxst` 权限，然后以用户身份来执行，这样子的一种访问控制管理简单但安全系数不高，一旦获取某一个用户的权限就可以做该用户能做的任何事情，还可以较为简单地进行提权攻击等。

.. _`SELinux User's and Administrator's Guide`: https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/SELinux_Users_and_Administrators_Guide/index.html
.. _`本人整理的工具列表`: https://gist.github.com/Bekcpear/590580d46bf739d3a58675212a2e7316
.. _`Google Books 上`: https://books.google.com/books?id=E8_cDgAAQBAJ&pg=PA70&dq=%22semanage+login+-l%22+Service&hl=en&sa=X&ved=0ahUKEwjN4LWN883UAhUP5WMKHZFrCK0Q6AEINTAC#v=onepage&q=%22semanage%20login%20-l%22%20Service&f=false
.. _`有一篇文章`: /build_nextcloud_service_on_centos_with_selinux.html#selinux-nextcloud
.. _`UNDERSTANDING AUDIT LOG FILES`: https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Security_Guide/sec-Understanding_Audit_Log_Files.html
.. _`SELinux User's and Administrator's Guide 第二章节 SELINUX CONTEXTS 的部分内容`: https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/SELinux_Users_and_Administrators_Guide/chap-Security-Enhanced_Linux-SELinux_Contexts.html
.. _`Creative Commons Attribution-ShareAlike 3.0 Unported License`: http://creativecommons.org/licenses/by-sa/3.0/
