========================================================================
[原文翻译] Postfix Architecture Overview
========================================================================

:slug: Translate_to_Chinese-Postfix_Architecture_Overview
:lang: zh
:date: 2016-07-25 03:23
:tags: postfix, server
:notoriginal: true
:status: draft

.. contents::

本文翻译自 http://www.postfix.org/OVERVIEW.html ，草稿不发布，原始协议未知。


介绍
------------------------------

这个文档展现了Postfix结构的总览，并将每一个Postfix的命令和服务器程序超链接到其他的文档进行描述。文章给出了每个使用的命令和服务器程序的大体信息，并将特殊的使用案例和背景信息超链接到别的文档。（关于这个，我这边仅仅会挑选自认为重点的描述在文档的结尾）

本文包含的主题有：

* Postfix如何接收邮件
* Postfix如何发送邮件
* Posffix后台运行过程
* Postfix支持的命令

Postfix符合接收邮件
------------------------------

当一封邮件到达了Postfix的邮件系统时，首先停留在了incoming队列。下面的图显示了一封新邮件参与的主要进程。名称后面跟有数字的是Postfix命令或者服务器程序，名称为[大写]的是Postfix队列（原文是写的不跟数字且有阴影的为队列，我这边因为作图使用code标签所以就不弄阴影了）。

::

                            trivial-rewrite(8)
                                ^|
                                |v
  Network -+-> smatpd(8) -+-> cleanup(8) ------------> [INCOMING]
          +--- qmqpd(8) -+
                          +----- pickup(8) <-+
                                            |
  Local -> sendmail(1) -> postdrop(1) -> [MAILDROP]

描述
------------------------------

* 网络邮件通过 :code:`smtpd(8)` 或者 :code:`qmqpd(8)` 服务器进入Postfix，这2种服务器会去除SMTP或QMQP的协议封装，为了保护Postfix也会同时执行一些必要的检查，然后就把发送者、接收者和邮件内容传输给 :code:`cleanup(8)` 服务器了。 :code:`smtpd(8)` 服务器通过一些配置就可以用于屏蔽不需要的邮件，请看文档 `SMTPD ACCESS README <http://www.postfix.org/SMTPD_ACCESS_README.html>`_ 。
* 本地寄送邮件由被Postfix兼容的 :code:`sendmail(1)` 命令接收，并被特权命令工具 :code:`postdrop(1)` 放到了MAILDROP队列。即使当Postfix邮件系统不工作的时候，这个操作也是会运行的（估计是纯粹的命令工具操作不依赖服务器）。本地的 :code:`pickup(8)` 命令则用于挑选本地提交的邮件，同样也会做一些有利于服务器的检测，然后将邮件内容发送给 :code:`cleanup(8)` 服务器。
* 邮件系统内部源的邮件会被直接发送到 :code:`cleanip(8)` 服务器，这个 **内部源** 并没有出现在上述的图例里面
