==================================================
Gentoo Linux 安装及使用指南
==================================================

:slug: gentoo-linux-installation-and-usage-tutorial
:date: 2021-10-03 11:35
:modified: 2021-11-06 17:14
:lang: zh_hans
:color: #463c65
:tags: Gentoo, Linux, tutorial, installation, usage
:mykeywords: gentoo,linux,installation,usage,tutorial,guide,handbook,portage,安装,配置,指南,手册
:description: 十分精简、适合新手、可持续进阶的 Gentoo Linux 完整安装及使用指南。
:featured_image: /nocimages/gentoo.png
:noindent: true
:summary:

.. contents::

很早以前，我就有写了一篇安装 Gentoo Linux 的文章（ `Gentoo Linux 安装 —— 带硬盘加密`_ ），只是那篇文章存在局限性。因为一些原因，我打算写一篇更详细更完整，适合新手且可以无缝进阶的 Gentoo Linux 安装及使用指南。

.. _`开头`:

* 本文面向新手，十分精简，配置正确
* 本文以 AMD64(x86_64) 平台为例进行说明
* 本文以安装到实体机为目的（也适用于虚拟机）
* 本文以一条相对单一的路线指导安装使用 Gentoo Linux，亦可前往 `Gentoo Wiki 页`_ 以获取更多更详细内容。
* 本文唯一原始链接： https://bitbili.net/gentoo-linux-installation-and-usage-tutorial.html
* 本文源码在 `这里`_ ，欢迎纠错
* 如有问题可以上 https://t.me/gentoo_zh 提问/反馈

.. tip::

  这里有一个完整参照本文安装的视频——《 5 分钟速看 Gentoo Linux 完整安装进 KDE Plasma 》：

  * `bilibili （需要登录才能查看高清版）`_
  * `我的公开链接下载`_

正文开始：

.. PELICAN_END_SUMMARY

开始之前，建议了解一下 Gentoo Linux 的哲学（英文）： https://www.gentoo.org/get-started/philosophy/

准备工作
==================================================

确保有
  至少一台可以正常使用且能连接互联网的电脑 *（用于*

  * *下载 LiveCD 系统*
  * *写入 LiveCD 到 U 盘*
  * *安装 Gentoo Linux）*

  一个可以工作的 U 盘 *（用于装载 LiveCD 系统）*

1. 打开 `北外镜像地址`_ ，进入目录 :file:`releases/amd64/autobuilds/current-install-amd64-minimal/` 下载最小化安装系统镜像，名字为 :file:`install-amd64-minimal-{日期}.iso`

   .. note::

     镜像地址是可以自由选择的，你可以选择更靠近自己的镜像服务器，Gentoo Linux 官方有收录的 `镜像列表`_ 。

     LiveCD 也同样不一定是 Gentoo Linux 的，可选系统的 LiveCD ，但本文以 Gentoo Linux 的为例。

     可选步骤
       为了保险起见，下载好的文件需要校验其完整性，镜像服务器会提供名为 :file:`install-amd63-minimal-{日期}.iso.DIGESTS` 和 :file:`install-amd64-minimal-{日期}.iso.DIGESTS.asc` 的校验文件。

       如今都是通过 https 协议下载文件，遂通常使用 :file:`.DIGESTS` 后缀的文件完成校验即可，该文件内包含四个 HASH 值，使用对应的工具来生成下载的 :file:`.iso` 文件的 HASH，后进行比较即可。

       Windows 平台可以使用 HashCalc 来生成，其可以生成 sha512sum，但是不支持 b2sum，一般来说两者之一匹配就可以了，如果一定想看看 b2sum 的话，可以在 :file:`https://www.blake2.net/` 下载适用 Windows 的二进制包后在命令行下执行生成。

       Linux 平台一般都默认安装了对应工具，命令为 :code:`sha512sum` 和 :code:`b2sum` 。

       后一个 :file:`.DIGESTS.asc` 校验文件附带上了签名信息，可以使用 Gentoo Linux 发布的公钥来校验这个包含 HASH 值的文件是否完整且未被篡改，超出本文内容，这里不进行说明。

2. 将 :file:`.iso` 文件写入到 U 盘。

   .. tip::

     如果是虚拟机，那么此章步骤 2 和 3 会不同，直接把 livecd 挂载到虚拟机的光驱，选择光驱启动即可，其它步骤一致。

   * Windows 上可以使用工具 `Rufus`_ 进行写入（写入前配置默认无需更改，即 MBR 分区，BIOS 或 UEFI，FAT32 系统）
   * Linux 上则可以使用自带的 :code:`dd` 命令来写入，具体命令为

     .. code-block:: shell

       dd bs=4M if=「.iso 文件的路径」 of=/dev/sdX status=progress oflag=sync
       # 命令中 sdX 为 U 盘这个块设备的路径名，需要根据你的实际情况来修改
       # 注意，U 盘内数据将丢失

3. 将准备好的 U 盘插上需要安装 Gentoo Linux 的电脑后重启/开启该电脑，通过按键（Esc/Del/F2/F10/F12）进入启动选项，选择后进入到 U 盘内的 LiveCD 环境。

   如需配置 UEFI 启动，务必同样以 UEFI 方式启动 U 盘内的系统（选择时会有带 [U]EFI 和不带 [U]EFI 字样的两种 U 盘启动选项）。

   .. note::

     根据主板不同，开机时选择启动项的方式也不同，一般可以按下 F12 来进行选择，若无效则可以通过 F2 进入到 BIOS 操作界面，找到 boot 相关的选项选择对应的 U 盘来启动，这里无法一一说明。

     如果不知道 UEFI 是什么，那这里也先不用去查它，看到有 UEFI 启动先以 UEFI 启动即可。简单来说，它是一个替代了老式 BIOS 新的固件接口，可用于引导系统的启动，且更适配 GPT 分区表（无需使用额外的 boot 分区）。扩展阅读请自行查阅。

     启动时，请注意提示信息， BIOS 模式下会多一个手动启动的提示，需要在 15s 内选择，否则会正常启动硬盘下的系统。

配置安装环境
==================================================

.. _`连接网络`:

连接网络
-----------------------------

有线
+++++++++++++++

1. 网络环境带 DHCP 服务的（比如家用路由器连接的），livecd 默认会运行 dhcpcd 服务，不出意外，进入环境后直接可以联网。可通过下述的 `ping 测试`_ 判断。
2. 网络环境无 DHCP 服务或 DHCP 无效需要手动配置网络的，需要知道网关 IP，可用的网络地址，然后执行如下命令：

   .. code-block:: shell

     # 先列出到当前使用的网卡
     ip link
     # 有线网卡的格式一般为 enpXsX, X 是一个数字
     # 假设这里看到了正在使用的网卡为 enp5s0
     ip link set dev enp5s0 up # 确保其开启
     # 这里假设　网关地址为： 10.0.1.1
     # 　　　可用网络地址为： 10.0.1.2
     # 　　　　　子网掩码为： 255.255.255.0 （即 CIDR 符号为 /24）
     ip address add 10.0.1.2/24 dev enp5s0
     ip route add default via 10.0.1.1 dev enp5s0
     # 这样就配置好了网卡的 IP 和默认路由
     # 未假设的内容即为固定参数，无需变动

   .. note::

     配置完成后可以执行以下命令查看当前的配置结果：

     .. code-block:: shell

       ip a
       # 查看 IP 地址信息，看到上述设置的网卡下有正确的 IP 地址即可

       ip r
       # 查看当前的路由信息，能看到首行有类似如下记录即可
       # default via 10.0.1.2 dev enp5s0 proto static metric 100


3. 拨号网络，执行 :code:`pppoe-setup` 根据提示配置好对应的值后，执行 :code:`pppoe-start` 进行连接。
4. 若仅存在 IPv6 环境，那么默认进入安装环境后，会直接进行路由协商获取可用的 IPv6 地址。如若无效，同样使用 :code:`ip` 命令自行配置（正常无需配置路由；因环境所限，没有更多 IPv6 环境测试，便不再说明）。

无线
+++++++++++++++

* 确定无线网卡设备，使用 :code:`iw dev` 进行查询， :file:`Interface` 后显示的即为无线网卡名，这里以 :file:`wlpXsX` 代替
* 确保清楚无线网络的 SSID（即无线网络名称），若不知，可以执行如下命令获取当前能检测到的所有 SSID：

  .. code-block:: shell

    iw dev wlpXsX scan | grep SSID
    # 其它信息可自行尝试

* 确保无线网卡设备开启

  .. code-block:: shell

    ip link set wlpXsX up

然后开始连接到无线网络：

1. 无认证的无线网络，执行如下命令连接

   .. code-block:: shell

     iw dev wlpXsX connect -w 「SSID」

   .. note::

     校园的开放网络，需要连接后打开网页以认证的，可以连接网络后执行 :code:`links` 命令打开网页后尝试认证。

2. WEP 认证的无线网络，执行如下命令连接

   .. code-block:: shell

     # 假设密码为 mypass
     iw dev wlpXsX connect -w 「SSID」 key 0:mypass
     # 若密码是十六进制的，比如为 6162636465，则
     iw dev wlpXsX connect -w 「SSID」 key d:0:6162636465

   .. note::

     *现在一般都弃用这种认证方式了*

3. WPA/WPA2/WPA3 认证的无线网络（如今常用的认证方式），执行如下命令连接

   .. code-block:: shell

     wpa_supplicant -i wlpXsX -c <(wpa_passphrase 「SSID」 「密码」)


认证通过连接上无线网络后，再采取和有线一样的方式进行联网配置，一般会直接由 DHCP 服务器给本机分配上 IP，如果没有，参考有线配置段落，将有线网卡替换为对应无线网卡即可。

DNS 及测试
+++++++++++++++

执行

.. code-block:: shell

  cat /etc/resolv.conf

查看 DNS 配置信息，通常使用 DHCP 配置的网络会自动获取到 DNS 地址后配置，如若没有，请执行

.. code-block:: shell

  echo 'nameserver 223.5.5.5' >/etc/resolv.conf

写入 DNS 配置，这里我选用的阿里云的公共 DNS 地址，也可以改成其它的。

.. _`ping 测试`:

再执行

.. code-block:: shell

  ping -c3 baidu.com
  # IPv6 使用 ping -6 -c3

查看返回信息，输出如下类似信息及联网成功

::

  PING baidu.com (220.181.38.251) 56(84) bytes of data.
  64 bytes from 220.181.38.251 (220.181.38.251): icmp_seq=1 ttl=53 time=28.5 ms
  64 bytes from 220.181.38.251 (220.181.38.251): icmp_seq=2 ttl=53 time=30.4 ms
  64 bytes from 220.181.38.251 (220.181.38.251): icmp_seq=3 ttl=53 time=29.6 ms

  --- baidu.com ping statistics ---
  3 packets transmitted, 3 received, 0% packet loss, time 2003ms
  rtt min/avg/max/mdev = 28.509/29.519/30.413/0.781 ms

如果长时间得不到响应或者直接显示失败，再自查网络配置或寻求帮助。

准备好分区
-----------------------------

作为新手教程，在这里往往会遇到在装有 Windows 系统的情况下安装 Linux 的情况，而硬盘也有可能是共用的，这些都无需担心，可以不影响到 Windows 一丝一毫，慢慢往下看。

.. note::

  今年是 2021 年，碍于篇幅，MBR 的分区不再说，只专注于 GPT 分区。如果你有一台很老的电脑，上面有一个采用 MBR 分区格式的 Windows 系统，想在保留 Windows 的情况下安装 Gentoo Linux，请点击文章开头的群组以寻求帮助。

***注意备份好资料***

确保有一片比较大的空闲硬盘空间或者一个完整的无用硬盘

* 仅用于测试，5G 空间够用
* 日常使用，至少 30G 空间，越大越好

本文不会涉及到硬盘加密， RAID 和 LVM

如果熟悉分区，可自行配置，只要确保满足以下条件即可跳过本节：

1. BIOS 启动，GPT 分区情况下，需要有一个 2M 大小的 :file:`BIOS boot` 分区，无需配置文件系统。
2. 配置 UEFI 启动情况下，需要有一个 100M （建议大小）的 EFI 分区，并格式化为 FAT32 文件系统。
3. 一个可以挂载到 :file:`/` 目录的格式化完成的分区。

如果不熟悉，请看以下内容

执行

.. code-block:: shell

  lsblk

列出当前所有的块设备，硬盘对应的名称一般为 :file:`sdX` ， :file:`nvmeXnX` 这种（虚拟机下可能为 :file:`vdX` ），其中 :file:`X` 为英文字母或阿拉伯数字。

确定好需要操作的块设备，这里假设为 :file:`sdX` ，然后执行自带的 :code:`fdisk` 命令进行分区（分区工具很多，这里仅以该工具为例）

.. code-block:: shell

  fdisk /dev/sdX

*若硬盘是与其它系统共用，仅有部分空闲空间的用于安装 Gentoo Linux 的，有些命令可能是无需操作的，对于这些命令，我会在命令后使用* :code:`#!!!` *这样的注释进行提醒，并说明；如果你是在一块完整的硬盘上安装，可以输入以下完整的命令*

执行上述命令后，进入了 :code:`fdisk` 交互界面，继续执行如下操作

.. note::

  在执行写入分区表操作（即 :code:`w` 命令）前，分区表不会实际更改，如若出错，可以执行 :code:`q` 退出交互界面重新进入再次操作

  如果使用的是已经被分过区的硬盘，那么创建过程中可能会出现红色的类似 :file:`Partition #3 contains a ext4 signature` 这样的提示信息，之后会让你选择 :file:`[Y]es/[N]o` ，输入 :file:`Yes` 回车覆盖数据即可。

.. code-block:: shell

  # [1]号命令
  p # 列出当前的分区情况

  # [2]号命令
  g #!!! 确保当前分区表为 GPT 格式
    #      此操作最终会破坏硬盘原有数据
    #      共用硬盘情况下不要操作！！！

  # [3]号命令
  n #!!! 先新建一个 2M 的 BIOS boot 分区
    #      这对于以 BIOS 启动的情景是必须的
    #      对于 UEFI 启动的情景也是无害的（此情景下可以不建）
    #      在系统共用硬盘情况，若已经存在，则无需再建
  「回车以选择默认值」 # 这里是当前分区的分区号，选择默认值并记住
  「回车以选择默认值」
  +2M

  # [4]号命令
  t #!!! 更改分区类型，[3]号命令执行情况下执行
  「数字」 # 输入[3]号命令记录分区号以选择该分区
  　　　　 #   当仅存在一个分区的情况下，这个步骤会略过，注意提示信息
  4 # 4 号即为 BIOS boot 类型，也可以输入 L 列出所有类型进行确认

  # [5]号命令
  n #!!! 再新建一个 100M 的 EFI 分区
    #      这对于以 UEFI 启动的情景是必须的
    #      对于 BIOS 启动的情景也是无害的（若后续无更换为 UEFI 打算，则可以不建）
    #      在系统共用硬盘情况，若已经存在（类型标记为 EFI System），可无需再建
  「回车以选择默认值」 # 这里是当前分区的分区号，选择默认值并记住
  「回车以选择默认值」
  +100M

  # [6]号命令
  t #!!! 更改分区类型，[5]号命令执行情况下执行
  「数字」 # 输入[5]号命令记录分区号以选择该分区
  　　　　 #   当仅存在一个分区的情况下，这个步骤会略过，注意提示信息
  uefi # uefi 为 EFI System 类型的别名，也可以输入 L 列出所有类型进行确认

  # [7]号命令
  n # 建立启动分区
    #   建立一个独立于根分区的系统启动分区（一般也建议这样做）
    #   这里选择 500M 的大小，作为 Gentoo Linux，这个大小可以放下很多的内核供玩耍
  「回车以选择默认值」
  「回车以选择默认值」
  +500M

  # [X]号命令
  n # 建立交换分区「可选」
    #   根据自己的需求判断是否需要建立此交换分区（在硬盘足够大的情况下，推荐建立）
    #   交换分区用于在电脑内存不足时，代替内存存储数据，用于弥补内存不足的问题
    #   　　　　也用于在内存足够时，将一部分不常用的数据写入到这个分区下，以提高内存命中率
    #   　　　　还用于保存电脑休眠时内存下的数据
    #   当然，即使没有交换分区，也可以创建交换文件以起到相同的作用，性能一样，还更灵活
    #   但在某些情况下，交换文件会阻碍一些功能，比如 BtrFS 的快照
    # 【参考建议】
    #   如果，CPU 有 8 核 16 线程，内存 16G 或者更低
    #   　　　那么建议建立至少 8G 的交换分区（也可以选择之后再建立交换文件）
  「回车以选择默认值」 # 这里是当前分区的分区号，选择默认值并记住
  「回车以选择默认值」
  +6G # 这里的 6G 我输入的是一个较为通用的值，实际上你可以根据自己的情况来给
      # 比如你内存有 32G，日常占用 20G，需要休眠功能，那么这里至少也得 20G

  # [X1]号命令
  t #!!! 更改分区类型，[X]号命令执行情况下执行
  「数字」 # 输入[X]号命令记录分区号以选择该分区
  　　　　 #   当仅存在一个分区的情况下，这个步骤会略过，注意提示信息
  swap # swap 为 Linux swap 类型的别名，也可以输入 L 列出所有类型进行确认

  # [8]号命令
  n # 建立根目录分区
    #   个人建议这里把剩余空间都分给根目录分区
  「回车以选择默认值」
  「回车以选择默认值」
  「回车以选择默认值」 # 这里的默认值是可以选择的最大值

  # [9]号命令
  w # 最后写入此次修改后的分区表

这样一个分区表就准备好了，接下来格式化分区，除了 EFI 分区必须为 FAT32 格式外，其它分区的可选格式范围很广。一般来说 ext4 适用性最广，这里就用 ext4 为例。

.. note::

  其它我个人推荐的文件系统有 xfs, BtrFS, zfs；当然 zfs 需要额外编译内核模块，新手安装不建议考虑。

  BtrFS 则是我一直使用的文件系统，有写时复制，子卷，快照，透明压缩等一系列功能，对 SSD 也有额外优化；但埋汰 BtrFS 的也不少。如果考虑采用 BtrFS，建议先了解清楚。它现在是 openSUSE 和 Fedora 桌面变体的默认文件系统。

  xfs 我没用过但用的人挺多的。是 Red Hat Enterprise Linux 的默认文件系统。

执行

.. code-block:: shell

  fdisk -l /dev/sdX

查看现在的分区表，记住现在的 EFI 分区（ EFI System ，若有），启动分区（ 500M 的 Linux filesystem ），交换分区（ Linux swap ，若有）以及根分区（最大的 Linux filesystem ）的设备名。这里假设

* EFI 分区设备为 :file:`/dev/sdX2`
* 启动分区设备为 :file:`/dev/sdX3`
* 交换分区设备为 :file:`/dev/sdX4`
* 根分区设备为 :file:`/dev/sdX5`

那么执行

.. code-block:: shell

  # 格式化 EFI 分区为 FAT32（若有）
  # 如果和其它系统共用的 EFI 分区，这一步跳过
  mkfs.vfat -F 32 /dev/sdX2

  # 格式化启动分区为 ext4
  mkfs.ext4 /dev/sdX3

  # 设置交换分区（若有）
  mkswap /dev/sdX4

  # 格式化根分区为 ext4
  mkfs.ext4 /dev/sdX5

最后，挂载好准备的分区

.. code-block:: shell

  # 挂载根分区
  mount /dev/sdX5 /mnt/gentoo

  # 挂载启动分区
  mkdir /mnt/gentoo/boot
  mount /dev/sdX3 /mnt/gentoo/boot

  # 起用交换分区（若有）
  swapon /dev/sdX4

  # 如果你是 UEFI 环境，安装 UEFI 启动，则挂载上 EFI 分区
  # 这里我设定 EFI 分区挂载到启动目录下的 efi 路径上
  mkdir /mnt/gentoo/boot/efi
  mount /dev/sdX2 /mnt/gentoo/boot/efi

至此，分区准备完成，到这就准备好了所需的安装环境。

进行安装
==================================================

获取基本系统
-----------------------------

.. _`关于 sshd 设置的提示`:

.. tip::

  如果你通过的是虚拟机安装，或者同一网络下有其它电脑可以使用，那么使用 ssh 连接上本机，通过复制粘贴命令来操作会更加方便，而 LiveCD 环境下的 sshd 配置为，执行，

  .. code-block:: shell

    nano /etc/ssh/sshd_config

  打开 sshd 配置文件，确保如下两个选项

  * PermitRootLogin
  * PasswordAuthentication

  前面都没有注释符 :code:`#` ，后面的值都为 :code:`yes` ，后按下 :kbd:`Ctrl` + :kbd:`X` ， :kbd:`y` ， :kbd:`Enter` 保存退出。之后执行，

  .. code-block:: shell

    rc-service sshd start

  启用 sshd 服务后，为 LiveCD 环境的 root 用户设置一个密码，

  .. code-block:: shell

    # 如果不想设置复杂密码，可以编辑 /etc/security/passwdqc.conf 文件
    # 将 enforce=everyone 改成 enforce=none 保存后再设置
    passwd root

  之后就可以通过其它电脑/主机连接到此 LiveCD 环境了。

首先调整好当前的系统时间，偏差的时间会导致后续一些问题（比如编译过程依赖系统时间）。执行

.. code-block:: shell

  ntpd -q -g

成功后使用 :code:`links` 命令访问镜像服务器，执行

.. code-block:: shell

  links https://mirrors.bfsu.edu.cn/gentoo/

打开后，使用方向及回车键定位到 :file:`releases/amd64/autobuilds/` 目录。

在这里，你需要确定你想要安装 Gentoo Linux 的哪个 *profile* ，关于 *profile* 的详细说明可以看 `对应的 wiki`_ ，简单说明即，它是一个完整的系统配置集合，不同的 *profile* 在安装完成后可以自行切换，但在安装过程中，只能使用下载好的 stage3 所用的 *profile* 进行。常用的几个 *profile* 属性说明：

* openrc: 带此单词表示，其默认的初始化程序为 openrc
* systemd: 带此单词表示，其默认的初始化程序为 systemd，而不带该单词所有 *profile* ，默认初始化程序都是 openrc （即 Gentoo Linux 官方默认）
* nomultilib: 带此单词表示，其不包含 32 位的系统库文件，即无法执行 32 位程序
* selinux: 带此单词表示，其默认包含 SELinux 相关配置，启用 SELinux
* hardened: 带此单词表示，其默认包含强化安全性相关的配置

正常使用情况下，推荐如下两个 stage3 进行下载：

* current-stage3-amd64-openrc
* current-stage3-amd64-systemd

openrc 是 Gentoo Linux 官方维护且默认的初始化程序，而 systemd 则是如今大多数发行版使用的初始化程序，各有优劣，二者均可，自行选择。

.. tip::

  `2021-10-18 起`_ ，官方开始上传 openrc/systemd 所对应 desktop profile 的 stage3 文件，如果目的是为了安装桌面环境，那么可以从这两个里面进行选择以缩短安装时间。

.. warning::

  以下 stage3 这里不推荐选择：

  * musl 相关，目前在 Gentoo 上处于实验状态，一些命令也可能不适用
  * uclibc 相关，适用嵌入式环境，目前在 Gentoo 上处于实验状态
  * x32 相关，目前在 Gentoo 上处于实验状态

.. note::

  随着时间的推移， stage3 包名可能会略有改动，如果后续发现有存在改动，请从更新时间最靠近的一批 stage3 文件中选择并下载。

这里以 :file:`current-stage3-amd64-openrc` 为例，那么

1. 选择进入该目录
2. 选中 :file:`stage3-amd64-openrc-{日期}.tar.xz` 文件，回车进行下载
3. 这里请同时下载其校验文件 :file:`stage3-amd64-openrc-{日期}.tar.xz.DIGESTS`

默认存储路径为执行 :code:`links` 的当前目录，下载完成后，按 :kbd:`q` 退出，执行

.. code-block:: shell

   # 列出当前目录下的内容，确保两个下载的文件存在
   ls

   # 使用 sha512sum 校验文件
   sha512sum -c --ignore-missing stage3-amd64-openrc-{日期}.tar.xz.DIGESTS

.. note::

  可选步骤
    如果想要进行更加严格的验证，可替换下载原 :file:`.DIGESTS` 文件为 :file:`stage3-amd64-openrc-{日期}.tar.xz.DIGESTS.asc` ，后退出 links 界面，执行

    .. code-block:: shell

      # 导入 Gentoo Linux 的发布公钥
      gpg --keyserver hkps://keys.gentoo.org --recv-keys 0x13EBBDBEDE7A12775DFDB1BABB572E0E2D182910

      # 校验 DIGESTS 文件
      gpg --verify -o stage3-amd64-openrc-{日期}.tar.xz.DIGESTS{,.asc}

    提示 :code:`Good signature from "Gentoo Linux Release Engineering (Automated Weekly Release Key) <releng@gentoo.org>"` 则校验成功，否则说明文件有损坏或被篡改（警告可不用理会）。

    之后再进行上述正常校验压缩包的操作。

确保无错误提示后继续。如果出错，说明下载的文件不完整，请重新下载。

解压 stage3 到根目录
-----------------------------

执行

.. code-block:: shell

  # 切换到挂载根分区的目录下
  cd /mnt/gentoo

  # 解压 stage3 文件，这里默认之前执行 links 的目录为家目录（没进行切换的话）
  # 　　        　　　若之前是切换了目录后执行的 links，请自行修改
  tar xpvf /root/stage3-amd64-openrc-{日期}.tar.xz --xattrs-include='*.*' --numeric-owner

.. _`配置镜像地址`:

配置镜像地址
-----------------------------

为了更快速的下载文件，配置一个离自己近的镜像服务器地址很重要，执行

.. code-block:: shell

  mirrorselect -i -o >>/mnt/gentoo/etc/portage/make.conf

会打开一个界面供选择镜像地址，比如在中国的话，可选 aliyun/netease/tsinghua 的（发文时， aliyun 的还是老延迟），使用空格选中，回车保存。

.. note::

  如果因为连接国外网络不畅的原因，导致获取列表失败，这时候也可以直接手动指定一个镜像：

  .. code-block:: shell

    echo 'GENTOO_MIRRORS="https://mirrors.bfsu.edu.cn/gentoo/"' >>/mnt/gentoo/etc/portage/make.conf

  后继续下一个步骤。

chroot 到目标系统
-----------------------------

执行

.. code-block:: shell

  # 复制 DNS 配置到目标系统环境
  cp -L /etc/resolv.conf /mnt/gentoo/etc/

  # 挂载必要的文件系统
  # /proc 是一个由内核暴露信息到环境下的伪文件系统
  mount --types proc /proc /mnt/gentoo/proc
  # /sys 是类似 /proc 但比其更结构化的伪文件系统
  mount --rbind /sys /mnt/gentoo/sys
  # /dev 是由 udev 管理，包含所有设备文件的普通文件系统
  mount --rbind /dev /mnt/gentoo/dev

.. note::

  如果之前选择的是 systemd 的 stage3 文件，那么在这里，你需要额外再运行两个命令

  .. code-block:: shell

    mount --make-rslave /mnt/gentoo/sys
    mount --make-rslave /mnt/gentoo/dev

之后执行如下进入到目标系统环境：

.. code-block:: shell

  # chroot 到目标系统环境
  chroot /mnt/gentoo
  # 导入环境信息
  . /etc/profile
  # 修改提示符以便于区分
  PS1=(chroot)$PS1


获取 portage 数据库
-----------------------------

执行

.. code-block:: shell

  emerge-webrsync

该命令会从之前配置好的镜像地址下载最近打包好的 portage 数据库到本地，并解压后使用。 *portage* 是 Gentoo Linux 的包管理器，这个数据库是安装各种软件的基础。

.. warning::

  如果这里发现下载速度明显很慢，那可能是上述 `配置镜像地址`_ 未配置到合适的镜像点，建议重新配置。

.. note::

  安装好数据库后，基本都会有一个让阅读新闻的提示，运行命令

  .. code-block:: shell

    eselect news read --quiet

  来标记全部阅读，这些信息对于全新的安装环境来说，很多都是过期的，不看问题也不大。之后可以运行

  .. code-block:: shell

    eselect news list

  以列出所有新闻的标题，再根据序号选择性地查看有用的信息（比如近期的新闻）

  .. code-block:: shell

    eselect news read 「序号」

确定首选编辑器
-----------------------------

Gentoo Linux 默认安装的编辑器为 :code:`nano` ，这是一个初始设置下就很适合新手的编辑器，如果你有其它的要求，比如想使用 :code:`vim` 或者 :code:`emacs` ，可以先安装

.. code-block:: shell

  # 若安装 vim 则执行
  emerge -vj app-editors/vim

  # 若安装 emacs 则执行
  emerge -vj app-editors/emacs

无论是否有安装其它编辑器，这里都需要选择一下默认的编辑器

.. code-block:: shell

  # 列出当前存在的编辑器
  eselect editor list

  # 根据所需要的编辑器对应的序号，设置默认
  eselect editor set 「序号」

  # 之后再运行一次
  . /etc/profile
  PS1=(chroot)$PS1


安装固件、内核及引导
-----------------------------

执行

.. code-block:: shell

  # 提示：对于虚拟机环境而言，以下步骤[1]一般无需进行，
  # 　　　　　　　　　　　　　步骤[2]内的 linux-firmware 也无需添加

  # [1]
  # 同意 Linux 固件的协议
  # 先创建一个文件夹，以便于管理
  mkdir -p /etc/portage/package.license
  # 再创建文件以同意对应协议
  echo 'sys-kernel/linux-firmware linux-fw-redistributable no-source-code' >/etc/portage/package.license/linux-firmware

  # [2]
  # 安装固件、内核及 grub 安装器
  emerge -vj linux-firmware gentoo-kernel-bin grub

该命令会为系统安装 Linux 固件文件、二进制内核以及 Grub 安装器。

Linux 固件文件
  这里的固件文件是一系列固件的集合，它们为某些硬件（无线网卡、蓝牙、显卡等）提供支持。因为其通常是私有的，所以这里需要同意额外的许可。

内核
  它是系统软件与硬件的中间层，必要。

Grub 安装器
  用于给计算机安装 Grub 引导程序，碍于篇幅，这里不打算介绍其它引导器，且 Grub 功能完善、成熟，建议安装。


配置 fstab
-----------------------------

执行

*注意替换下述命令中的设备名 sdXN*

.. code-block:: shell

  # 记录启动分区的 UUID 值到 fstab 文件
  blkid /dev/sdX3 >>/etc/fstab

  # 如果是配置 UEFI 启动记录，那么记录 EFI 分区的 UUID 值到 fstab 文件
  blkid /dev/sdX2 >>/etc/fstab

  # 记录交换分区的 UUID 值到 fstab 文件（若有）
  blkid /dev/sdX4 >>/etc/fstab

  # 记录根分区的 UUID 值到 fstab 文件
  blkid /dev/sdX5 >>/etc/fstab

记住这个顺序，后使用编辑器打开 :file:`/etc/fstab` 文件

.. code-block:: shell

  # 比如 nano
  nano /etc/fstab

打开文件后可以看到示例配置，你需要删除之前新添加行（不被 :code:`#` 注释的）的除了 :code:`UUID="XXXX...XXXX"` 字段外其它的所有内容。

根据之前添加进去的顺序，依次配置到如下值：

.. code-block:: shell

  # 启动分区
  UUID="XXXXXXXX-...XXXX"  /boot       ext4  rw,noatime,errors=remount-ro 0 2
  # EFI 分区（若有）
  UUID="XXXX-XXXX"         /boot/efi   vfat  rw,noatime,errors=remount-ro 0 2
  # 交换分区（若有）
  UUID="XXXXXXXX-...XXXX"  none        swap  sw                           0 0
  # 根分区
  UUID="XXXXXXXX-...XXXX"  /           ext4  defaults,noatime             0 1

安装并配置引导
-----------------------------

安装
+++++++++++++++

这里区分为两种情况：

1. BIOS 启动，执行

   .. code-block:: shell

     grub-install --target=i386-pc /dev/sdX

   显示无报错即安装完成。

2. UEFI 启动，执行

   .. code-block:: shell

     grub-install --target=x86_64-efi --efi-directory=/boot/efi/ --bootloader-id=Gentoo

   显示无报错即安装完成。

   .. note::

     这里值得注意一点，一些旧主板（还有一些虚拟机环境）有可能存在不识别指定位置 EFI 实体的情况，这种情况下需要执行：

     .. code-block:: shell

       grub-install --target=x86_64-efi --efi-directory=/boot/efi/ --removable

     将 EFI 实体安装到通用目录下。非虚拟机环境无需直接尝试，等发现无法启动后再来操作。

配置
+++++++++++++++

执行

.. code-block:: shell

  # （可选）如果之前有分配交换分区，在这里可以执行如下命令以启用其休眠后唤醒的功能
  sed -Ei "/GRUB_CMDLINE_LINUX_DEFAULT/s/^#*(GRUB.*DEFAULT=).*$/\1\"resume=UUID=$(blkid -o value /dev/sdX4 | head -1)\"/" /etc/default/grub
  # 也可以手动修改，打开 /etc/default/grub 文件
  # 　　　找到 GRUB_CMDLINE_LINUX_DEFAULT 变量
  # 　　　去掉其注释标记 (#) 后
  # 　　　在其双引号内添加上内容：
  # 　　　　　　　resume=UUID=<UUID 值>
  # 　　　此 <UUID 值> 可由命令 blkid -o value /dev/sdX4 | head -1 显示

  # （必要）创建配置
  grub-mkconfig -o /boot/grub/grub.cfg

以完成引导的配置，该命令会自动根据 :file:`/etc/fstab` 以及 :file:`/etc/default/grub` 的内容来生成所需要的引导配置。

.. note::

  如果电脑存在多系统，可以执行如下步骤添加其它系统的引导菜单选项

  .. code-block:: shell

    # 给 grub 添加 mount 这个 USE 以满足 os-prober 的依赖
    echo 'sys-boot/grub mount' >/etc/portage/package.use/grub

    # 安装 os-prober 工具
    emerge -vj os-prober
    # 如果你上面进行了可选操作，更新了 grub 配置文件，那么
    # 安装完成后可能会有一个关于 Grub 的配置文件更新提示
    #   IMPORTANT: config file '/etc/default/grub' needs updating.
    # 这个暂时不用理会，后面「关于配置文件的更新」一节会讲如何处理这种情况

    # 配置 grub 以启用 os-prober 功能
    echo 'GRUB_DISABLE_OS_PROBER=false' >>/etc/default/grub

  之后再次运行一次上述的 :code:`grub-mkconfig` 命令，该命令会自动识别同一机器上其它的系统，并做成引导菜单选项。

自此，一个基本的可以启动的系统安装完成。但还需要进行一些基本的收尾工作。

配置基础系统
==================================================

设置用户
-----------------------------

1. 设置 root 用户密码，执行

   .. code-block:: shell

     passwd root

   后根据提示，设置好 root 用户密码（如果你是第一次在 Linux 下输入密码，不要奇怪为何输入时无任何字符提示，这是正常的）。

2. 创建一个平常使用的普通用户

   .. code-block:: shell

     # 通常情况下，建议日常通过普通用户来使用系统
     # 创建普通用户，同时将其额外添加到 usb 组，以使其可以访问 USB 设备
     # 　　　　　　　　　　　　　　　　 wheel 组，以使其可以使用 su 命令
     # 这里的用户名只能是字母和数字，数字不能打头，不要给空格
     useradd -m -G usb,wheel 「用户名」
     # 这里可能有一个关于 mail 文件夹不存在的提醒
     #   Creating mailbox file: No such file or directory
     # 忽略即可

     # 设置普通用户密码
     passwd 「用户名」

     # （可选）
     # 安装 sudo 并修改配置文件
     # 使普通用户可以以超级权限执行命令
     emerge -vj app-admin/sudo
     visudo # 打开配置文件，找到 #%wheel 开头的几行设置
            # 根据说明去掉所需配置行的注释符号

配置网络
-----------------------------

之前配置的是 LiveCD 环境下的网络，这里为新系统环境配置网络（如果你需要的话）。

最方便的支持多种联网方式的工具是 NetworkManager ，基本能满足所有需求，但同时它的依赖项会有一点多。如果此系统用来作为桌面环境，那么建议安装它，执行

.. code-block:: shell

  # 添加必要的 USE 标记以解决依赖关系（什么是 USE 见下文 USE 标记 一节）
  echo "net-wireless/wpa_supplicant dbus" >>/etc/portage/package.use/nm
  echo "net-misc/openssh -bindist" >>/etc/portage/package.use/nm
  # （随着时间的推移，可能后续会有其它依赖关系问题，若出现，访问本文开头群组寻求帮助）

  # 安装 NetworkManager
  # 这里为了处理依赖关系，所以稍有复杂
  emerge -vj1 net-misc/openssh net-misc/networkmanager
  emerge -On net-misc/networkmanager

.. note::

  如果觉得 NetworkManager 的依赖太多了，想要简单一点的工具就能满足的话，参考准备安装环境的 `连接网络`_ 一节，具体需要的工具为

  * 有线网络： openrc 下有自带的 :file:`net-misc/netifrc` ； systemd 下有自带的 :file:`systemd-networkd` 即可
  * 无线网络： 在有线网络要求下，额外需要 :file:`net-wireless/wpa_supplicant` 或 :file:`net-wireless/iwd` ，用于连接和认证
  * PPPoE 环境： 在上述要求下还需要 PPPoE 客户端，比如 :file:`net-dialup/ppp`

  碍于篇幅，具体使用和配置方式请自行查阅相关维基。

安装完成后，由于此时处于 chroot 环境，所以暂时无法运行此工具，等之后重启后可进行可视化配置，下文会说。

之后添加开机启动服务

.. code-block:: shell

  # 若你是安装的 openrc 系统，执行
  rc-update add NetworkManager default

  # 若你是安装的 systemd 系统，执行
  systemctl enable NetworkManager

安装日志服务
-----------------------------

这段仅针对 openrc 用户，systemd 则有自带的日志服务。

openrc 这里我推荐使用 :gepkg:`app-admin/syslog-ng` ，执行

.. code-block:: shell

  # 安装
  emerge -vj app-admin/syslog-ng

  # 添加开机启动
  rc-update add syslog-ng default

其默认的配置即可使用。

至此，一个基础的 Gentoo Linux 系统安装完成。

重启
-----------------------------

重启进入新的系统环境：

.. code-block:: shell

  # 同步一下当前的文件系统
  sync

  # 退出 chroot 环境
  exit

  # 卸载所有挂载的文件系统
  umount -Rl /mnt/gentoo/{dev,proc,sys,}

  # 重启
  reboot

使用 Gentoo Linux
==================================================

重启后会出现预期中的 Grub 菜单界面，倒计时后会自动进入首选引导项，加载内核，启动初始化程序，最后进入操作系统。

这时候的 Gentoo Linux 只有一个命令行界面，先使用 root 用户登陆到系统。

登陆后完成上述没有进行完的网络配置，执行 :code:`nmtui` 进入到可视化的配置界面，根据提示把网络配置完成。

.. tip::

  网络配置完成后，如果还是想通过 SSH 登陆到此电脑后执行命令，依旧参考上述 `关于 sshd 设置的提示`_ 。只不过运行 sshd 的命令需要根据此时的环境来， openrc 下和上述相同， systemd 下则使用命令 :code:`systemctl start sshd` 。

完成基础配置
-----------------------------

配置时区
+++++++++++++++

这里假设设置为国内时区，执行

.. code-block:: shell

  # 通用操作
  # 将时区信息写入指定文件
  echo 'Asia/Shanghai' >/etc/timezone
  # 删除旧的常规文件以避免警告
  rm /etc/localtime
  # 更新时区信息
  emerge --config sys-libs/timezone-data

  # systemd 用户可选的替换操作
  #timedatectl set-timezone Asia/Shanghai

如果你需要添加其它的时区，对应的时区名字可以在 :file:`/usr/share/zoneinfo/` 目录下找到，将其替换到 :file:`Asia/Shanghai` 的位置后执行命令即可。

.. note::

  设置完时区后，可以执行以下命令查看效果：

  .. code-block:: shell

    date

语言环境
+++++++++++++++

准备系统语言环境。对于 root 用户而言，一般使用默认的配置即可。但这里需要添加上自己所需其它语言设置以供普通用户使用。

使用编辑器打开 :file:`/etc/locale.gen` 文件，在里面添加上你需要的语言环境配置，说明如下：

.. code-block:: shell

  # 这个配置是默认存在的，不用去修改它
  C.UTF8 UTF-8
  # 空格前代表该语言环境的名字，后代表选择的编码
  # 在这里，C 是一个为计算机适配的语言环境，英文，兼容性强，root 用户下推荐使用它

  # 下面是推荐添加的语言环境

  # 生活在中国则添加
  zh_CN.UTF-8 UTF-8

  # 若 生活在其它国家
  # 　 或需要其它国家对应的 数字、货币、日期等表示格式，
  # 则添加对应国家的语言环境配置
  # 配置格式为 <语言>_<国家代码>[@可选的变体].<编码> <编码>
  # 其中，
  # 　　<语言>_<国家代码>[@可选的变体] 可以在 /usr/share/i18n/locales/ 文件夹下找到
  # 　　而支持的 <编码> 可以在 /usr/share/i18n/charmaps/ 文件夹下找到
  # 　　编码一般只推荐使用 UTF-8，除非有明确的其它需求

.. _`about-locale-name`:

.. tip::

  如果你在好奇，为何默认存在的 Locale 名是 :file:`C.UTF8` ，而我要你添加的却是 :file:`zh_CN.UTF-8` ，那个小短横（ :file:`-` ）到底需不需要，我在这里说明。

  在正常的 GNU Library C 环境下（MUSL 等其它环境不考虑），标准的 glic 库 Locale 名识别中，在 2004 年十一月将 UTF8 与 UTF-8 均判断为 UTF-8 编码，且不区分大小写，所以上面关于名字的设置都是可以的。不过就正常来说，还是 :file:`UTF-8` 更规范。

  如今的相关代码为

  .. code-block:: c

    codeset_name = nl_langinfo (CODESET);
    if ((codeset_name[0] == 'U' || codeset_name[0] == 'u')
        && (codeset_name[1] == 'T' || codeset_name[1] == 't')
        && (codeset_name[2] == 'F' || codeset_name[2] == 'f')
        && strcmp (codeset_name + 3 + (codeset_name[3] == '-'), "8") == 0)
      dfa->is_utf8 = 1;

  也可以查看 `glibc 的 git 仓库`_ （具体的 commit 为 :file:`e40a38b` 和 :file:`eb04c21` ）。

  至于空格后的则是设定的编码名字，需要规范填写。

当添加了其它语言环境配置后，执行

.. code-block:: shell

  locale-gen

该命令会根据 :file:`/etc/locale.gen` 下配置的内容，生成所需语言环境列表。

.. note::

  如果你有需求要在此刻为 root 用户变更语言环境，可以执行

  .. code-block:: shell

    eselect locale list
    # 以列出当前的语言环境列表，后

    eselect locale set 「序号」
    # 来设置所需语言环境，再

    env-update
    # 更新环境配置，最后

    . /etc/profile
    # 为当前 shell 加载环境配置

时间同步
+++++++++++++++

为保证时间的精准，

1. 启用对网络的时间同步服务。这里我推荐使用 :gepkg:`net-misc/chrony` 这个同步软件，执行

   .. code-block:: shell

     # 安装
     emerge -vj net-misc/chrony

     # 配置 chrony 以 UTC 对待硬件时钟
     echo $'\n'rtconutc >>/etc/chrony/chrony.conf

   安装完成后，执行

   .. code-block:: shell

     # openrc 用户
     rc-service chronyd start
     rc-update add chronyd default

     # systemd 用户
     systemctl --now enable chronyd

   启动服务并开机启动。

   .. note::

     也还有其它的时间同步软件，比如 :file:`net-misc/ntp` , :file:`net-misc/openntpd` 等，可以根据需要选择。

2. 确保与硬件时钟的同步。即在系统启动时将硬件时钟同步到系统时间，并在关闭系统时（或运行过程中定时）将系统时间同步回硬件时钟。

   （此节略显繁琐，如果你初入 Linux ，对此节略感迷惑，可以跳过，不影响大局）

   （如果你永不断互联网，那忽略这一节也可以）

   在 openrc 下，会有一个默认启用的名为 :file:`hwclock` 的服务负责此功能。

   在 systemd 下却没有默认的服务用于将系统时间自动同步回硬件时钟。

   而自 3.8 及以上版本的 Linux 内核开始，可以配置交由内核来全权负责此功能。

   .. note::

     本文至目前只介绍预编译好的二进制内核，在写这篇文章时「2021 年，十月初」，Gentoo Linux 下二进制内核稳定版为 :file:`5.10.XX` ，其默认未开启系统时间到硬件时钟的同步功能；测试版为 :file:`5.14.XX` ，其默认配置则开启了完整的硬件时钟同步功能。

   判断当前内核是否开启了对应功能，可以通过如下命令进行验证，执行

   .. code-block:: shell

     zgrep 'CONFIG_RTC_[H|S]' /proc/config.gz

   当输出内容存在

   .. code-block:: shell

     CONFIG_RTC_HCTOSYS=y
     CONFIG_RTC_HCTOSYS_DEVICE="rtc0"

   表示开启了在启动或恢复系统时从硬件时钟同步时间的功能。

   .. note::

     即使此配置未开启，内核也会有一个基础功能用于尝试获取硬件时钟信息，但可能会在启动时导致额外的文件系统检查，所以一般都是开启的。

   当输出内容存在

   .. code-block:: shell

     CONFIG_RTC_SYSTOHC=y
     CONFIG_RTC_SYSTOHC_DEVICE="rtc0"

   表示开启了通过 NTP 同步将系统时间每隔约 11 分钟同步到硬件时钟的功能。没错，这个需要 NTP（即上述的时间同步服务）来辅助，chrony 默认配置已经支持。

   当输出的内容存在被注释的情况（行首有一个 :code:`#` ）则代表对应功能未开启。

   systemd 用户
     **确保以上两个功能均开启即可跳过。**

     若未开启，那么此时有两个选择：

     一、 安装测试版内核，执行

     .. code-block:: shell

       # 添加基于本机架构的测试用关键字以解除测试版软件的安装屏蔽
       echo 'virtual/dist-kernel' >>/etc/portage/package.accept_keywords
       echo 'sys-kernel/gentoo-kernel-bin' >>/etc/portage/package.accept_keywords

       # 更新到测试版二进制内核
       emerge -vuj gentoo-kernel-bin

       # 更新 Grub 引导信息
       grub-mkconfig -o /boot/grub/grub.cfg

       # 重启系统
       reboot

     后再次判断功能是否已经完整开启。若依旧未，说明包维护人员再次改动了默认配置，此时只能选择自行配置内核。

     二、 自行配置内核，请参考下文 `内核配置`_ 章节，若遇问题建议寻求帮助。

     这里略作说明，可以在内核源码目录下，执行 :code:`make menuconfig` 进入菜单配置界面，确认开启如下选单下的选项::

       Device Drivers  --->
         [*] Real Time Clock  --->
           [*]   Set system time from RTC on startup and resume
           (rtc0)  RTC used to set the system time
           [*]   Set the RTC time based on NTP synchronization
           (rtc0)  RTC used to synchronize NTP adjustment
           ...
           [*]   /sys/class/rtc/rtcN (sysfs)
           [*]   /proc/driver/rtc (procfs for rtc0)
           [*]   /dev/rtcN (character devices)
           ...
           <*>   PC-style 'CMOS'
           ...

     后保存退出，编译并安装内核，最后更新引导重启。

   openrc 用户
     无论什么内核什么配置，openrc 默认都会有完好的与硬件时钟的同步功能。

     **但，当完整地将同步功能交给内核后** （根据上文进行判断），建议关闭其自带的同步服务，执行

     .. code-block:: shell

       #!!! 以下内容判断后操作

       # 删除 hwclock 开机启动
       rc-update delete hwclock boot

       # 添加一个空的时钟服务以满足其它服务的要求
       rc-update add osclock boot

   到此时，时间同步配置完毕。

   .. note::

     在与 Windows 组双系统的情景下需要注意：

     Windows 默认是将硬件时钟视为当地时间（而非 UTC），而 Linux 则默认将硬件时钟视为 UTC，为避免冲突，在此情景下建议更改 Windows 的默认行为，将硬件时钟修改为 UTC，可以在 Windows 系统上操作，具体方法：

     按下 :kbd:`⊞ Win` + :kbd:`r` 后输入 :code:`regedit` 运行打开注册表编辑器，在 :file:`HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\TimeZoneInformation` 路径下，创建一个名为 :file:`RealTimeIsUniversal` 的 :file:`QWORD` 类型条目，将其值设为 :code:`1` ，之后重启系统。

     （如果你是 32 位的 Windows 系统，那么将 :file:`QWORD` 类型改为 :file:`DWORD` 类型）

Portage 配置
+++++++++++++++

Portage 是 Gentoo Linux 默认的包管理器，用于更新系统，安装各种所需软件。

Gentoo Linux 上绝大部分的软件是自行从源码编译安装而来的，所以编译过程中的一些参数也可以自由调节，这里说明几个基础配置。

make.conf
~~~~~~~~~~

:file:`/etc/portage/make.conf` 这个文件是 portage 的主配置文件，它控制了 portage 系统的绝大部分变量，你可以执行 :code:`man make.conf` 看到详细的说明。

它有一个预配置好的模板文件在 :file:`/usr/share/portage/config/make.globals` ，而 :file:`make.conf` 下的配置会覆盖该模板下对应变量，现在只需设置如下几个变量：

.. code-block:: shell

  # 这是一组推荐的设置
  # '#' 后内容代表注释

  COMMON_FLAGS="-march=native -O2 -pipe"
  # 这不是一个 portage 可以识别的变量，只是方便给其它变量赋值
  # 说明：
  #   -march=native, -march 用于指定编译目标架构
  #                  native 用于自动识别当前的 CPU 架构，它并不是一个最终参数，但方便可用
  #             -O2,     -O 用于指定编译优化等级，
  #                       2 是当前推荐的优化等级，它隐性地开启了一系列 flags
  #                         具体参阅： https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html#Optimize-Options
  #                         　　以及： https://wiki.gentoo.org/wiki/GCC_optimization#-O
  #                         　　以及： https://stackoverflow.com/questions/15548023/clang-optimization-levels
  #           -pipe, 这个标记对代码本身不会产生影响，它能加速编译过程但会消耗更多的内存
  #                  内存充足情况下建议使用，否则去掉该标记

  CFLAGS="${COMMON_FLAGS}"   # 传递给 C 编译器的变量，这里将上面统一设置的值给了 CFLAGS，下同
  CXXFLAGS="${COMMON_FLAGS}" # 传递给 C++ 编译器的变量
  FCFLAGS="${COMMON_FLAGS}"  # 传递给现代化编译系统下的 FORTRAN 编译器的变量
  FFLAGS="${COMMON_FLAGS}"   # 传递给 FORTRAN 77 编译器的变量
  # 可以根据实际需要添加/修改，并传递给编译器

  #MAKEOPTS="-j16"
  # 这是用来告知编译器同时执行任务数的变量（这里演示设置了 16 个并行任务数）
  # 通常设置为总线程数（会在编译一些大任务时占满 CPU 时间）
  # 当 CPU 线程够多（>=24）的时候，推荐可以小于总线程 1-2 个任务
  # 当 CPU 线程够多，但内存不足时，推荐设置为更小值
  # 　     　　　　　　　　　　　　Gentoo Wiki 推荐取「内存大小/2G」与「CPU 线程数」中的较小者
  # 　     　　　　　　　　　　　　但就我个人使用情况经验来说，要看 CPU 线程数多少，
  # 　     　　　　　　　　　　　　　　　　　　　　　　　　　　大于 10 线程我就建议替换上述比较为：
  # 　     　　　　　　　　　　　　　　　　　　　　　　　　　　「内存大小/1G」与「CPU 线程数」中的较小者，
  # 　     　　　　　　　　　　　　　　　　　　　　　　　　　　然后再根据日常使用情况进行调整。
  # 请自行配置后删除注释符
  # 如果变量未进行设置
  # 那么 portage 会根据当前 CPU 的线程数自动赋予一个值
  # 该自动值等于当前 CPU 线程数

其它当前存在的内容默认即可 无需更改。随着后续的使用，会有更多的内容写入这个配置文件。

.. _`why-not-accept_keywords-tildeamd64-as-default`:

.. _`在上文我有写到`:

.. note::

  **为什么我不建议开启全局的** :file:`~amd64` **关键字**

  有的教程可能会推荐添加配置： :file:`ACCEPT_KEYWORDS="~amd64"` 以默认在全局范围下安装更新的软件版本。

  先解释 :file:`~amd64` 此关键字的含义，它不一定是表示所对应软件的对应版本一定处在测试期，但它一定表示在当前的 Gentoo Linux 系统下，此版本的该软件一定处在测试期。这个测试的含义可能是软件本身还不够稳定，也有可能是与 Gentoo Linux 的兼容性还有待进一步验证。

  设置此配置的利弊：

  利
    你可以拥有整个 Portage 系统下几乎最新的软件版本，意味着你可以提前享受到各种新版本软件所带来的新功能。

  弊
    可同时的，它会引入一些潜在的依赖冲突（这个还挺容易遇到的），更频繁的更新（有时候一个软件的修订版会在一天内出好多次），其它相对稳定版更多的潜在问题。

  如果你愿意花时间去解决上述的弊端，那么当然，完全可以开启。

  可就我个人建议来说，完全可以省下这个时间，并同时尽可能满足上述的利端，只要针对自己明确需要的软件，单独开启 :file:`~amd64` 关键字即可（如何操作下文 `关键字`_ 一节会有介绍），这样既尽可能地保证了系统的稳定性，又最大化满足了自己的需要，还节省时间。

  *（顺便说一句，在 Gentoo Linux 下，即使是稳定版的软件，大部分跟随上游同步还是非常及时的）*

数据库
~~~~~~~~~~

默认情况下， Portage 自带一个官方的数据库同步配置，位于 :file:`/usr/share/portage/config/repos.conf` ，会以 rsync 方式从官方服务器同步数据（手动）。

而还有一种同步方式—— git，两者的优劣区别很小：

* rsync 方式可以使用命令校验本地改动，但本地同步时速度较慢；镜像站同步上游频率正常
* git 方式可以使用命令结合人工介入判断以校验本地改动，本地同步时速度快；官方镜像点与原始仓库同步最及时，但国内镜像站同步上游频率低

无论选择哪种同步方式，均可（目前我推荐使用 git 方式）。为了使得更新更迅速，建议自定义一个靠近自己的镜像站点。方法为，

先创建一个自定义配置文件 :file:`/etc/portage/repos.conf/gentoo.conf` ，后根据同步类型进行操作，

自定义 rsync 方式同步配置
  将如下内容写入上述文件中：

  .. code-block:: ini

    [gentoo]
    location   = /var/db/repos/gentoo
    auto-sync  = yes
    sync-type  = rsync
    sync-uri   = rsync://mirrors.bfsu.edu.cn/gentoo-portage
    # 国内我这里建议可以使用北外的镜像站，其负载小，带宽大，更新迅速。
    # 其它国内的镜像站我所知的还有：
    #   TUNA： rsync://mirrors.tuna.tsinghua.edu.cn/gentoo-portage
    #    163： rsync://mirrors.163.com/gentoo-portage
    #  中科大： rsync://rsync.mirrors.ustc.edu.cn/gentoo-portage/

自定义 git 方式同步配置
  将如下内容写入上述文件中：

  .. code-block:: ini

    [gentoo]
    location   = /var/db/repos/gentoo
    auto-sync  = yes
    sync-type  = git
    sync-depth = 1
    sync-uri   = https://mirrors.bfsu.edu.cn/git/gentoo-portage.git
    # 国内我找到的 git 方式同步镜像只有北外和 TUNA 两家
    #   TUNA 的地址： https://mirrors.tuna.tsinghua.edu.cn/git/gentoo-portage.git
    # 但它们的同步上游的频率都很低（截至发文时确认为 11 小时一次）
    # 所以若使用 git 方式同步，在网络流畅的情况，个人更建议直接同步官方镜像：
    #   https://github.com/gentoo-mirror/gentoo.git
    sync-git-verify-commit-signature = yes
    # 设置校验最上层 commit 的签名，默认是不校验的

  之后执行，

  .. code-block:: shell

    emerge -vj dev-vcs/git
    # 以安装 git 工具，它并不是系统自带的

    rm -rf /var/db/repos/gentoo
    # 删除原有的不支持 git 方式的数据库

    emerge --sync
    # 初始化同步一次数据库

之后，无论 rsync 方式还是 git 方式都可以很顺畅地使用 :code:`emerge --sync` 命令来对数据库进行日常同步，Gentoo Linux 官方有一份较为完整的 `rsync 镜像列表`_ 。

.. note::

  如果你比较疑惑为何在安装时添加了一个镜像地址，此时又添加了，那么在此说明：

  安装 Gentoo Linux 时往 :file:`/etc/portage/make.conf` 写入的镜像地址，是 distfiles 镜像地址，用于下载安装软件时的软件本体（源代码或者二进制包），也包括了很多其它内容，比如 Portage 数据库的快照（但此快照不适用于日常更新）。

  而此时配置的镜像是用于同步 Portage 系统的数据库，其包含了基础的系统配置文件，安装软件所需的描述文件等等很多基础内容。

设置桌面环境
-----------------------------

Gentoo Linux 既可以作为服务器，也可以作为个人电脑来使用。

如果作为服务器，那么至此基本配置已经全部完成，后续自行根据需要安装/配置服务即可，后文会继续说明如何使用 Gentoo Linux 的包管理系统等。

而作为个人电脑，则还需安装配置额外的软件，可以是 :ruby:`桌面环境|Desktop Environment` ，也可以是 :ruby:`窗口管理器|Window Manager` （其它极少数情景不在本文讨论范围内）。

桌面环境与窗口管理器的主要区别：它俩是包含与被包含的关系，桌面环境更庞大复杂，集成的功能全面（基本你需要的都有了），开箱即用，其包含了窗口管理器；而窗口管理器，顾名思义，纯粹用于管理窗口的，一个纯窗口管理器是连基本的任务栏、托盘等基础组件都不包括的（不过现在很多都包括了），需要额外的配置后使用，它的优势在于轻量（相对于桌面环境而言，特别轻量）、简洁、更方便定制。

如今主流的 `桌面环境`_ 有很多，这里我会介绍我熟悉的 KDE Plasma，它使用 QT 实现。主流的 `窗口管理器`_ 也很多，这里我会介绍我熟悉的 Awesome WM。

X? Wayland?
+++++++++++++++

无论选择安装哪种环境，都需要显示服务器作为依托。而现今 Linux 下主流的显示服务器有两种， X Window System 以及 Wayland。其中 X Window System 是最早开发的也是现如今稳定使用的；而 Wayland 则是未来。

简单比较：

X Window System
  当前基本所有的图形化软件都是针对其开发的，扩展性强，兼容性好；但各窗口间无隔离，安全性较差。

Wayland
  它是一个协议，实现该协议的显示服务器（也叫 Wayland 混成）有多种，目前大部分软件对 Wayland 的支持都不够成熟或者不支持；但它性能比 X 更好，窗口有隔离安全性更好，各软件也都在忙着兼容它。

就当下（2021 年，十月）的情况来看，依旧是选择 X 更合适，在不久的将来则是 Wayland 会对 X 实现完全替代。现在着重说配置 X 环境，后续等 Wayland 更成熟后再更新。

显卡驱动
+++++++++++++++

在之前安装 Gentoo Linux 的过程中，二进制内核本身已自带了大多数显卡的内核驱动部分，该部分负责接收用户空间发送的指令及数据，进行处理后传递给显卡。

.. note::

  如若你的显卡是较新的 N 卡，开源驱动还未支持，请参阅官方的 `NVIDIA/nvidia-drivers`_ 一文以安装闭源驱动。

.. _`显卡的配置`:

对于 X 而言，它还需要配置对应的 2D 驱动，这里以现代化的 A 卡为例，编辑 :file:`/etc/portage/make.conf` 文件，添加以下内容：

.. code-block:: shell

  VIDEO_CARDS="amdgpu radeonsi"
  # 其中，
  # 　　amdgpu radeonsi 用于给 X 开启 2D 驱动（X 下必须）
  # 　　radeonsi 用于给 OpenGL 的实现 mesa 开启对内核下 amdgpu 驱动的支持（无论 X 还是 Wayland 均需配置）
  # 如果 A 卡比较老，则额外添加 radeon 值，详细查阅： https://wiki.gentoo.org/wiki/AMDGPU
  # Intel 的一般设为 intel i965 iris， 详细查阅： https://wiki.gentoo.org/wiki/Intel
  # N 卡开源驱动一般设为 nouveau， 详细查阅： https://wiki.gentoo.org/wiki/Nouveau
  # 虚拟机下的驱动设置得具体看，比如现在的 VirtualBox 和 VMWare 都用 vmware 驱动，
  # 　　　　　　　　　　　　　　那么就设置值为 vmware
  # 　　　　　　　　　　　　　　再比如 QEMU 可选使用 virgl 驱动，那么就设置为 virgl
  # 　　　　　　　　　　　　　　等等，请自行查阅相关资料

在这里，还需将之前配置的普通用户添加到 :file:`video` 组下以使用硬件加速功能。执行

.. code-block:: shell

  groupmod -a video -U 「用户名」


切换 Profile
+++++++++++++++

在安装心仪的 DE/WM 之前，建议切换到的 :file:`desktop` profile 下，执行

.. code-block:: shell

  eselect profile list
  # 以列出所有的 profiles
  # 然后进行选择
  # 例如：
  # 　　　openrc 下，可以选择 amd64/17.1/desktop
  # 　　　       　　　　　　 amd64/17.1/desktop/gnome
  # 　　　       　　　　　　 amd64/17.1/desktop/plasma
  # 　　　       　　　　　　 等
  # 　　　systemd 下，可以选择 amd64/17.1/desktop/systemd
  # 　　　        　　　　　　 amd64/17.1/desktop/gnome/systemd
  # 　　　        　　　　　　 amd64/17.1/desktop/plasma/systemd
  # 　　　        　　　　　　 等

  # 如若只想安装轻量级的窗口管理器，那么可以选择类似 amd64/17.1/desktop 一样的纯 desktop profile
  #eselect profile set 5

  # 根据本文上下文环境，这里我选择 amd64/17.1/desktop/plasma 以准备好 KDE Plasma 的前期环境
  eselect profile set 8

.. warning::

  这里不要跨初始化环境选择 Profile ，systemd 与 openrc 的 Profile 切换不会很轻松。

且，虽然 :file:`desktop` profile 下已经配置启动了基本的 ALSA 声音接口功能，但个人建议再启用 PulseAudio 声音服务器以获得更多功能。只需编辑 :file:`/etc/portage/make.conf` 文件，设置

.. code-block:: shell

  USE="pulseaudio"

.. note::

  切换到 :file:`desktop` profile 并不是一个必须的操作，也可以在基础的 profile 或者其它的 profile 下进行，但如果这样的话，则需要再自行额外配置，会相对复杂一点，此处不多做说明。

安装 DE/WM
+++++++++++++++

此处以安装 KDE Plasma 为例，

.. tip::

  在进行安装完整的 KDE Plasma 之前，可以选择是否安装二进制包而不是自己从源码开始编译。

  关于 KDE Plasma 二进制包的提供是目前 Gentoo 的一种实验性质的方案，它的存在能显著缩短整体安装时间，降低机器负载，但目前对二进制包是不存在文件校验的，所以使用它有些许潜在风险。同时，使用二进制包表示将不会对本机有编译优化。（其它的也有可能导致一些需要编译的包出现编译问题）

  另外，如果本地一些包的 `USE 标记`_ 有变动或者一些包的依赖有了变动，那么对于该包， Portage 目前默认会回退到自行编译安装的状态（也推荐这样），在尽可能安装二进制包的同时，也完全不影响正常的使用。

  如果你决定启用这个尚处于实验状态的方案，那么需创建一个文件 :file:`/etc/portage/binrepos.conf` ，并添加以下内容：

  .. code-block:: shell

    [binhost]
    priority = 9999
    sync-uri = https://mirrors.bfsu.edu.cn/gentoo/experimental/amd64/binpkg/default/linux/17.1/x86-64/
    # 这里可以配置成任意所选镜像地址

  再编辑 :file:`/etc/portage/make.conf` 文件，设置：

  .. code-block:: shell

    EMERGE_DEFAULT_OPTS="--binpkg-changed-deps=y --binpkg-respect-use=y --getbinpkg=y"

  即可。

  *无论是否配置二进制包安装，都不影响下续步骤*

先更新一下当前的 Portage 数据库，使其为最新，执行

.. code-block:: shell

  emerge --sync
  # 如果你使用的是 rsync 同步方式，那么同步开始时可能会卡在
  #   Refershing keys from WKD ...
  # 发生这种情况是网络不通畅导致的，请等待， Portage 需要先更新它的校验公钥

在准备完上述的准备工作后，执行以下命令，开始安装过程：

.. code-block:: shell

  # 执行此命令将 plasma-meta 这个元包添加到 world set 中，关于 world set 后文使用 Portage 一节有指引
  emerge -Ow kde-plasma/plasma-meta

  # 处理下桌面环境下的依赖关系
  echo "media-libs/freetype harfbuzz" >>/etc/portage/package.use/desktop
  # （随着时间的推移，可能后续会有其它依赖关系问题，若出现，访问本文开头群组寻求帮助）

  # 先安装一个 rust-bin 以避免待会儿依赖安装需要编译的 rust
  # （因为完整编译 rust 会很久，除明确需要外没太大必要）
  emerge -vj1 dev-lang/rust-bin

  # 再整体更新一下整个系统
  emerge -ajvuDN --keep-going @world
  # 等待依赖计算完成后按回车以开始更新

此过程会比较漫长，由具体机器的性能而定。万一更新过程中失败，有可能为

1. 偶然问题，尝试对出问题软件包单独安装，使用命令 :code:`emerge -vj1 <包名>` 进行；成功后再次运行上述更新命令
2. 因为内存太低导致的，尝试去除上述命令选项中的 :code:`j` 重新更新
3. 其它问题，请查看提醒的相应编译日志，如不能解决，可加文章开头群组寻求帮助

.. note::

  如果你打算安装 WM，那么以 Awesome Window Manager 为例，profile 可以选择纯 :file:`desktop` profile 以获得最基础的桌面配置，然后安装 :gepkg:`x11-wm/awesome` 即可。

  安装完毕后，建议安装 :gepkg:`x11-misc/sddm` 这个 Display Manager 用于启动 Awesome WM，至于之前的 KDE Plasma，它已经默认依赖了 sddm。

  相对于 KDE Plasma， Awesome WM 的依赖要少太多太多，安装快速，但功能也极简单。

  顺便说一下 Display Manager (DM)，它用于提供图形化的登陆界面以登陆到 DE 或者 WM，它有多种，比如 KDE 默认的 sddm， Gnome 默认的 GDM，等等。

.. warning::

  上述的操作会自动依赖上 X server: :gepkg:`x11-base/xorg-server` ，其依赖路径是::

    plasma-meta -> sddm -> xorg-server

  所以无需单独安装；

  如果安装的是其它未硬性依赖 X server 的 DM/DE/WM，那么还需要手动安装上 X server，否则 X 软件无法运行。

  *Wayland 不在此警告考虑范围内*

上述安装完毕后，可选安装 KDE Plasma 的应用元包，执行

.. code-block:: shell

  # 这是一个可选命令，它会引入 KDE 应用
  # 个人建议没必要使用默认设置来安装 kde-apps/kde-apps-meta 包，
  # 因为会引入太多不常用的应用
  # 建议根据 USE 来管理（下文 USE 标记一节有说明），选择性安装，即
  echo 'kde-apps/kde-apps-meta -*' >/etc/portage/package.use/kdeapps
  # 同时取消 kdecore-meta 的 webengine 依赖，以减少当下的编译时间
  echo 'kde-apps/kdecore-meta -webengine' >>/etc/portage/package.use/kdeapps
  # 以安装最核心的 KDE 应用
  emerge -vj kde-apps/kde-apps-meta
  # 其它 KDE 应用根据需要安装即可

.. note::

  建议至少安装一个终端模拟器（上述应用元包已包含 konsole），否则进入了桌面后无法使用终端，只能按下 :kbd:`Alt` + :kbd:`Ctrl` + ( :kbd:`F1` 至 :kbd:`F6` ) 切换到 TTY 下使用 shell 环境（回到桌面环境一般为 :kbd:`Alt` + :kbd:`F7` ）。

配置 DM 启动
+++++++++++++++

到此时，用于启动桌面环境的必要组件都安装完毕了，接下来需要配置 DM 的开机启动，并启动它

openrc 下
  先编辑 :file:`/etc/conf.d/display-manager` ，设置

  .. code-block:: shell

    DISPLAYMANAGER="sddm"
    # 这样就设置了 sddm 作为默认的 DM，如果你安装了别的 DM，那么根据提示做对应设置

  然后执行

  .. code-block:: shell

    rc-update add display-manager default
    # 设置其默认开机启动

    rc-update add dbus default
    # openrc 下请也同时设置 dbus 的开机启动
    # 若不设置，虽然 display-manager 也会启动它，但有时候会出现奇怪的问题，原因我还未查明

    # 以下步骤等待下次重启后会自动执行
    rc-service dbus start
    # 先启动 dbus
    rc-service display-manager start
    # 再启动 DM

systemd 下
  则直接执行

  .. code-block:: shell

    systemctl --now enable sddm.service
    # 以启用，如果是其它的 DM 也是启用对应的服务即可。

之后，确保 DM 界面选定了 Plasma (X11) 这个 Session，再选择对应的普通用户，输入密码后登陆。

动画过渡后，就进入了人性化的桌面环境。

必要的桌面应用
+++++++++++++++

以下操作需要在桌面的终端或者 TTY 下，以 root 权限进行。

如果是在桌面终端的话，打开终端后，执行 :code:`su -` 或其它等同命令进入 root 用户下；如果之前安装并配置了 :file:`app-admin/sudo` 工具，那么也可以以普通用户在下述的每一条命令前添加上 :code:`sudo「空格」` 后执行。

中文字体
~~~~~~~~~~

在应用之前，最好先安装好中文字体，官方仓库提供有中文字体的包有

* media-fonts/arphicfonts
* media-fonts/noto-cjk
* media-fonts/source-han-sans
* media-fonts/wqy-microhei
* 等

自行选择安装即可，比如，

.. code-block:: shell

  emerge -vj media-fonts/noto-cjk

也可以将其它的字体文件复制到目录 :file:`~/.local/share/fonts/` 下，然后执行 :code:`fc-cache` 创建字体缓存。

输入法
~~~~~~~~~~

作为中文用户，肯定需要款输入法，我推荐使用 fcitx （还有一款叫 ibus ，但是我不熟，就不介绍了）。目前稳定维护的 fcitx 版本是 5 ，但是官方仓库 :file:`::gentoo` 目前只有 4 （也能用，就是不怎么维护了）。

所以这里有两个选择：

1. 使用官方提供的 fcitx4 ，执行

   .. code-block:: shell

     # 先配置下 fcitx4 开启对 gtk2 的支持以避免有些程序无法使用（gtk3 默认开启了）
     echo 'app-i18n/fcitx gtk2' >>/etc/portage/package.use/fcitx

     # 然后安装
     emerge -vj app-i18n/fcitx:4 app-i18n/fcitx-configtool:4 app-i18n/fcitx-qt5:4 app-i18n/fcitx-libpinyin:4
     # 其中， app-i18n/fcitx 是 fcitx 的主程序
     # 　　　 app-i18n/fcitx-configtool 是它的配置工具
     # 　　　 app-i18n/fcitx-qt5 用于支持在 qt 程序上使用它
     # 　　　 app-i18n/fcitx-libpinyin 是一个输入法

2. 使用更新的 fcitx5 。因为官方仓库目前没有，所以这里需要使用额外的仓库。

   据我所知目前提供 fcitx5 的 Gentoo 仓库有 `::gentoo-zh`_ 以及我自己的 `个人仓库`_ 。

   具体方法为：

   .. code-block:: shell

     # 添加额外的仓库
     # 先安装必要的工具
     emerge -vj app-eselect/eselect-repository

     # 然后启用仓库
     # 启用过程中，可能会因为网络原因导致比较慢，请耐心等待
     eselect repository enable ryans
     # 这里启用了我的个人仓库

     # 更新以获取下仓库内容
     emerge --sync ryans
     # 如果一直卡在这里，那说明当前网络访问 github.com 不流畅
     # 　　　　　　　　　这时候有一种方法是：
     # 　　　　　　　　　　　　访问 https://fastgit.org （我不对该网站做任何保证）
     # 　　　　　　　　　　　　修改 /etc/portage/repos.conf/eselect-repo.conf 文件，
     # 　　　　　　　　　　　　替换对应链接的域名为上述网站内指定值
     # 　　　　　　　　　　　　并再次同步

     # 添加关键字用于安装
     echo "app-i18n/*::ryans" >>/etc/portage/package.accept_keywords
     echo "x11-libs/xcb-imdkit::ryans" >>/etc/portage/package.accept_keywords

     # 之后安装
     emerge -vj app-i18n/fcitx-meta:5
     # 这里安装了 fcitx 的元包，它会自动依赖安装 fcitx5 主体、 RIME 输入法、配置工具等
     # 我的仓库未提供 fcitx5-chinese-addons 这个包，如有需要，使用 ::gentoo-zh 的仓库，见下

     # 如果你选择 ::gentoo-zh 这个仓库的话，因为包名和依赖不同，所以安装命令为（自行删除命令前注释符）
     # 先安装必要的工具
     #emerge -vj app-eselect/eselect-repository
     # 然后启用仓库
     #eselect repository enable gentoo-zh
     # 之后获取仓库（如若卡同步，见上）
     #emerge --sync gentoo-zh
     # 添加关键字用于安装
     #echo "app-i18n/*::gentoo-zh" >>/etc/portage/package.accept_keywords
     #echo "x11-libs/xcb-imdkit::gentoo-zh" >>/etc/portage/package.accept_keywords
     # 再安装
     #emerge -vj app-i18n/fcitx5-meta
     # 这个仓库的会默认安装上 fcitx5-chinese-addons ，里面包含有中文输入法

   .. warning::

     当使用非官方的 Fcitx5 时，因为没有镜像收录，所以源码需从 Github 下载，这时可能遇到因网络问题导致无法下载的情况（可以从 :file:`/var/log/emerge-fetch.log` 文件查看源码包下载情况），如果遇到这种情况那么请自行通过各种途径下载好对应的 :file:`.tar.gz` 格式（或类似）软件包，然后移动到 :file:`/var/cache/distfiles/` 目录下。

     软件包需更名为对应的包名加完整的版本号（执行上述 :code:`emerge -vj <包名>` 命令后可以看到完整的版本号），比如当显示的包名为 :file:`app-i18n/fcitx-gtk-5.0.8:5::ryans` 那么就更名下载的源码包为 :file:`fcitx-gtk-5.0.8.tar.gz` （ :file:`/` 符号后以及 :file:`:` 符号前的内容），以此类推。

无论选择哪个版本、哪个仓库，安装完成后，均执行此配置，这里另开一个终端，以普通用户编辑 :file:`~/.xsession` 文件（这里为普通用户的家目录下，不存在则创建一个），然后添加以下内容：

.. code-block:: shell

  export XMODIFIERS="@im=fcitx"
  export QT_IM_MODULE=fcitx
  export GTK_IM_MODULE=fcitx
  export SDL_IM_MODULE=fcitx

之后，登出 KDE Plasma，后重新登陆，此时只需做最后的配置，以安装的为 :file:`fcitx-rime:5` 为例，

1. 右击托盘区输入法图标，选择 :file:`Configure`
2. 点击右下角 :file:`Add Input Method`
3. search 框下输入 :code:`rime`
4. 选中 Rime 后点击右下角的 :file:`Add`
5. :file:`Apply` 后退出界面
6. 右击托盘区输入法图标，选择 :file:`Restart`

之后， Rime 会进入一个部署状态，等待片刻后即可使用。默认情况下， Rime 输出的为繁体中文，常规有两个方法切换成简体，

* 临时选择简体，按下 :kbd:`Ctrl` + :kbd:`\`` 后在弹出的选框中选择。
* 永久修改，这里区分 fcitx 的版本，版本 4 对应目录 :file:`~/.config/fcitx/rime/` ；而版本 5 对应目录 :file:`~/.local/share/fcitx5/rime/` ，在对应目录下（这里的 :file:`~` 依旧是普通用户的家目录）创建文件 :file:`luna_pinyin.custom.yaml` 并添加以下内容：

.. code-block:: yaml

  # 注意缩进
  patch:
    switches:
      - name: ascii_mode
        reset: 0
        states: [ 中文, 西文 ]
      - name: full_shape
        states: [ 半角, 全角 ]
      - name: simplification
        reset: 1
        states: [ 漢字, 汉字 ]

后重启 fcitx 即可（详情见 `Rime 的 CustomizationGuide`_ ）。

浏览器
~~~~~~~~~~

关于浏览器的选择，有很多，比如

* www-client/google-chrome （chrome 的官方二进制包）
* www-client/google-chrome-beta （chrome 的官方二进制包， beta 分支）
* www-client/chromium （chromium 源码包，需编译，时间很久很久）
* www-client/firefox-bin （火狐官方二进制包，国际版）
* www-client/firefox （火狐源码包，需编译，时间很久）
* www-client/microsoft-edge-beta （Edge 官方二进制包， beta 分支）
* 等

可以自行选择安装。命令依旧是 :code:`emerge -vj <包名>` 。安装个别浏览器时，可能会因为许可问题导致无法安装，如何解决看下文的 `软件的许可`_ 一节。

其它的应用自行发掘。这里有推荐应用列表：

* https://wiki.gentoo.org/wiki/Recommended_applications
* https://wiki.archlinux.org/title/List_of_applications

至此，桌面配置告一段落。

.. note::

  未重启系统之前，有可能会出现 KDE Plasma 下看不到重启/关机等操作、声音无法使用的情况，重启系统后一般就正常了。

使用 Portage
-----------------------------

Portage 是 Gentoo Linux 的包管理系统，本文自开始至此，大部分时候都在围绕 Portage 操作，本段详细说明一下它的日常使用。

几个基础概念

* ebuild 可以指文件，此文件是组成软件包的最小部分，定义了软件包如何安装，依赖关系等，存放在 portage 数据库路径下
* ebuild 也可以指一个命令，该命令用于测试 ebuild 文件
* emerge 是 portage 系统的主命令，它负责 portage 系统的几乎所有功能
* distfile 是 portage 下载的软件包原始文件，它可能是源码包，也可能是二进制包，因软件包而异
* 集（sets）是 Portage 用于管理软件包的一种方式，用户安装的软件一般会添加到 world 集中，详见 `Package sets`_
* Portage 拥有一个名为 gentoo 的主仓库，同时也能添加额外的仓库以作补充，额外的仓库优先级默认高于主仓库，详见 `ebuild repository`_

几个基础命令

* :code:`emerge --info` 用于查询 Portage 的信息
* :code:`emerge --sync` 用于更新数据库
* :code:`emerge -s <包名>` 用于查询软件包
* :code:`emerge <包名>` 用于安装软件包
* :code:`emerge -r` 用于恢复上一次失败的 emerge
* :code:`emerge -ac` 自动清理系统下的软件包
* :code:`emerge -vpc <包名>` 用于查询当前所有对该包的依赖
* :code:`emerge -avuDN @world` 用于更新系统，这个是日常更新的基础命令，常见的组合为：

  .. code-block:: shell

    # 先更新数据库
    emerge --sync
    # 再更新系统
    emerge -avuDN @world
    # 更新完毕后清理系统
    emerge -ac

* :code:`emerge -C <包名>` 用于卸载软件包，但是注意，这个命令可能会破坏掉系统的依赖关系，所以更合理的卸载方式为：

  .. code-block:: shell

    # 先删除软件包的 world 集记录
    emerge --deselect <包名>
    # 再清理系统
    emerge -ac

emerge 常用选项
+++++++++++++++++++

先解释上述基础命令中的选项，其中

* :file:`-C, -c, --deselect, --info, -r, -s, --sync` 都是执行的对应操作，不属于选项
* :file:`-D` 表示检查包的整个依赖树
* :file:`-N` 表示检查 USE 的任何改动
* :file:`-a` 代表询问以确认执行该操作
* :file:`-u` 表示升级，略过不升级的包
* :file:`-v` 表示显示详细信息

其它常用的选项有

* :file:`-1/--oneshot` 一般用在安装软件包时，不将该包添加到 world 集中
* :file:`-O/--nodeps` 不计算依赖关系，只操作指定的包（安装时可能会因为依赖不满足而导致安装失败）
* :file:`-f/--fetchonly` 仅下载指定包及其依赖的 distfiles 而不进行安装
* :file:`-j/--jobs` 设置 Portage 同时执行的最大任务数，如果未设置数量，那么 Portage 不会限制最大的任务数
* :file:`--keep-going` 它会在安装出错时，跳过安装失败的包，并重新计算依赖后继续安装剩余包
* :file:`-n/--noreplace` 不重复安装已经安装的包（默认会忽略掉 USE 的改动以及升级的查询，除非对应加上 :file:`-D/-U` 和 :file:`-u` 选项）
* :file:`-p/--pretend` 假装进行该操作（实际不进行），一般只计算依赖关系，也可用于非特权用户查询信息用
* :file:`-t/--tree` 显示给定包的安装依赖树

.. _`USE 标记`:

USE 标记
+++++++++++++++++++

USE 标记是 Portage 系统的一个核心功能，很多包都会有可选的 USE 标记，正如上文有地方会写入到 :file:`package.use` 文件夹下的内容。Portage 使用它来管理每个包的功能，是一个很重要的特性。

在日常使用过程中，也会发现包与包之间关于对 USE 标记的依赖问题，比如当一个包 A 依赖另一个包 B 的 USE 非默认时，会出现无法安装的问题，此时需要对 B 包配置其 USE 标记。

USE 的配置可以分为全局的和局部的：

全局配置
  自定义的全局配置可以编辑 :file:`/etc/portage/make.conf` 文件下的 USE 变量，这个变量是一个增量型的，它会与默认的 :file:`/usr/share/portage/config/make.globals` 文件下的 USE 配置，以及选定的 profile 下的 USE 配置组合，可以使用如下命令查看当前应用的全局 USE 标记：

  .. code-block:: shell

    emerge --info | grep '^USE'

  全局的 USE 会应用给当前系统下支持该 USE 的所有包，谨慎配置。

局部配置
  自定义的局部配置则编辑 :file:`/etc/portage/package.use` 文件，如果这个路径是一个文件夹，那么编辑该文件夹下的任意文件即可，一般建议使用文件夹来进行管理。

  其配置格式为

  .. code-block:: shell

    # 注释
    <类>/<名> <USE>

    # 亦可指定版本，比如对 21.04.3 及以上版本的 kde-apps-meta 进行配置
    >=kde-apps/kde-apps-meta-21.04.3 -* admin
    # USE 标记前加 - 代表去掉这个 USE，
    # 上述 -* 代表去除该匹配的包的所有已经添加的以及默认的 USE
    # 然后再启用 admin 这个 USE 标记

Portage 有一个 USE Expand 功能，即把指定变量的值扩展成 USE，这些指定的变量被设置在 Portage 数据库路径下的 :file:`profiles/base/make.defaults` 文件的 USE_EXPAND 变量中。这个功能很实用，简化了配置值，还能进行归类，更便于管理。上文有一个 `显卡的配置`_ 其实就是一个 USE_EXPAND 值。其它会使用到它的地方不多，但也有，比如：

.. code-block:: shell

  # 配置全局的本地化配置，就可以在 make.conf 文件下配置
  L10N="zh-CN zh-TW zh en-GB-oxendict en"
  # 这样，那么以后当有包支持上述的本地化配置时，就会自动添加

  # 其它比如可以对 qemu 这个虚拟机添加额外的模拟平台，
  # 可以往 /etc/portage/package.use/qemu 文件写
  # app-emulation/qemu QEMU_SOFTMMU_TARGETS: aarch x86_64
  # 以支持 arm64 及 x86_64 平台。等等

.. _`关键字`:

关键字
+++++++++++++++++++

*ACCEPT_KEYWORDS* 这个是一个针对 CPU 架构及软件的稳定/测试分支的变量。 `在上文我有写到`_ 为何不建议全局 :file:`~amd64` 关键字，这里详细说明这个变量。

Portage 会默认启用针对当前 CPU 架构的关键字，即： AMD64(x86_64) 架构，默认启用 :file:`amd64` 关键字； ARM64(AArch64) 默认启用 :file:`arm64` 关键字，以此类推。

这个关键字是用于判断软件包稳定性的，软件的维护者会在维护软件（维护 ebuild）时，对该软件设定好对应架构的稳定程度，当该软件设定好的关键字在系统下未被接受时，该软件将无法被安装。

上述默认启用的关键字是一个稳定关键字，这里以 :file:`arch` 来表示，而还有一个测试关键字 :file:`~arch` ，即在稳定关键字前加一个 :code:`~` 符号。

默认情况下，系统都会接受当前架构的稳定关键字，你可以根据需要添加或者删除所需的关键字。

.. note::

  对于非官方的的 Portage 仓库，软件包一般都采用测试关键字，这算是对主仓库包的一种保护措施。

自定义 *ACCEPT_KEYWORDS* 变量同样分为全局和局部，全局配置依旧在 :file:`/etc/portage/make.conf` 文件内。

可以按包进行局部配置则是在 :file:`/etc/portage/package.accept_keywords` 文件，它和 :file:`package.use` 一样，如果路径为文件夹，那么将配置写入该文件夹下的任意文件内即可。格式如下：

.. code-block:: shell

  # 注释
  <类>/<名> [可选的关键字配置]
  # 当只指定了包，却未添加任何关键字时
  # 　　　　　　　默认添加当前架构的测试关键字：~arch，
  # 　　　　　　　比如 amd64 平台则默认添加 ~amd64
  # 这里存在一种情况，当软件未设置任何关键字时，
  # 　　　　　　　　　这种情况一般出现在实时（live）包上
  # 　　　　　　　　　那么为了安装此包，需为其设置标记 **
  # 　　　　　　　　　代表忽略关键字检查
  # 　　　　　　比如欲安装实时的 app-editors/vim 包，则配置
  # 　　　　　　　　　app-editors/vim **

  # 亦可指定版本，比如对 21.04.3 及以上版本的 kde-apps-meta 进行配置
  #>=kde-apps/kde-apps-meta-21.04.3

无论是全局配置还是局部配置，其都是一个增量值，如需去掉所有之前配置的关键字，同样使用 :code:`-` 符号。

.. _`软件的许可`:

软件的许可
+++++++++++++++++++

Portage 下的软件包很多，每个包所使用的许可也不尽相同。默认情况下，基础的 profile 配置已经接受了各种自由许可，使得安装自由软件不再需要额外的许可步骤。

而一些私有软件，所使用的许可默认是不接受的，于是安装他们的时候会出现无法安装的情况，这时候有两个方式来解决。

一是全局配置接受所有许可，这个方法一劳永逸，以后再也不会提示因为许可而导致的软件无法安装，方法是在 :file:`/etc/portage/make.conf` 文件内添加

::

  ACCEPT_LICENSE="*"

另一个则是当每次出现许可问题时，单独添加该软件的许可到 :file:`/etc/portage/package.license` 文件内，或者该文件夹下的任意文件内（许可名会在出现问题时提醒）。格式为

.. code-block:: shell

  # 注释
  <类>/<名> <许可名称>

  # 亦可指定版本，比如对 20210818 及以上版本的 sys-kernel/linux-firmware 进行配置
  #>=sys-kernel/linux-firmware-20210818 linux-fw-redistributable no-source-code

请根据自己的喜好，自行选择。

emerge 默认选项
+++++++++++++++++++

emerge 支持配置一组默认选项，用于在每次运行 emerge 时采用。这个储存默认选项的变量名为 :file:`EMERGE_DEFAULT_OPTS` ，在 :file:`make.conf` 文件下设置。

常见设置的默认选项有

:file:`-v/--verbose`
  显示详细信息

:file:`--keep-going`
  上文已交代

:file:`-j/--jobs`
  上文已交代，这里作补充。如果要将该选项添加到默认选项下，那么建议配合 :file:`-l/--load-average` 使用， :file:`-l/--load-average` 用于配置 emerge 的负载阈值，当当前负载到达设定值后， emerge 将不再开启新任务，以避免负载过高，这在 CPU 不够强悍或者内存不宽裕的机器上很需要。比如在一个 8 核 16 线程 16G 内存的机器上，可以设置成 :file:`-j -l 12` ，这样的设定使 portage 的并行任务数不由硬性规定的数目来限制，而是通过动态负载来进行限制。

:file:`--autounmask` 类
  这是一组在新装软件包时便于解除安装限制的选项。之前有介绍，在 Portage 安装软件的过程中，可能会因为 USE/License/Keywords 等因素导致无法直接安装，需要配置后再进行，而这组选项可以自动化这个过程。个人建议的相关选项组合为 :file:`--autounmask --autounmask-keep-masks --autounmask-write=n` ，此组合不会完全自动写入配置到系统下，但是提示了如何配置，方便手动写入，既简化了处理限制的流程，又能保证掌握每次安装包时的改动。

那么这里一组比较推荐的默认选项配置为

.. code-block:: shell

  EMERGE_DEFAULT_OPTS="--autounmask --autounmask-keep-masks --autounmask-write=n -j -l 12 --keep-going -v"
  # 其中的 12 请根据实际情况修改
  # 如果配置了上文的 binhost ，那么对应选项也添加进入

其它的选项请自行发现。

Portage 的内容太多，以上仅列出了几个经常会使用到的配置。更多内容，请通过执行 :code:`man portage` , :code:`man emerge` , :code:`man make.conf` 查询，或者访问 Gentoo Linux 官方维基。

关于配置文件的更新
+++++++++++++++++++

有时候在更新了某些软件包后你会发现出现了一个类似如下的提示信息：

::

  * IMPORTANT: 2 config files in '/etc' need updating.
  * See the CONFIGURATION FILES and CONFIGURATION FILES UPDATE TOOLS
  * sections of the emerge man page to learn how to update config files.

正如提示所说，完全可以自行查阅手册获取帮助，这里简单说明一下。

一般出现这种情况的直接原因是你通过归属于一个软件包的文件修改了其默认配置，导致新安装的文件与现存文件不符，于是 Portage 出于保护现存文件的目的，将新文件重命名为了对应目录下的 :file:`._cfgxxxx_<原名>` 文件，这是一个很常见的情况。

而每当出现这种情况后，需要做的操作就是人工介入，判断一下保留哪个文件，还是将两个文件合并。而自带用于进行此操作的对应命令有 :code:`dispatch-conf` 与 :code:`etc-update` 。

以 :code:`dispatch-conf` 为例，root 权限下执行后，它会逐个文件列出改动，然后提示你进行操作，比如按 :kbd:`z` 保留旧的配置文件，按 :kbd:`u` 使用新安装的配置文件替换旧的，等等。

常用工具
+++++++++++++++++++

单纯 Portage 自带的工具对于日常管理其会显得有些吃力，这里推荐几个比较有用的软件用于辅助管理 Portage。

:gepkg:`app-portage/eix`
  这个可以说是非常有用的软件，主要用于查询 Portage 数据库，其优势在于更快的速度、更人性化的显示格式以及更方便的查询模式。

  使用前需执行 :code:`eix-update` 以更新 eix 数据库，安装它之后，可以使用 :code:`eix-sync` 命令来更新 Portage 数据库，更新完毕后会自动更新 eix 数据库，并显示更新前后的软件包对比情况。

  使用 eix 查询所需软件，最基本的命令为

  .. code-block:: shell

    eix <包名匹配字符串>

    # 也可只查询已安装的包
    eix -I <包名匹配字符串>

    # 也可查询属于一个特定分类下的所有包
    eix -C <类名>

  等等，执行 :code:`man eix` 查看更多用法。

:gepkg:`app-portage/gentoolkit`
  包含了 Gentoo 的一些管理脚本，常用的命令有用于查询依赖关系，文件归属，软件包内容的 :code:`equery` ，以及用于清理 distfile 的 :code:`eclean-dist` 。比如

  .. code-block:: shell

    equery d vim-core
    # 可以查询依赖 vim-core 的软件包（仅根据 ebuild 文件内容查询）

    equery g vim
    # 可以查询 vim 下属的依赖关系图

    equery f vim
    # 可以查询 vim 安装了哪些文件到系统下

    equery b /usr/bin/vim
    # 可以查询这个文件属于哪个包

    eclean-dist -d
    # 可以清理未安装在系统下的 distfile 文件

  等等，请自行发现。

:gepkg:`app-portage/portage-utils`
  包含了 Portage 的帮助工具，与上面 gentoolkit 的功能有重合，他们具有互补性，常用的命令有用于分析 emerge 日志的 :code:`qlop` 。它是用 C 写的，速度更快。

:gepkg:`app-portage/pfl`
  Portage File List，可用于在线查询文件所归属的包，命令为 :code:`e-file <文件名>` 。

多版本管理
+++++++++++++++++++

Gentoo Linux 支持同一软件多版本同时存在于系统上，这归功于 Portage 系统的 slotting 机制。当你执行命令 :code:`eix dev-lang/python` 会发现它有好多行可用版本，最前圆括号内的内容即对应的 slot 名，不同 slot 下的版本可同时安装到系统上（ slot 名内 :file:`/` 符号后的内容表示其 sub-slot，同 slot 但不同 sub-slot 的版本无法共存）。比如，:file:`sys-devel/gcc` , :file:`sys-devel/clang` , :file:`dev-lang/lua` 等等都支持多版本共存。

对于一些多版本共存的工具， Gentoo Linux 准备了对应的 :code:`eselect` 命令以方便用户选择使用。其会在对应的 :file:`$PATH` 目录下创建一个指向当前选定版本命令的软链接。比如，

.. code-block:: shell

  eselect lua list
  # 列出当前所有已经安装的 lua 版本

  eselect lua set {序号}
  # 这样就设定了系统下用户交互环境的默认 lua 版本

其它的类似，执行 :code:`eselect help` 以查看当前所有支持的模块。不是所有的多版本共存的包都会有 eselect 模块，它们并不存在强制的依赖关系。执行 :code:`eix -I2` 可以显示当前系统下安装的可多版本共存的包。

Proxy
+++++++++++++++++++

并不是所有的 distfile 都能从镜像站下载，当遇到 distfile 下载不下来（或者 git 仓库克隆不下来）需要使用代理的时候，如何为 Portage 正确地配置 Proxy 呢。关于这个问题，我之前有一篇文章详细谈到了： https://bitbili.net/set-proxy-for-gentoo-portage.html

至此， Gentoo Linux 所特有的用法（除内核外）大致说明完毕。

关于内核
==================================================

自本文开始至此，我特意简略了所有关于内核的相关配置，原因是内核的配置非常复杂，需根据每台机器的环境而定，为了使读者可以在完全参照本文命令的情况下完整安装好 Gentoo Linux，我选择了预编译好的，适用范围最广的二进制内核。

而在这里，我会简述一些通用设定及操作。

可用内核版本
-----------------------------

Gentoo Linux 所提供的可用内核都在 :file:`sys-kernel` 类下，使用命令 :code:`eix -C sys-kernel` 即可列出。而其中以下三个版本更通用：

sys-kernel/gentoo-sources
  这是最高到内核主线版本的内核源码包，需要自行配置后，再自行编译后安装

sys-kernel/gentoo-kernel
  这是最高到内核主线版本的内核源码包，但同时包含了通用的内核配置，可自动编译后安装

sys-kernel/gentoo-kernel-bin
  这是最高到内核主线版本的内核二进制包，也是本文使用的内核，其使用的是最通用的内核配置

在 :file:`::gentoo` 这个官方仓库内，能被定为稳定的内核版本，目前只有 :ruby:`长期支持|Long-term support` (LTS) 版本。但这并不意味着该仓库下的 test 版本内核就不稳定，以上三个版本的内核的 test 分支均可使用，追溯的是上游的主线版。

在这里，我以 :gepkg:`sys-kernel/gentoo-sources` 为例。

.. _`内核配置`:

编译安装的整体流程
-----------------------------

.. _`上文已有`:

根据上下文环境，当前系统下只有一个二进制的内核，因此先安装上述内核，然后开始（以下操作需 root 用户进行，或自行使用 sudo 等命令）

.. code-block:: shell

  # 安装源码版的内核，以及 genkernel 工具
  emerge -vj sys-kernel/gentoo-sources sys-kernel/genkernel
  # 此处的 genkernel 工具可用于生成内核的 initramfs 文件

  # 安装完毕后使用 eselect 列出当前所有的内核
  eselect kernel list

  # 将源码版的内核设为选定
  eselect kernel set {序号}
  # 此时，路径 /usr/src/linux 会软链接到新安装的源码版内核目录下

  # 切换到内核目录下
  cd /usr/src/linux

  # 创建/修改配置文件
  make localmodconfig
  # 此命令基于当前环境快速创建了一个可用配置文件
  # 详细看下一节说明

  # 编译内核
  make -j {任务数}

  # 无报错后安装模块及内核
  make modules_install
  make install

  # 生成此内核对应的 initramfs 文件
  genkernel --kernel-config=/usr/src/linux/.config initramfs

  # 更新 Grub 菜单
  grub-mkconfig -o /boot/grub/grub.cfg

以上即内核从配置到编译到安装再到更新启动菜单的整体流程。

关于内核配置
-----------------------------

内核是否真的需要自定义配置？这个问题因人而异，有人想要一份精简的内核，有人只要功能完善即可。我个人建议则是，非嵌入式环境下，对内核体积没要求情况下量力而行即可。内核的配置系统太过庞与复杂，理解所有的配置很难。而纯粹使用通用的配置则会导致模块目录太大，无用的模块太多，也不妥。

上述步骤中的 :code:`make localmodconfig` 生成了一份完整的内核配置文件。此命令的含义是，以当前系统环境为参考，禁用没有被加载的模块配置。可在纯模块加载的系统环境下，接上你有的设备，开启你需要用到的所有服务，然后执行它。一般用于首次配置内核，使得后续配置更轻松。

而进一步的配置可以在内核目录下使用 :code:`make menuconfig` 命令打开一个界面化的配置菜单，根据界面内提示进行。也可以执行 :code:`make help` 显示帮助信息，以方便根据需要自行选择。

自定义配置时，建议给该配置文件设定一个自定义版本，以便于区分，配置路径位于::

  General setup  --->
    (-examplename) Local version - append to kernel release

其它的项目本文不会说明，建议查阅 `官方内核配置文档`_ ，其它可查阅的资料有：

* 在界面化的配置菜单界面，选中选项按下 :kbd:`h` 后显示的说明
* 查询硬件设备对应驱动的 Linux-Hardware 站点（英文）： https://linux-hardware.org/index.php?view=search
* cateee.net 的 Linux 内核驱动数据库（英文）： https://cateee.net/lkddb/web-lkddb/
* 金步国针对旧版本内核的配置说明（中文）： http://www.jinbuguo.com/kernel/longterm-linux-kernel-options.html

关于 initramfs
-----------------------------

配置内核时，有一个重要的内容是 initramfs (initial ram file system) ，它用于解决如何在真正初始化系统运行前执行用户空间程序。类似的方案还有一种叫 initrd ，两者功能基本一致，实现方式有差异，这里只以 initramfs 为例说明。

它代表着一种方案，也代表着一个文件。它在一些基础情况下并不是必须的（比如本文的上下文环境）。

在说明它存在的意义前，先简单说明下 Linux 系统的基本启动流程：

1. PC 加电，BIOS/UEFI 自检后载入系统引导程序
2. 引导程序载入内核
3. 内核挂载根目录所对应的分区
4. 内核执行根目录下系统的初始化（init）命令
5. 自此来到了用户空间下

这个基本的流程里面会出现问题，看步骤 3

* 问题一、如果这个根目录的分区无法直接挂载怎么办（被加密了、使用了 RAID、它是一个 NFS，等情况）
* 问题二、如果这个根目录的分区下的 :file:`/usr` 又单独分区了，里面没所需文件怎么办（这个文件夹包含了系统的库文件等）

如果上述两种情况都未出现，那么只要把根目录分区所对应的文件系统驱动被编译进内核（而非模块的形式），就可以省略掉 initramfs ；如果出现了任意一种情况，这个时候就需要 initramfs 的参与。

正如前文所说， initramfs 提供了在真正系统初始化前提前进入用户空间的功能，它其实就是一个简略版的完整系统，通过它，可以把该解密的分区解密，该挂载的内核无法直接挂载的分区（包括模块未加载，额外的分区，需要联网等情况）都挂载好，之后再由根目录下真正的系统初始化程序接管。

了解了其功能，现在开始说如何制作它。

Gentoo Linux 提供了一个工具叫 :gepkg:`sys-kernel/genkernel` 可用于创建 initramfs ，并且有别于其它的 initramfs 创建工具， genkernel 会单独编译一个独立的 initramfs 环境（而非直接使用当前系统环境），并打包压缩。这会使得其相对于其它的工具（比如 dracut）创建过程更慢。

简单的使用例子 `上文已有`_ ，其配置文件位于 :file:`/etc/genkernel.conf` ，里面对每个变量的设置都有详细的说明。

总结及引导
==================================================

本文以一条较为单一的路线讲述了 Gentoo Linux 的安装及使用，勾勒了一个大致的框架，以便于快速掌握。

当通读了安装几章后会发现， Gentoo Linux 的安装其实很简单，复杂的在它的使用上。同时还会发现，使用 Gentoo Linux 需要一定的耐心，Portage 的绝大部分的软件包都是从源码编译安装的，相对于其它二进制包的发行版，会比较花时间。

而使用源码进行安装的好处，可以在日常使用中来逐渐发现，举个例子，你可以很方便的给需要的软件包打 patch 后编译安装到系统上（还不会污染包管理系统），以满足自己的需要。使用源码进行安装使得 Gentoo Linux 可以只依赖于软件包的最上游，更安心。

由于 Portage 的依赖管理在本地，所以系统上的所有软件包都会处于自己的掌控范围内（比如可以在系统整体升级的情况下，设置某几个包不升级，只要处理好依赖关系）。

我对 Gentoo Linux 的评价是 **随心所欲** 。

至此，内容已全部结束。

*若对本文有任何问题，都欢迎访问文章开头的用户群组，找我 @cwittlut_on_TG*

接下来，

* 若想进一步学习 Gentoo Linux 的知识，请访问文章 `开头`_ 所指出的 Gentoo Wiki 页面。里面的内容非常之丰富。
* 若对 Gentoo Linux 下的 Portage 包管理器感兴趣，请访问 `开发手册`_ 。

建议，

* 善用搜索
* 不在不明白某个配置/选项含义时使用它
* 每次安装新的系统服务/系统工具时，都去查阅下 Gentoo wiki 对应词条
* emerge 完成后，出现的提示信息要看
* 新出的 news 要看

完。

题外话：
  我有一个脚本，可以比较方便地将其它 Linux 发行版转为 Gentoo Linux，目前还是处于测试状态中，有需要的话可以使用，有问题可以找我反馈，但我不负责数据丢失等问题。

  地址 https://gitlab.com/cwittlut/distro2gentoo

.. _`Gentoo Linux 安装 —— 带硬盘加密`: https://bitbili.net/reinstall_gentoo.html
.. _`Gentoo Wiki 页`: https://wiki.gentoo.org/wiki/Main_Page
.. _`这里`: https://github.com/bekcpear/mypelicanconfandarticles/blob/master/content/Tech/gentoo-linux-guide-for-installation-and-usage-tutorial.rst
.. _`bilibili （需要登录才能查看高清版）`: https://www.bilibili.com/video/BV1wv411u7ZU/
.. _`我的公开链接下载`: https://public.cwittlut.dev/share/VGhEB0fI/Videos/Gentoo/5%20%E5%88%86%E9%92%9F%E9%80%9F%E7%9C%8B%20Gentoo%20Linux%20%E5%AE%8C%E6%95%B4%E5%AE%89%E8%A3%85%E8%BF%9B%20KDE%20Plasma.mp4
.. _`北外镜像地址`: https://mirrors.bfsu.edu.cn/gentoo/
.. _`镜像列表`: https://www.gentoo.org/downloads/mirrors/#CN
.. _`Rufus`: https://rufus.ie/zh/
.. _`对应的 wiki`: https://wiki.gentoo.org/wiki/Profile_(Portage)
.. _`2021-10-18 起`: https://gitweb.gentoo.org/proj/releng.git/commit/?id=59328ba4341123278bf87d14a802333602d83b7e
.. _`glibc 的 git 仓库`: https://sourceware.org/git/?p=glibc.git;a=blob;f=posix/regcomp.c;h=887e5b50684e22f501011a9cac52ebe1a0bb3894;hb=HEAD#l877
.. _`官方内核配置文档`: https://wiki.gentoo.org/wiki/Kernel#Configuration
.. _`rsync 镜像列表`: https://www.gentoo.org/support/rsync-mirrors/
.. _`桌面环境`: https://wiki.gentoo.org/wiki/Desktop_environment
.. _`窗口管理器`: https://wiki.gentoo.org/wiki/Window_manager
.. _`NVIDIA/nvidia-drivers`: https://wiki.gentoo.org/wiki/NVIDIA/nvidia-drivers
.. _`::gentoo-zh`: https://github.com/gentoo-mirror/gentoo-zh
.. _`个人仓库`: https://github.com/gentoo-mirror/ryans
.. _`Rime 的 CustomizationGuide`: https://github.com/rime/home/wiki/CustomizationGuide
.. _`Package sets`: https://wiki.gentoo.org/wiki/Package_sets
.. _`ebuild repository`: https://wiki.gentoo.org/wiki/Ebuild_repository
.. _`开发手册`: https://devmanual.gentoo.org/
