==================================================
Gentoo Linux 安装及使用指南
==================================================

:slug: gentoo-linux-installation-and-usage-guide
:date: 2021-10-03 11:35
:lang: zh_hans
:color: #463c65
:tags: Gentoo, Linux, guide, installation, usage
:mykeywords: gentoo,linux,installation,usage,guide,howto,handbook
:description: 十分精简、适合新手、可持续进阶的 Gentoo Linux 完整安装及使用指南。
:featured_image: /nocimages/gentoo.png
:noindent: true
:summary:

.. contents::

很早以前，我就有写了一篇安装 Gentoo Linux 的文章（ `Gentoo Linux 安装 —— 带硬盘加密`_ ），只是那篇文章存在局限性。因为一些原因，我打算写一篇更详细更完整，适合新手且可以无缝进阶的 Gentoo Linux 安装及使用指南。

* 本文面向新手，十分精简，配置正确
* 本文以 AMD64(x86_64) 平台为例进行说明
* 本文以安装到实体机为目的（也适用于虚拟机）
* 本文唯一原始链接： https://bitbili.net/gentoo-linux-installation-and-usage-guide.html
* 如有问题可以上 https://t.me/gentoo_zh 提问/反馈

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

1. 打开 `北外镜像地址`_ ，进入目录 :file:`releases/amd64/autobuilds/current-install-amd64-minimal/` 下载最小化安装系统镜像，名字为 :file:`install-amd64-minimal-<日期>.iso`

   .. note::

     镜像地址是可以自由选择的，你可以选择更靠近自己的镜像服务器，Gentoo Linux 官方有收录的 `镜像列表`_ 。

     LiveCD 也同样不一定是 Gentoo Linux 的，可选系统的 LiveCD ，但本文以 Gentoo Linux 的为例。

     可选步骤
       为了保险起见，下载好的文件需要校验其完整性，镜像服务器会提供名为 :file:`install-amd63-minimal-<日期>.iso.DIGESTS` 和 :file:`install-amd64-minimal-<日期>.iso.DIGESTS.asc` 的校验文件。

       如今都是通过 https 协议下载文件，遂通常使用 :file:`.DIGESTS` 后缀的文件完成校验即可，该文件内包含四个 HASH 值，使用对应的工具来生成下载的 :file:`.iso` 文件的 HASH，后进行比较即可。

       Windows 平台可以使用 HashCalc 来生成，其可以生成 sha512sum，但是不支持 b2sum，一般来说两者之一匹配就可以了，如果一定想看看 b2sum 的话，可以在 :file:`https://www.blake2.net/` 下载适用 Windows 的二进制包后在命令行下执行生成。

       Linux 平台一般都默认安装了对应工具，命令为 :code:`sha512sum` 和 :code:`b2sum` 。

       后一个 :file:`.DIGESTS.asc` 校验文件附带上了签名信息，可以使用 Gentoo Linux 发布的公钥来校验这个包含 HASH 值的文件是否完整且未被篡改，超出本文内容，这里不进行说明。

2. 将 :file:`.iso` 文件写入到 U 盘。

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

     如果是虚拟机，那么直接把 livecd 挂载到虚拟机的光驱，选择光驱启动即可，其它步骤一致。

配置安装环境
==================================================

连接网络
-----------------------------

有线
+++++++++++++++

1. 网络环境带 DHCP 服务的（比如家用路由器连接的），livecd 默认会运行 dhcpcd 服务，不出意外，进入环境后直接可以联网。
2. 网络环境无 DHCP 服务或 DHCP 无效需要手动配置网络的，需要知道网关 IP，可用的网络地址，然后执行如下命令：

   .. code-block:: shell

     # 先列出到当前使用的网卡
     ip link
     # 假设这里看到了正在使用的网卡为 enp5s0
     ip link set dev enp5s0 up # 确保其开启
     # 这里假设　网关地址为： 10.0.1.1
     # 　　　可用网络地址为： 10.0.1.2
     # 　　　　　子网掩码为： 255.255.255.0 （即 CIDR 符号为 /24）
     ip address add 10.0.1.2/24 dev enp5s0
     ip route add default via 10.0.1.1 dev enp5s0
     # 这样就配置好了网卡的 IP 和默认路由
     # 未假设的内容即为固定参数，无需变动

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


认证通过连接上无线网络后，再采取和有线一样的方式进行联网配置，一般会直接由 DHCP 服务器给本机分配上 IP，如果没有，参考有线配置段落。

DNS 及测试
+++++++++++++++

执行

.. code-block:: shell

  cat /etc/resolv.conf

查看 DNS 配置信息，通常使用 DHCP 配置的网络会自动获取到 DNS 地址后配置，如若没有，请执行

.. code-block:: shell

  echo 'nameserver 223.5.5.5' >/etc/resolv.conf

写入 DNS 配置，这里我选用的阿里云的公共 DNS 地址，也可以改成其它的。

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

执行 :code:`lsblk` 列出当前所有的块设备，硬盘对应的名称一般为 :file:`sdX` ， :file:`nvmeXnX` 这种（虚拟机下可能为 :file:`vdX` ），其中 :file:`X` 为英文字母或阿拉伯数字。

确定好需要操作的块设备，这里假设为 :file:`sdX` ，然后执行自带的 :code:`fdisk` 命令进行分区（分区工具很多，这里仅以该工具为例）

.. code-block:: shell

  fdisk /dev/sdX

*若硬盘是与其它系统共用，仅有部分空闲空间的用于安装 Gentoo Linux 的，有些命令可能是无需操作的，对于这些命令，我会在命令后使用* :code:`#!!!` *这样的注释进行提醒，并说明；如果你是在一块完整的硬盘上安装，可以输入以下完整的命令*

执行上述命令后，进入了 :code:`fdisk` 交互界面，继续执行如下操作

.. note::

  在执行写入分区表操作（即 :code:`w` 命令）前，分区表不会实际更改，如若出错，可以执行 :code:`q` 退出交互界面重新进入再次操作

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

查看现在的分区表，记住现在的 EFI 分区（若有），启动分区，交换分区（若有）以及根分区的设备名。这里假设

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

.. note::

  随着时间的推移， stage3 包名可能会略有改动，如果后续发现有存在改动，请从更新时间最靠近的一批 stage3 文件中选择并下载。

这里以 :file:`current-stage3-amd64-openrc` 为例，那么选择进入该目录，选中 :file:`stage3-amd64-openrc-<日期>.tar.xz` 文件，回车进行下载。这里请同时下载其校验文件 :file:`stage3-amd64-openrc-<日期>.tar.xz.DIGESTS` ，默认存储路径为执行 :code:`links` 的当前目录，下载完成后，按 :kbd:`q` 退出，执行

.. code-block:: shell

   # 列出当前目录下的内容，确保两个下载的文件存在
   ls

   # 使用 sha512sum 校验文件
   sha512sum -c --ignore-missing stage3-amd64-openrc-<日期>.tar.xz.DIGESTS

.. note::

  可选步骤
    如果想要进行更加严格的验证，可替换下载原 :file:`.DIGESTS` 文件为 :file:`stage3-amd64-openrc-<日期>.tar.xz.DIGESTS.asc` ，后退出 links 界面，执行

    .. code-block:: shell

      # 导入 Gentoo Linux 的发布公钥
      gpg --keyserver hkps://keys.gentoo.org --recv-keys 0x13EBBDBEDE7A12775DFDB1BABB572E0E2D182910

      # 校验 DIGESTS 文件
      gpg --verify -o stage3-amd64-openrc-<日期>.tar.xz.DIGESTS{,.asc}

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
  tar xpvf /root/stage3-amd64-openrc-<日期>.tar.xz --xattrs-include='*.*' --numeric-owner

配置镜像地址
-----------------------------

为了更快速的下载文件，配置一个离自己近的镜像服务器地址很重要，执行

.. code-block:: shell

  mirrorselect -i -o >>/mnt/gentoo/etc/portage/make.conf

会打开一个界面供选择镜像地址，比如在中国的话，可选 aliyun/netease/tsinghua 的。

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

该命令会以分包的形式从之前配置好的镜像地址下载最近打包好的 portage 数据库到本地，并解压后使用。 *portage* 是 Gentoo Linux 的包管理器，这个数据库是安装各种软件的基础。

.. note::

  安装好数据库后，基本都会有一个让阅读新闻的提示，运行命令

  .. code-block:: shell

    eselect news read --quiet

  来标记全部阅读，这些信息对于全新的安装环境来说，很多都是过期的，不看问题也不大。之后可以运行

  .. code-block:: shell

    eselect news list

  以列出所有新闻的标题，再根据序号选择性地查看有用的信息

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


安装内核及引导
-----------------------------

执行

.. code-block:: shell

  emerge -vj gentoo-kernel-bin grub

该命令会为系统安装二进制的内核以及 grub 安装程序（其它引导器碍于篇幅这里不再说明）。

配置 fstab
-----------------------------

执行

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

     这里值得注意一点，一些旧主板有可能存在不识别指定位置 EFI 实体的情况，这种情况下需要执行：

     .. code-block:: shell

       grub-install --target=x86_64-efi --efi-directory=/boot/efi/ --removable

     将 EFI 实体安装到通用目录下。无需直接尝试，等发现无法启动后再来操作。

配置
+++++++++++++++

执行

.. code-block:: shell

  # （可选）如果之前有分配交换分区，在这里可以执行如下命令以启用其休眠后唤醒的功能
  sed -Ei "/GRUB_CMDLINE_LINUX_DEFAULT/s/^#*(GRUB.*DEFAULT=).*$/\1\"resume=UUID=$(lsblk -fnoUUID /dev/sdX4)\"/" /etc/default/grub
  # 也可以手动修改，打开 /etc/default/grub 文件
  # 　　　找到 GRUB_CMDLINE_LINUX_DEFAULT 变量
  # 　　　去掉其注释标记 (#) 后
  # 　　　在其双引号内添加上内容：
  # 　　　　　　　resume=UUID=<UUID 值>
  # 　　　此 <UUID 值> 可由命令 lsblk -fnoUUID /dev/sdX4 显示

  # 创建配置
  grub-mkconfig -o /boot/grub/grub.cfg

以完成引导的配置，该命令会自动根据 :file:`/etc/fstab` 以及 :file:`/etc/default/grub` 的内容来生成所需要的引导配置。

.. note::

  如果电脑存在多系统，可以执行如下步骤添加其它系统的引导菜单选项

  .. code-block:: shell

    # 给 grub 添加 mount 这个 USE 以满足 os-prober 的依赖
    echo 'sys-boot/grub mount' >/etc/portage/package.use/grub

    # 安装 os-prober 工具
    emerge -vj os-prober

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
     # 创建普通用户，同时将其额外添加到 wheel 组
     # 这里的用户名只能是字母和数字，数字不能打头，不要给空格
     useradd -G wheel 「用户名」

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

执行

.. code-block:: shell

  emerge -vj net-misc/networkmanager

这是最方便的支持多种联网方式的工具，安装好它之后基本能满足所有要求。安装完成后，执行 :code:`nmtui` 进入可视化的配置界面，根据提示进行配置。

配置完成后，添加开机启动服务

.. code-block:: shell

  # 若你是安装的 openrc 系统，执行
  rc-update add NetworkManager default

  # 若你是安装的 systemd 系统，执行
  systemctl enable NetworkManager

安装日志服务
-----------------------------

这段仅针对 openrc 用户，systemd 用户有自带的日志服务。

openrc 这里我推荐使用 syslog-ng，执行

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

重启后会出现预期中的 grub 菜单界面，倒计时后会自动进入首选引导项，加载内核，启动初始化程序，最后进入操作系统。

这时候的 Gentoo Linux 很丑，只有一个命令行界面，接下来开始说明如何正确的使用 Gentoo Linux。

未完（休息一下）


.. _`Gentoo Linux 安装 —— 带硬盘加密`: https://bitbili.net/reinstall_gentoo.html
.. _`北外镜像地址`: https://mirrors.bfsu.edu.cn/gentoo/
.. _`镜像列表`: https://www.gentoo.org/downloads/mirrors/#CN
.. _`Rufus`: https://rufus.ie/zh/
.. _`对应的 wiki`: https://wiki.gentoo.org/wiki/Profile_(Portage)


