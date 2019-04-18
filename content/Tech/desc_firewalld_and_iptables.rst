====================================
简述 Firewalld 和 iptables(8)
====================================

:slug: desc_firewalld_and_iptables
:date: 2017-07-19
:tags: firewalld, iptables, netfilter
:description: 本文介绍了 Firewalld 和 iptables(8) 的异同以及用法，理解其原理。
:status: draft

.. contents::

简述区别
==============================

Firewalld 和 iptables(8)/ip6tables(8) 都是用来进行 Netfilter 管理的工具， Netfilter 是由内核本身提供的用于管理网络相关操作的框架，其主要的目的是用于实现包过滤、网络地址/端口转换(NAT/NAPT)。为了实现这样子的一个目的，Netfilter 提供了一系列 hooks 给其他内核模块调用。

前者是目前主流的管理工具，后者则是元老（这里需要区别于 Netfilter 的 iptables, ip 表），而相关 Firewalld 的概念可以访问 `Firewalld Concepts`_ 。

无论是理解 Firewalld 还是 iptables(8)，都需要先对 Netfilter 有一定的了解。

Netfilter
==============================

Netfilter 的实现基本贯穿了整个 OSI 模型，它在 Linux 的网络栈内插入了 5 个 hooks 用于实现其目的，分别是：

* **NF_IP_PRE_ROUTING** [1]，对应常用的 PREROUTING 链，所有从外界来的已经通过了合理检查的包都会经过的第一个 hook
* **NF_IP_LOCAL_IN** [2]，对应常用的 INPUT 链，所有(也仅有)进入本地的包所经历的最后一个 hook
* **NF_IP_FORWARD** [3]，对应常用的 FORWARD 链，所有不进入本地的包都会经过
* **NF_IP_POST_ROUTING** [4]，对应常用的 POSTROUTING 链，所有发往外界的包所经历的最后一个 hook
* **NF_IP_LOCAL_OUT** [5]，对应常用的 OUTPUT 链，所有（也仅有）本地创建的发往外界的包进入的第一个 hook

一个流程图如下(figure from netfilter.org)::

  --->[1]--->[ROUTE]--->[3]---->[4]--->
                |            ^
                |            |
                |         [ROUTE]
                v            |
               [2]          [5]
                |            ^
                |            |
                v            |

简单的一个流向说明：

* 包先到达 [1] 号 hook，进行处理（比如：D-NAT/D-NAPT、CONNTRACK、FILTER），需要注意的是，nat 表的 PREROUTING 链仅仅被一个通讯流中的首个包所遍历，意味着其它有被赋予状态的（查阅 CONNTRACK 相关）包不会被该链表所检查，也就意味着对于一个新的链接，首个包所确定下来的 nat 规则应用于这整个链接的所有包。
* 包被交给处理路由的代码，该代码决定包是传给其他的 interface 的还是本地，如果判断无法路由，则丢弃这个包。

  * 如果是本地，那么包来到 [2] 号 hook 进行处理。
  * 如果是其他的 interface，那么包来到 [3] 号 hook 进行处理。

* 包最后会通过 [4] 号 hook 被发往外界。
* 值的注意的是 [5] 号 hook，只有从本地生成的包才会经过它，从上图来看，路由代码会在 hook 触发后再调用，实际上是会先调用来断定源 IP 和一些 IP 选项，这便涉及到了代码的具体实现，不再深究。

内核模块可以在这些 hooks 中任意一个上注册函数，当核心网络代码调用一个 hook 时（一般在包到达对应 hook 时），相应的已经注册好的函数会根据注册时对应的优先级来依次调用，调用后它们会告诉 Netfilter 做这 5 件事情之一：

* NF_ACCEPT 放行该包，包会继续遍历
* NF_DROP 简单的丢弃，包不再继续编历
* NF_STOLEN 接管本包，包不再继续编历
* NF_QUEUE 把包放到一个队列中供用户空间程序执行，一般来说是异步执行的，但是如果没有对应的用户空间工具则会被丢弃，包不再继续编历
* NF_REPEAT 再次请求该包

关于 iptables 下的五张表的优先级是 raw > mangle > nat > filter > security

简单整理下：

* Netfilter 是
* 用来截取数据包的叫 hook，它是 Netfilter 框架提供的插入到网络栈的勾子
* IP tables 是建立在 Netfilter 框架下的包选择系统，内核模块可以利用它注册新表，并让数据包遍历这个表，比如 filter、nat、mangle
* iptables 是一个在内存中的集合规则的数组，它为每一个 hook 提供数据包遍历时是所需要的信息，而 iptables(8) 则是读写这个数组的一个用户空间工具。注意的是，iptables 与 hook 不直接相关，操作数据包的相关模块必须分别注册 hook 和 iptables 才行（这个是开发者的事情了）。

关于常用 targets 的适用范围说明:

* **ACCEPT** 适用于所有
* **DROP** 适用于所有
* **LOG** 适用于所有
* **DNAT** 仅适用于 nat 表下的 PREROUTING/OUTPUT 链
* **SNAT** 仅适用于 nat 表下的 INPUT/POSTROUTING 链
* **MASQUERADE** 仅适用于 nat 表下的 POSTROUTING 链
* **REDIRECT** 仅适用于 nat 表下的 PREROUTING/OUTPUT 链
* **REJECT** 仅适用于 filter 表下的 INPUT/OUTPUT/FORWARD 链

*详细的查看 iptables-extensions(8)*

iptables(8)
==============================

iptables(8) 是一个管理员工具，用于维护 netfilter 对应的 IPv4 表， IPv6 表则由对应的 ip6tables(8) 管理。两者命令格式基本一致。


Firewalld
==============================




.. _`Firewalld Concepts`: http://www.firewalld.org/documentation/concepts.html