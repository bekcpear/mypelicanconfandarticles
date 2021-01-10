====================================================================================
如何正确地为 Gentoo 的 Portage 包管理器设置代理
====================================================================================

:slug: set_proxy_for_gentoo_portage
:date: 2021-01-10 23:01
:lang: zh_hans
:color: #463c65
:tags: proxy, gentoo, portage
:mykeywords: proxy,socks,git,emerge,gentoo,portage
:description: 如何为 Portage 配置 ftp_proxy, http_proxy, https_proxy, 以及关于 socks5 协议的适用性。
:noindent: true
:status: draft
:summary:

.. contents::

开门见山，本文介绍在 Gentoo Linux 下如何正确地对其包管理器 Portage 设置代理，即日常使用的 emerge 命令。这里介绍软件下载安装时需要的配置；对于同步 Portage 树，则是部分适用。

.. PELICAN_END_SUMMARY

Gentoo 的默认设置
========================================

默认代理： 无
默认下载工具：

* 带版本号的包： :code:`wget`
* 不带版本号的包： :code:`git`

持久性地修改代理
========================================

一、 适用下载带版本号的包
------------------------------------------------

:code:`man make.conf` 可以看到里面有说明如何配置代理，但是过于简要，这边详细说明。

在下载带版本号的包的情况下，只需在 :file:`/etc/portage/make.conf` 文件下配置如下三个变量，就完全足够了：

.. code-block:: bash

  http_proxy="[protocol://][user[:password]@]proxyhost[:port]"
  https_proxy="[protocol://][user[:password]@]proxyhost[:port]"
  ftp_proxy="[protocol://][user[:password]@]proxyhost[:port]"

这些变量会在 emerge 命令运行时，传递给预配置的 :code:`FETCHCOMMAND` 即 :code:`wget` 命令。但，该命令有一个问题是不支持 socks 协议；所以，对于不同的协议需要有不同的代理服务，这样子很麻烦。

修改支持 socks 协议有一个很简单的方法，即修改默认的获取命令为 :code:`curl` ，同样在 :file:`/etc/portage/make.conf` 文件下配置变量，如下：

.. code-block:: bash

  FETCHCOMMAND="curl --retry 3 --connect-timeout 60 --ftp-pasv -o \"\${DISTDIR}/\${FILE}\" \"\${URI}\""
  RESUMECOMMAND="curl -C - --retry 3 --connect-timeout 60 --ftp-pasv -o \"\${DISTDIR}/\${FILE}\" \"\${URI}\""

保存后即完成修改，此时，就可以给不同协议配置同样的 socks 类协议的代理服务，均可生效。比如：

.. code-block:: bash

  https_proxy="socks5h://127.0.0.1:1080"
  ...

二、 适用下载不带版本号的包
------------------------------------------------

对于不带版本号的包，即 :code:`-9999*` 这些包，它们直接使用 :code:`git` 命令从 git 仓库抓取。

而 :code:`git` 命令支持 socks 协议，并且除了能吃上述配置的环境变量外，

.. note::
  配置 :code:`https_proxy` 时也配好 :code:`http_proxy` ，否则可能出现 SSL_ERROR_SYSCALL 错误。

还能独立于其它包单独配置 git 自身的代理，方法有两种：

1. git 能配置针对整个 Linux 系统的参数

   .. code-block:: bash

     git config --system http.proxy '[protocol://][user[:password]@]proxyhost[:port]'

   此配置会写入到 :file:`/etc/gitconfig` 文件内，并生效于系统级别，会被用户/项目级别的配置覆盖。

2. 通过 Portage 的全局 `bashrc`_ 文件 :file:`/etc/portage/bashrc` 来配置临时的 git 代理

   这种方式会对系统配置造成最少的干扰，只略微繁琐一点，需要将下述脚本写入上述的 bashrc 文件内：

   .. code-block:: bash

     if [[ ${EBUILD_PHASE} == "unpack" && ${PV} =~ ^9999 ]]; then
       git config --global http.proxy '[protocol://][user[:password]@]proxyhost[:port]'
     fi

   这个 bashrc 只被 Portage 引用，会在进入每一个安装阶段时被导入。目前，Portage 下抓取 git 项目是通过 git-r3.eclass 实现，该 eclass 定义了 git 项目是在 src_unpack 阶段被更新，所以这里只需要在此阶段时设置即可。且，因为该目录不是被抓取包的 git 目录，所以只能设置用户级别的配置以生效，配置文件会被存放于 Portage 安装过程中沙盒的家目录下，即对应 *安装软件临时目录* [1]_ 下的 :file:`homedir/` 目录。

临时添加代理
========================================

对于需要临时添加代理以使用的情况，目前我知道两种方式：

1. 使用 :gepkg:`net-misc/proxychains` 软件，适用所有下载方式。

   配置好代理列表后，通过如下命令使用：

   .. code-block:: bash

     proxychains -q <cmd> [<args>...]

   其默认配置文件位于 :file:`/etc/proxychains.conf`

2. 临时指定环境变量 {ftp,http,https}_proxy 的方式，适用性同持久性配置。

   即如下：

   .. code-block:: bash

     export http_proxy="..." https_...
     <cmd> [<args>...]

   或

   .. code-block:: bash

     http_proxy="..." https_... <cmd> [<args>...]

以上。

.. [1] 这个目录是 Portage 在编译/安装软件过程中临时建立的，会在成功安装软件后被删除，所以不用担心会有文件残留。具体位置是可以自定义的，详情看 make.conf(5) 手册下 PORTAGE_TMPDIR 条目。

.. _`bashrc`: https://wiki.gentoo.org/wiki//etc/portage/bashrc
