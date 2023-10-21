==================================================
一套适用个人/团队的 IRC 解决方案
==================================================

:slug: an-irc-usage-solution-for-individuals-and-teams
:date: 2023-02-05 20:10
:lang: zh_hans
:color: #1A1A1A
:tags: irc, guide, solution
:mykeywords: irc,solution,guide,znc,weechat,tutorial,指南,教程,personal,个人
:description: 一份适用于个人的，能长期舒适使用的 IRC 指南。
:noindent: true
:summary:

.. contents::

IRC 作为一款 20 世纪 80 年代发布的聊天系统竟能沿用至今，确有其独到之处。
本文会从个人使用者的角度，讲述一套就目前来看，方便且实用的 IRC 聊天解决方案，
包括 IRC 网络、 IRC Bouncer 、客户端 的选择和使用，以及消息推送的集成。
同时，会引出额外的线索，以便读者进行部署。

.. PELICAN_END_SUMMARY

* 本文适用有基本的 IRC 客户端使用经验者
* 本文不涉及繁杂的 IRC 命令，因不同客户端，不同服务器实现，命令也不同
* 仅讲述基本、常用的操作，以一条较单一、实用的路线作为引导，概述整个 IRC 系统
* 根据上述两条规则，帮助理解并配置好一套实用、简洁的方案以使用 IRC
* 本文非手把手类型，对于服务的搭建，仅列出大致框架，并引出更详细的官方指导页
* 本文忽略 irccloud 这种方便现成但收费也不好自定义的服务
* 本文较为粗糙，会找时间进一步完善
* 本文唯一原始链接： https://bitbili.net/an-irc-usage-solution-for-individuals-and-teams.html
* 如有疑问或发现错漏，欢迎留言

前置要求
=========================================

知识及技能
++++++++++++++++++++++++++++

1. 熟练的 Linux 命令行操作能力（或 MacOS/Windows 同阶）
2. 举一反三和独立思考的能力
3. 基础的网络相关概念，包括但不限于：

   * DNS
   * NAT
   * TCP/IP 模型
   * TLS
   * TLS 证书

4. （可能）基本网络相关工具的使用（用于调试），包括但不限于：

   * curl
   * dig
   * ip
   * openssl
   * ping

额外的设备及要求
++++++++++++++++++++++++++++

1. 一台连接互联网的可 7x24 小时工作的服务器（虚拟机或物理机），本文内标记为 :code:`Server R`
2. （可选）条件 1 的服务器带公网 IP
   *此条件的目的是为了支持从外网直接连接，如果不满足，则只支持内网访问*

.. important::

  7x24 小时运行的要求是为了保证使用此套方案的舒适性，无论是家庭服务器还是 VPS 类，均可。
  断断续续的运行（频繁开关服务）会导致失去本应有的体验，也就失去了部署此套方案的意义。

  下文介绍的 ZNC 服务器支持多用户，也就是支持多人共用一台服务器，一人劳动多人受益，相当适合团队使用。

概览
=========================================

IRC 系统
++++++++++++++++++++++++++++

.. ditaa::
  :alt: IRC System Overview

                                                                                                                         * IRC System Overview (bitbili.net)
                                                                                                                            from the client's point
  /----------------------\
  |     Client Relay c666|                                                                   /-------------------------------------\
  +----------------------+                                                                   : {d}                                 |
  |                      |<-=----------------------------> Server / Bouncer ..               |  IRC Network A                      |       /------------------\
  |     IRC Client A     |                                                                   |                                     |       : {d}              |
  |                      |<----------------------------------------------------------------->|   +----------------+                |       |  IRC Network B   |
  \----------------------/                                                                   |   |                |<-=-> Client X  |       |                  |
                                                                                             |   |  IRC Server A  |<-=-> Bouncer Y | ..<=->|     ...          |
  /----------------------\                      +-----------------+                          |   |                |<-=-> ..        |       |                  |
  |                      |<-------------------->| {io}            |<------------------------>|   +----------------+                | ..<=->|     ^ |          |  ...
  |     IRC Client B     |                      |  IRC Bouncer A  |                          |          ^ |                        |       |     | v          |
  |                      |<-=--> ..             |                 |<-=--> Server ..          |          | v                        |       |                  |  ...
  \----------------------/                      +-----------------+                          |   +----------------+                |       |     ... <- ...   |
                                                                                             |   |  IRC Server B  |<-=-> Client Z  |       |         ->       |
             ...                                +-----------------+                          |   +----------------+<-=-> ..        |       |     ^ |          |
                                                | {io}            |                          |          ^ |                        |       |     | v          |
                                Client .. <-=-->|  IRC Bouncer B  |<-=--> Server ..          |          | v                        |       |                  |
                                                |                 |                          |          ...                        |       |     ...          |
                                                +-----------------+                          |                                     |       |                  |
                                                                                             \-------------------------------------/       \------------------/
                                                        ...

.. this is a comment to close the highlight in vim editor >|

上图从客户端的角度表示了 IRC 系统的基本构成，并表明了其间的关系。

1. 一个 `IRC 服务器`_ 和两个 `IRC 客户端`_ ，就能组成最基础的聊天系统
2. IRC 服务器之间可以互相通讯，加上各自负责的客户端，组成了一个更大的 `IRC 网络`_
3. 世界上有很多个 IRC 网络
4. 一个客户端/一个 IRC Bouncer 可以同时连接到多个 IRC 网络
5. 我们通常所说的 IRC 聊天是指在同一个 IRC 网络下的聊天，不同网络间无法通讯
6. 传统的 IRC 服务器并不储存客户端发送的消息，如其名（Internet Relay Chat），它只是一个中继 [1]_
7. 每当一个用户的所有客户端从 IRC 网络断开连接后，就无法再收到发送给该用户的消息
8. 客户端连接到 IRC 网络后，实际的 IP 地址会被其它用户所知晓 [2]_
9. 为了解决问题 7 和 8，出现了 `IRC Bouncer`_ ，它位于客户端和 IRC 服务器之间，扮演着代理和中继的角色

解决方案
++++++++++++++++++++++++++++

.. ditaa::
  :alt: IRC Usage Solution

                                                                                                             * IRC Usage Solution (bitbili.net)

                                                          +----------------------------+
                                                          :                            |
                                                          |  Server R"                 |
                                                          |                            |
                       +------------------+               |       /----------------+   |
                       |{io}   APNs  cFAA |               |       |  Notification  |   |
                  /----| or other similar |<----------------------|cFAA Server     |   |
                  |    +------------------+               |       +----------------/   |
                  |                                       :                ^           |
                  |                                       +----------------|-----------+
                  |                                                        |
  /---------------|-----------------\                       +--------------|---------+                       /-----------------------\
  :               |                 :                       :              |         :                       : {d}                   |
  |  Mobile       |                 |                       |  Server R    |         |                       |   Libera.chat         |
  |               v                 |                       |              |         |     /---------------->|                       |
  | +-----------------------------\ |                       |      /--------------\  |     |                 |          ...          |
  | |cFAA Notification Center     | |                       |      |cFAA PUSH     |  |     |                 |                       |
  | \-----------------------------+ |                       |    +-+-------------+/  |     |                 \-----------------------/
  |                                 |                       |    | {io}          |<--------/
  |      /---------------------\    |                       |    |      ZNC      |<-------------\
  |      |  Client Solution A  |    |                       |    |               |<--------\    |
  |      |  Palaver or Others  |<---------------------\     |    +---------------+   | ... |    |                /-----------------------\
  |      \---------------------/    |                 |     |           | |          |     |    |                : {d}                   |
  |               or                :                 |     |  +------------------+  :     |    |                |   OFTC.net            |
  |      /---------------------\    |                 \------->|       Nginx      |  |     |    \--------------->|                       |
  |      |  Client Solution B  |    |                       :  +------------------+  |     |                     |          ...          |
  |      |    Glowing Bear c666|<---------------------\     |          ^   ^         |     |                     |                       |
  |      \---------------------/    |                 |     +----------|-=-|---------+     |                     \-----------------------/
  \---------------------------------/                 |                |   |               |
                                       +--------------|-----------+    |   |               |
                                       |  +-----------+---------+ |    |   |               \-------------------------------->  ...
  /---------------------------------\  |  | tmux           cAFB | |    |   |
  :                                 |  :  |           |         | :    |   |
  |  Desktop                        |  |  |           v         | |    |   |
  :                                 |  |  | /---------------\   | |    |   |
  |      /---------------------\    |  |  | |c666 Relay     |   | |    |   |
  |      |  Client Solution A  |    |  |  | +---------------+   | |    |   |
  |      |cAFB    SSH          |<-------->| |               |   | |    |   |
  |      \---------------------/    :  |  | |    Weechat    |<- +------/   |
  |               or                |  :  | |               |   | |        |
  |      /---------------------\    |  |  | \---------------/   | |        |
  |      |  Client Solution B  |    |  |  +---------------------+ |        |
  |      |  Weechat or Others  |    |  |                          |        |
  |      \---------------------/    |  |   Server R'              |        |
  |                ^                |  |                          |        |
  \----------------|----------------/  +--------------------------+        |
                   \-------------------------------------------------------/

方案以 IRC Bouncer 实现之一的 ZNC 为核心，充当客户端到 IRC 服务器之间的桥梁，同时利用其插件实现了消息推送的功能。
具体见下文各章。

IRC 网络
=========================================

IRC 网络是由多个 IRC 服务器互相连接所构成的，每个 IRC 服务器可能有零、一或多个连接着的 IRC 客户端或 IRC Bouncer。
（单个服务器也能作为一个 IRC 网络）

选择一个适合的 IRC 网络作为平台是使用 IRC 的一个前提，其它细节在这里不用在意。

目前最大的 IRC 网络名为 `Libera.Chat`_ [3]_ ，下文以它为目标进行讲述。

IRC 服务器
++++++++++++++++++++++++++++

接入 IRC 网络的方法是连接上该网络内的一台 IRC 服务器。
虽然一个大型的 IRC 网络存在多台服务器，但使用上只需连接该网络主地址
（如 irc.libera.chat ），通常都会以轮询的方式就近分配一台特定的服务器地址给客户端 [4]_ 。

现如今，使用 TLS 的连接已经是基本要求，所以就默认端口号而言，使用 6697 这个启用 TLS 的端口。
不同的网络可能设置有不同的端口号，需确认。

**IRC 网络和服务器都是现成的，仅需选择所需地址和端口即可** （连接到 IRC 服务器的连接都使用 TCP 协议）。
而从下文开始，服务和客户端均需自行配置。

IRC Bouncer
=========================================

IRC Bouncer 作为代理和中继的角色，是实现本文所述方案的核心。
它能作为客户端与 IRC 服务器进行通讯，也能作为服务器与 IRC 客户端进行通讯。
它可以隐藏 IRC 客户端的真实地址，更主要的，在现有的 IRC 网络环境下，它基本上 [1]_
是确保消息不遗漏，实现消息推送的唯一手段（虽然某些客户端长时间运行加插件的形式也可以）。

这里选择 ZNC 这个实现，它虽然不是实现功能和标准最多的，但就目前来看是非常稳定，功能也足够的。

.. tip::

  世界上有一些 `免费的 ZNC 服务提供者`_ ，这里不涉及，如果使用，须知所有消息记录无法控制（不包括 DCC 和使用额外加密插件的情况）。

*此章所有操作均在 Server R 上完成*

ZNC 安装
++++++++++++++++++++++++++++

参考官方文档： https://wiki.znc.in/Installation

安装很方便，使用各 Linux 发行版自带包管理器安装完毕即可。

ZNC 配置
++++++++++++++++++++++++++++

参考官方文档： https://wiki.znc.in/Configuration

运行 :code:`znc --makeconf` 生成一个初始化的配置文件，虽然该命令所生成的配置并不足够日常使用，但是一个很好的开始。

.. attention::

   该命令需要使用 znc 服务的执行用户执行，通常为 `znc` 用户，即 :code:`sudo -u znc znc --makeconf` 。
   执行完成后，注意配置文件保存路径，默认在执行用户的 :file:`~/.znc` 文件夹下。

这里提供一个额外的更合理的不方便通过 Web UI 变更的配置示例（适用于初始设置）：

.. code-block:: c

  LoadModule = webadmin
  // webadmin 加载 webadmin 模块后，就可以通过 Web UI 对 ZNC 进行配置

  LoadModule = adminlog
  // 启用后会记录基本的用户连接信息，建议启用

  LoadModule = log
  // log 模块用于记录所有的聊天记录，并按频道/用户进行保存
  // 它可以在三个级别上加载（global/network/user），此处为 global 级别
  // 同一级别的不同网络/用户间互相隔离，需注意
  // 重复加载会导致重复的日志记录，所以通常情况下在一个级别上加载
  // 私有部署的服务器，直接全局加载即可

  LoadModule = lastseen
  // 用于显示用户最后登录的时间，可开可不开

  // 另有其它多个模块可用，不同模块适用的范围不同，可查 Web UI 根据需要配置

  //SSLCertFile = /path/to/cert/dir/fullchain.cer
  //SSLDHParamFile = /path/to/dhparam.pem
  //SSLKeyFile = /path/to/cert/dir/primary.key
  // 顾名思义， SSL/TLS 证书相关， SSL = true 时必要
  // 我这里本身服务器就有 Nginx 占用 443 端口，就顺带全过 Nginx 反代了，
  // 当然在无 Nginx 反代的情况下，也是可以正常使用 SSL 的。
  // （需要注意的是，虽然 ZNC 设置内无法配置 TLSv1.3 的启用与关闭
  //   但实际支持，参考： https://github.com/znc/znc/issues/1512
  //   注意加密套件优先级配置）

  // 针对监听端口的配置如下，这里我配置了两个监听端口。
  // listener0 只用于 web 访问，方便通过 Web UI 对 ZNC 进行配置；
  // listener1 只用于 IRC 连接。
  // 一些顾名思义的配置不赘述
  // Host 为本地的监听地址，因为需要套额外的 Nginx，所以这里配置为 lo 地址，
  // 如果有其它情景，请根据需要修改。
  <Listener listener0>
    AllowIRC = false
    AllowWeb = true
    Host = 127.0.0.1
    IPv4 = true
    IPv6 = false
    Port = 15010
    SSL = false
    URIPrefix = /
  </Listener>

  <Listener listener1>
    AllowIRC = true
    AllowWeb = false
    Host = 127.0.0.1
    IPv4 = true
    IPv6 = false
    Port = 15011
    SSL = false
    URIPrefix = /
  </Listener>

  // …
  // 这里省略了用户配置内容，用户配置使用命令生成的即可，但需要注意：
  //   1. 不建议使用管理员账户作为平常 irc 客户端的登录用户
  //   2. 因为 1， 所以至少再创建一个额外的非管理员账户
  //   3. 额外用户的创建和所有用户的额外配置，可通过 web ui 进行

TLS 证书
---------------------

无论是 ZNC 的 Web 服务还是 IRC 服务，通常都需要一个受 CA 认证的证书，才能支持 TLS 连接，
但这并非本文重点，如何申请免费受信的 TLS 证书，可参阅： https://github.com/acmesh-official/acme.sh 。
注意配置好自动续期，同时别忘了自动续期后， reload ZNC 或者 Nginx 服务，以重新载入新的证书文件。

Nginx 配置
---------------------

Nginx 基础不赘述，这里贴出适用的两个缩减过的 Nginx 配置。

1. 反代 Web 端口：

.. code-block:: nginx

  # ...

  server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name znc.your.domain;

    # ...

    ssl_certificate         /path/to/cert/dir/fullchain.cer;
    ssl_certificate_key     /path/to/cert/dir/primary.key;
    ssl_dhparam             /path/to/dhparam.pem;
    ssl_trusted_certificate /path/to/cert/dir/fullchain.cer;

    ssl_protocols TLSv1.3;
    ssl_prefer_server_ciphers off;

    # ...

    location / {
      # ...
      proxy_pass http://127.0.0.1:15010;
    }


2. 反代 IRC 端口：

.. code-block:: nginx

  stream {
    log_format  main  '$remote_addr:$remote_port [$time_local] '
                      '$status ';

    upstream znc {
      server 127.0.0.1:15011;
    }

    server {
      listen      6697 ssl;
      listen      [::]:6697 ssl;

      # ...
      # 及上述的 SSL 配置

      # 为了避免某些客户端不支持 TLSv1.3，所以这里还是兼容了 TLSv1.2 协议
      ssl_protocols TLSv1.2 TLSv1.3;
      ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
      # 通常来说，上述加密套件都是安全的，是可以由客户端进行选择的，但这里我更希望严格遵循此服务端规定的套件顺序。
      # 此处加密套件的设定，仅对 TLSv1.2 有效
      ssl_prefer_server_ciphers on;

      proxy_pass znc;
    }
  }

:code:`server` 和 :code:`stream` 块的层级不同，需注意。
可使用 https://ssl-config.mozilla.org/ 方便地生成 Nginx 配置。

完成配置
++++++++++++++++++++++++++++

在完成上述自选的配置后，请使用管理员账户访问 ZNC 服务的 Web UI，进行配置微调，创建额外的普通账户等工作。
之后，上述提及的配置文件会被自动更新，再之后，无特殊情况无需再手动更新该配置文件。
（通常使用 Web UI 或者 *controlpanel* 这个模块进行）

此时，可以从 Web UI 界面为普通账户添加一个 IRC 网络（UI 界面内的设置请自行摸索）。

.. tip::

  1. 添加网络时建议使用启用 TLS/SSL 的连接。
  2. 有些 IRC 网络针对特定的 IP 段会要求只接受 SASL 认证的连接（如 Libera.Chat），
     这种情况在 Web UI 上不好查看， `下文`_ 会额外说明。

目标
++++++++++++++++++++++++++++

无论情景是否需要 Nginx 作为反代，至此应完成的目标如下：

1. 能正常打开 Web UI 界面，管理员账户正常登录
2. 拥有一个/多个管理员账户，此账户仅作为登录 Web UI 进行管理所用
3. 拥有一个/多个日常使用账户（无管理员权限），此类账户为 IRC 客户端使用账户，
   一个账户下可以配置多个 IRC 网络，支持同时连接，
   如何连接同一账户下不同网络，参阅 Web UI 界面提示。
4. 本地 :code:`telnet ZNC-IP ZNC-IRC-PORT` 连接正常

所有目标确认完成后，继续下文。

IRC 客户端
=========================================

ZNC 作为 IRC Bouncer 无法方便的查看消息，回复消息。所以还需使用常用的客户端。

由上述 `解决方案`_ 的概览图可知，

**移动端** 的客户端方案有两种：

1. 使用通常意义上的 IRC 客户端，直接连接 ZNC，这也是最简单方便的。
2. 使用 Weechat 的 Relay 客户端，即 Glowing Bear （或其它类似的产品，或 Weechat 级别上类似的产品链）。

.. note::

  就目前体验来讲，我倾向于使用 Glowing Bear，原因在于
  iOS 上我找到的比较好用的 IRC 客户端 Palaver 中文输入支持过于糟糕，尝试过一些其它的也不如意。

**桌面端** 则使用通常意义上的 IRC 客户端即可，但如果配合 Glowing Bear 在服务器端长期开启的 Weechat Relay 的话，
可以通过 SSH 方式打开服务器上 tmux 下的 Weechat 使用。此处的服务器可以是 Server R，也可以是其它（注意连接保密性）。

对于通常意义上的 IRC 客户端，只说明一点，ZNC 服务所提供的普通连接方式是用户名和密码，这个通常填写在 IRC
客户端的服务器用户和密码一栏，如果没有单独的服务器用户名提供，则以 :code:`username:password` 这样的格式，填写在服务器密码栏。

*客户端所需要连接的服务器地址是 Server R 的地址，域名/IP 以及端口号根据具体部署确定。*

.. _`下文`:

.. attention::

  使用客户端连接上 ZNC 后，如果遇到 *提示无法连接到 Libera.Chat （或其它）网络，原因是 IP 受限需要 SASL*
  *认证* 这种情况，需要通过任意办法（切换 IP、代理等）先完成好 SASL 注册，请参考各网络的 SASL
  文档并设置完成，再启用 ZNC 的 `SASL`_ 模块，并配置后才可成功登录。

Weechat + Relay 形式
++++++++++++++++++++++++++++

着重讲述::

  Glowing Bear <---> RELAY == WEECHAT
                             ---------
                               TMUX   <-- SSH --> Terminal

这种形式。

`Glowing Bear`_ 是 Weechat 的中继客户端，它与启用了中继的 Weechat 客户端进行通讯，以实现远程操纵该 Weechat 客户端的目的。

如何配置 Weechat 中继请查阅官方文档： https://weechat.org/files/doc/stable/weechat_user.en.html#relay ，这里说明一些注意事项：

1. Glowing Bear 官方有提供一个现成的客户端地址（ :code:`https://www.glowing-bear.org/` ）
   可以访问此网站加载客户端界面，再由本地连接到你 Weechat Relay 服务
2. HTTPS 连接下的 Weechat 只能访问开启了 SSL/TLS 的 Weechat Relay 服务，TLS 证书同样建议使用由认证 CA 颁发的，具体略。
3. 因此如果需要使用未开启 SSL/TLS 的 Relay 服务需要使用 HTTP 连接下的 Weechat 客户端
4. **重要：虽然官方也提供了 HTTP 连接的地址，域名同上，但个人不推荐在外网使用 HTTP 连接，因为客户端文件很容易被篡改。**
   因此，在需要 HTTP 环境的情况下，建议自行搭建 Glowing Bear 服务，并通过内网访问使用，方法见 Glowing Bear 链接内文档

Weechat
++++++++++++++++++++++++++++

Weechat 是我很喜欢的一个桌面/服务器均可用的字符界面 IRC 客户端。它的核心仅实现了界面、配置、基本的网络服务和 API，
IRC 和其它的一些功能均通过插件的形式实现，是一个可扩展的 IRC 客户端。

具体使用请自行查阅文档，这里贴出一个我针对外观的一套配置： :github:`bekcpear/weechat-config` ，内附整体截图。
同时推荐 :file:`go.py` 插件用于替换 :kbd:`Alt` + :kbd:`j` 这个默认的 buffer 跳转功能，我对官方原版的进行了修改使其更方便使用：
:github:`bekcpear/weechat-scripts@go:python/go.py` ，改动为：

1. 支持 :kbd:`Esc` 按键退出跳转输入窗口
2. 竖向排列候选列表，并限制个数，以增加美观程度

目标
++++++++++++++++++++++++++++

我说明了自己熟悉的，其实客户端没有任何要求，根据自己需求选择。

到这里需要完成：

1. 选定自己需要的 IRC 客户端（方案）
2. 可以使用 IRC 客户端连接上 ZNC 并正常使用
3. 如果有选择了 Weechat 的 Relay 功能作为中转，则需完成可以使用 Glowing Bear 连接成功并使用
4. 可以方便的通过 Desktop 或者移动平台使用 IRC 了
5. 可以经由客户端方便的加入/退出频道

消息推送
=========================================

至此，一个基本的使用环境已经完成，但是少了一个很重要的环节，消息推送。
IRC 作为很传统的聊天系统，移动平台的消息推送是基本没有的，但是这里，可以借助 ZNC 的一个名为 `Push`_ 的模块完成。
具体请查阅该链接。

它里面包含了预置的多个消息推送服务器的 API，但很多已经无法使用，可以使用的也基本收费，所以看子章节：

iOS
++++++++++++++++++++++++++++

针对 iOS 系统，推荐使用一名为 `bark-server`_ 消息推送服务器，在 App Store 可以搜索 :file:`Bark` 安装使用，其自带了一个可用服务器，
消息的具体推送流程在上述 `解决方案`_ 图已注明，如果不担心信息泄漏，可以直接使用预配置的服务器，也支持自行搭建，具体请查阅文档。

针对此服务器，提供 Push 插件的配置如下（确认加载插件后，执行 :code:`/msg *push help` 进入配置）：

.. code-block:: ini

  # 必要配置
  # 1. 推送采用自定义 URL 的方案
  set service url
  # 2. 消息转义
  set message_escape URL
  # 3. 具体 API，其中 Server-Key 在手机 App 于添加的服务器上注册完成后，可以查看到
  set message_uri https://bark.domain/Server-Key/{context}+%E2%80%A2%E2%80%A2%E2%80%A2+%40{nick}/{message}?group=irc

  # 其它配置可选，请根据需要自行决定
  # 但建议如下几项：
  # 1. 不考虑最后一次消息发送的窗口时间
  set last_active 0
  # 2. 缩短消息通知的间隔时间（秒）
  set last_notification 30
  # 3. 同个 buffer 已通知后，不要求仅在回复后继续通知
  set replied no

Android
++++++++++++++++++++++++++++

Android 系统我这里未测试，但可以考虑使用 `PushDeer`_ ，同样支持自行部署。
其它同 iOS 内容。

目标
++++++++++++++++++++++++++++

虽然单独的推送系统，无法满足点击消息能直接打开 IRC 客户端的要求，
但实际使用发现，仅消息推送就已满足日常使用需求。

到这里，需要完成：

1. 每当有提及 IRC 登录账户的消息送达时，移动平台能立刻接收到消息推送
2. 能够根据自己的需求，使用 ZNC 的 :code:`Push` 插件自定义高亮关键字（未提及，请摸索）

总结
=========================================

这一套方案，很轻量，能提供完整的消息记录，在有需要的时候可以进行全文检索，能保证全天候在线，实现了实时的消息推送，并满足快速的回复的要求。针对目前的 IRC 网路环境而言，是一套能长期使用，也易用的成熟方案。

但 IRC 客户端不像其它 IM 足够美观，整套系统不像 irccloud 开箱即用。

不过我很喜欢，在主流的 IRC 网络支持离线消息之前（应该还很久），这套都适合使用 *（况且还有消息推送不知何时能自带）* 。

脚注
=========================================

.. [1] 现已有聊天历史记录的标准草案，有些服务器实现（如 ergo）已实现之，以后或成为标准，参见: https://ircv3.net/specs/extensions/chathistory 。
.. [2] 该项针对传统的但也是目前盛行的 IRC 服务器实现，但通常 IRC 网络都会有额外的 :ruby:`斗篷|Cloak` 功能以向非服务器管理员隐藏 IP 地址，详细看各 IRC 网络的说明。
.. [3] Libera.Chat 是由 freenode.net 的前员工于 2021 年 5 月份创建，起因复杂，详见: https://en.wikipedia.org/wiki/Freenode#Ownership_change_and_conflict 。
.. [4] 一个是 DNS 的轮询机制，即针对不同区域可以设定针对性的多个解析记录，再经由每次查询轮询一个更优先的结果来粗略的实现负载平衡；至于设定 DNS 解析本身的行为，每个网络内部可能存在或者不存在一套额外的轮询系统。

.. _`Libera.Chat`: https://libera.chat
.. _`免费的 ZNC 服务提供者`: https://wiki.znc.in/Providers
.. _`Glowing Bear`: https://github.com/glowing-bear/glowing-bear
.. _`SASL`: https://wiki.znc.in/Sasl
.. _`Push`: https://wiki.znc.in/Push
.. _`bark-server`: https://github.com/Finb/bark-server
.. _`PushDeer`: https://github.com/easychen/pushdeer
