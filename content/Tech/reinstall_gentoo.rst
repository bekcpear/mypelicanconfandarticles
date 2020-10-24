=====================================================================================================================
Gentoo Linux 安装 —— 带硬盘加密
=====================================================================================================================

:slug: reinstall_gentoo
:date: 2016-05-22 23:24
:modified: 2020-10-18 15:07
:lang: zh_hans
:tags: gentoo, installation, luks
:description: 安装 Gentoo Linux 的主要步骤。
:color: #463c65
:noindent: true
:featured_image: /nocimages/gentoo_minimal_install_media_1.png
:summary:

.. contents::

:del:`可能是因为运行了某A开头VPN的Linux客户端安装脚本，加上@world更新以及内核重新配置，导致系统彻底崩溃，试了很多方法无果，干脆重新安装，也好重新整理。`

.. PELICAN_BEGIN_SUMMARY

时隔 4 年，我又来装 Gentoo 啦～ 之前换了个台式，平台太新了，怎么都搞不定显卡的驱动，后来就一直笔记本用的 Arch，但是现在笔记本越来越卡.. 于是.. 我又拿台式装 Gentoo 了，台式很牛B， 16 核 32 线程， :del:`跑起 Gentoo 肯定很爽～|我想多了... 再强大的电脑用 Gentoo 都不过分`

此次，我是在已有 Windows 10 系统的情况下，用一块额外完整的硬盘安装 Gentoo， :del:`并配置双系统引导，` 同时开启硬盘加密。

写在前面
============================================================

Gentoo 和一般的 Linux 的发行版的区别在于 Gentoo 需要自己编译安装，且自定义度极其高，可以很方便地定制与个性化（从内核到桌面以及各种管理软件），也更易于理解 Linux。

本文重新整理完善，旨在以备不时之需，也希望可以帮到网友（也可以看 `官方的 wiki`_ ）。文档会包含主要流程，言简意赅。

.. PELICAN_END_SUMMARY

Gentoo 的安装主要是 10 个步骤，分别对应一个状态（此段翻译自上述官方 Wiki）：

========== ===========================================================================================================
   步骤       对应结果
========== ===========================================================================================================
    1        进入到一个可以安装 Gentoo 的工作环境
    2        安装 Gentoo 的网络就绪
    3        安置 Gentoo 的硬盘就绪
    4        安装环境准备完成，且用户可以 chroot 到新的环境下了
    5        Gentoo 需要的核心包文件安装完成
    6        Linux 内核配置且安装完成
    7        大部分 Gentoo 系统配置文件创建完成
    8        必要的系统工具安装完成
    9        适当的启动引导安装且配置完成
   10        新安装的 Gentoo Linux 环境准备好被探索使用了
========== ===========================================================================================================

下文会根据这 10 个步骤和对应的状态来整理。

步骤一： 进入到安装环境
============================================================

需要准备的内容：

* 一个好的 U 盘
* 互联网络
* 一台可控制的主机
* 也许还需要一台正常使用的主机（Windows/Mac/类 UNIX 皆可）

下载并校验安装文件
------------------------------------------------------------

从 Gentoo 的 `镜像站点`_ 获取适合的最小安装 CD 文件，并校验，比如 `清华的 TUNA 源`_ ：

::

  目录： /gentoo/releases/amd64/autobuilds/current-install-amd64-minimal/
  Parent directory/                                       -           -
  hardened/                                               -           2020-09-21 17:01
  install-amd64-minimal-20200920T214503Z.iso              428.0 MiB   2020-09-21 07:48
  install-amd64-minimal-20200920T214503Z.iso.CONTENTS.gz  1.0 KiB     2020-09-21 07:48
  install-amd64-minimal-20200920T214503Z.iso.DIGESTS      778 B       2020-09-21 07:48
  install-amd64-minimal-20200920T214503Z.iso.DIGESTS.asc  1.3 KiB     2020-09-21 08:01
   …

.. note::

  有时候可能会遇到同步不完全的情况，遇到时就更换一个源下载。

1. 需要的是这个 .iso 的文件，下载它。（ .CONTENTS.gz 文件是一个文本文件压缩包，该文本内存储了 .iso 文件内所有文件的列表）
2. 下载校验文件， .DIGESTS 文件不带签名，里面存储了 .iso 以及 .CONTENTS.gz 散列值。而 .DIGESTS.asc 是前者的带签名版，直接下载这个。
3. 导入 `公钥`_ 并校验：

.. code-block:: bash

  gpg --keyserver keys.gnupg.net --recv-keys 0xBB572E0E2D182910 # 导入对应公钥
  gpg --verify install-amd64-minimal-20200920T214503Z.iso.DIGESTS.asc # 检查文件完整性
  sha512sum install-amd64-minimal-20200920T214503Z.iso # 然后与文件内散列值进行比对验证

制作盘启动盘并进入安装环境
------------------------------------------------------------

校验没问题后就制作 U 盘启动盘， 习惯性使用 :code:`dd` 命令：

.. code-block:: bash

  dd bs=4M if=install-amd64-minimal-20200920T214503Z.iso of=/dev/sdc status=progress oflag=sync

如果需要制作光盘启动盘，使用 :code:`cdrecord` 工具。如果仅有 Windows 的话， Windows 7 以上可以直接使用系统自带的功能将镜像写入到光盘内；如果是 U 盘，可以尝试 Rufus，但我未验证。

之后就是开机选择 U 盘作为启动盘进入安装环境，根据主板不同，开机后敲击 F1/F2/F12 等选择 U 盘启动。

.. image:: /nocimages/gentoo_minimal_install_media_0.png
  :alt: Gentoo 启动盘界面

步骤二： 连接网络
============================================================

我的台式带有线和无线网卡，直接使用有线网卡，已经被内核识别且可以使用，自己配置一下路由即可，比如：

.. code-block:: bash

  ip link set dev enp5s0 up
  ip add add 192.168.30.100.24 dev enp5s0
  ip route add default via 192.168.30.1 dev enp5s0
  echo 'nameserver 223.5.5.5' >> /etc/resolv.conf

.. note::
  这里遇到一个问题，本以为主板上默认的千兆网卡驱动是被加载的，结果后来发现默认加载的是万兆网卡，所以当发现接口状态怎么都是 DOWN 时，考虑加载的网卡接口不对。这里可以使用 :code:`lspci | grep -i eth` 查看所有网卡接口，然后 :code:`lspci -v -s<slot>` 查看哪些有加载完成驱动。

或者开启 dhcpcd 服务，Gentoo 默认使用 OpenRC，所以可以运行：

.. code-block:: bash

  /etc/init.d/dhcpcd start

启动 dhcpcd 服务。

其它方式可以自行查找官方文档，比如通常情况下，目前无线基本使用 WPA 加密程序，那么直接使用 :code:`wpa_supplicant` 命令，在明确知道无线 SSID 和密码的情况下，执行如下命令连接：

.. code-block:: bash

  wpa_supplicant -i <INTERFACE> -c <(wpa_passphrase "<SSID>" "<PASSWORD>")

确认没问题后，可以添加 :code:`-B` 选项重新执行使之以守护进程模式在后台运行。如果仅知道无线密码，但是不确定无线的 SSID，可以通过以下命令获取后自行确认：

.. code-block:: bash

  iw dev <INTERFACE> scan | grep SSID

拨号则使用 :code:`pppoe-setup` 和 :code:`pppoe-start` 命令，具体我没测试条件，反正安装 CD 下自带的这个脚本有很自动化的配置选项。

测试网络连通后，这个步骤结束。如果网络无法连通，执行 :code:`ip a` , :code:`ip r` 查看当前获取的 IP 和路由，如果都正常，则去确认 :file:`/etc/resolv.conf` 文件下的 DNS 设置情况，通过 :code:`ping` 各个网卡/网关地址和 DNS 地址排查。

步骤三： 准备好硬盘
============================================================

因为我打算加密硬盘，所以加密操作也需要在这个步骤完成。也就是在这个步骤，需要确定使用的 BIOS 固件接口及引导程序，做分区，确定选用的文件系统，加密分区/硬盘，格式化，挂载。

因为需要使用双系统引导，所以复用 Windows 的 EFI 分区，使用 UEFI，但是这里还是要留出足够的 EFI 分区空间以备以后单硬盘单系统使用。 :file:`/boot` 分区单分，其它分区完整一个加密盘，所以硬盘的分区结果如下：

::

  sde                 8:64  0   477G  0 disk
  |--sde1             8:65  0   512M  0 part
  |--sde2             8:66  0 476.4G  0 part
     |--ct0         253:0   0 476.4G  0 crypt

其中 sde1 用作当前的 boot 分区， sde2 做 luks 加密，然后格式化成 btrfs 分区，这里不用 lvm，因为我完全不想分区，直接采用 btrfs 的子卷。具体命令：

.. code-block:: bash

  parted /dev/sde
  (parted) mklabel gpt
  (parted) unit MiB
  (parted) mkpart primary 2 514
  (parted) mkpart primary 515 -1
  (parted) name 1 boot # 这里不给 boot 分区添上 boot 标记，因为是需要复用 Windows 的 EFI 分区引导
  (parted) name 2 luks
  (parted) q

  cryptsetup luksFormat /dev/sde2
  cryptsetup open /dev/sde2 ct0
  mkfs.btrfs /dev/mapper/ct0
  mkfs.vfat -F32 /dev/sde1
  mount /dev/mapper/ct0 /mnt/gentoo

因为我是决定使用 btrfs 的子卷功能，所以这里划分单独的子卷，当作根分区：

.. code-block:: bash

  btrfs subvolume create /mnt/gentoo/subvol-root
  btrfs subvolume create /mnt/gentoo/subvol-home
  btrfs subvolume create /mnt/gentoo/subvol-snapshots
  btrfs subvolume set-default /mnt/gentoo/subvol-root

然后重新挂载子卷到 :file:`/mnt/gentoo` 下：

.. code-block:: bash

  umount /mnt/gentoo
  mount /dev/mapper/ct0 /mnt/gentoo

至此硬盘准备完毕。

步骤四： 准备好 chroot 到新环境
============================================================

首先调整好时间，因为错误的时间会引起一些很奇怪的问题，比如安装好的系统文件的时间超前的话，之后编译安装过程可能会出现报错，等等之类的问题。

.. code-block:: bash

  ntpd -q -g

然后访问镜像站去下载 stage3 包文件，可以使用 :code:`links` 工具，注意下载完成后校验，方法同上述校验安装文件。

.. code-block:: bash

  links https://mirrors.tuna.tsinghua.edu.cn/gentoo/releases/amd64/autobuilds/current-stage3-amd64/
  # 下载 stage3-xxx-xxx.tar.xz 以及 stage3-xxx-xxx.tar.xz.DIGESTS.asc
  gpg --keyserver keys.gnupg.net --recv-keys 0xBB572E0E2D182910
  gpg --verify stage3-xxx-xxx.tar.xz.DIGESTS.asc #之后对比

之后切换到挂载的 :file:`/mnt/gentoo` 目录后，解压 stage3：

.. code-block:: bash

  cd /mnt/gentoo
  tar xpvf stage3-*.tar.xz --xattrs-include='*.*' --numeric-owner #解压选项不要漏错

然后要针对本机配置一下编译环境。

打开 :file:`etc/portage/make.conf` 文件，简单编辑常用的选项（语法： VARIABLE="content" ）：

CFLAGS/CXXFLAGS ，主要是为了优化 gcc/C 编译

* -march= / -mtune= ：计算机的架构，一般使用 native 告知编译针对本机。
* -O ： gcc 优化的标签， s 优化大小， 0 不做优化， 1/2/3 优化编译速度，一般使用 -O2
* -pipe ：占用更多的内存，避免编译时出现碰撞现象而使用管道代替临时文件，内存大的话，建议开启
* -fomit-frame-pointer ：具体这个不太了解，大致意思就是释放多余的指针，但是对于 debug 有负面影响

.. code-block:: bash

  # Compiler flags to set for all languages
  COMMON_FLAGS="-march=native -O2 -pipe"
  # Use the same settings for both variables
  CFLAGS="${COMMON_FLAGS}"
  CXXFLAGS="${COMMON_FLAGS}"

MAKEOPTS，这个决定了每次并行运行的任务数，一般设置 CPU 的个数/核心数 +1，核心太多的话，也可以适度减少以留出余量运行其它程序。

.. code-block:: bash

  MAKEOPTS="-j28"

其他的暂时不需要修改。

安装环境完成，可以 chroot 后开始安装基本的系统了。

步骤五： 安装基本的系统
============================================================

先选择一个/多个足够快的镜像地址（下载源码用于编译的安装）：

.. code-block:: bash

  mirrorselect -i -o >> /mnt/gentoo/etc/portage/make.conf

选择 163/TUNA 的源就好。然后可以再设定一个更快的 ebuild 资料库同步地址，如需设定，拷贝默认配置文件到如下地址：

.. code-block:: bash

  mkdir etc/portage/repos.conf
  cp usr/share/portage/config/repos.conf etc/portage/repos.conf/gentoo.conf

以 TUNA 源 rsync 方式为例，编辑 :file:`etc/portage/repos.conf/gentoo.conf` 文件，替换

.. code-block:: ini

  sync-uri = rsync://rsync.gentoo.org/gentoo-portage

为

.. code-block:: ini

  sync-uri = rsync://mirrors.tuna.tsinghua.edu.cn/gentoo-portage

不过我觉得少量的同步，采用官方源即可，也可以不替换。且这些以后都可以再改。

设置 DNS 服务器地址，可以直接复制之前配置的：

.. code-block:: bash

  cp -L /etc/resolv.conf etc/

然后挂载需要的文件系统： :file:`/proc` 和 :file:`/sys` 是伪文件系统，记录了 Linux 内核向环境所暴露的信息，后者原打算用于取代前者，输出内容更加结构化。 :file:`/dev` 则是常规文件系统，部分由 Linux 设备管理器管理，包含了所有的设备文件。 

.. code-block:: bash

  mount --types proc /proc proc
  mount --rbind /sys sys
  mount --make-rslave sys
  mount --rbind /dev dev
  mount --make-rslave dev

.. note::

  安装 systemd 支持一定需要 :code:`--make-rslave` 操作。

现在 chroot 到新的环境下：

.. code-block:: bash

  chroot /mnt/gentoo /bin/bash
  source /etc/profile
  export PS1="(chroot) $PS1"

挂载 boot 分区用于后续内核及引导的安装：

.. code-block:: bash

  mount /dev/sde1 /boot

通过网络安装 Gentoo ebuild 资料库：

.. code-block:: bash

  emerge-webrsync # 打包安装准备好的快照
  emerge --sync   # 然后同步更新到目前最新，这样可以最快速度安装完成

安装完成后，可能会提示有新闻，可以阅读一下，以防遇到奇怪的问题没法解决：

.. code-block:: bash

  eselect news list
  eselect news read [num]

之后选择合适的配置文件：

.. code-block:: bash

  eselect profile list # 列出可用的配置文件

::

  Available profile symlink targets:
     …
    [16]   default/linux/amd64/17.1 (stable) *
     …
    [20]   default/linux/amd64/17.1/desktop (stable) 
    [21]   default/linux/amd64/17.1/desktop/gnome (stable) 
     …
    [26]   default/linux/amd64/17.1/no-multilib (stable) 
     …
    [29]   default/linux/amd64/17.1/systemd (stable) 
     …

.. code-block:: bash

  eselect profile set [num] # 设定需要的配置文件，这里纠结了半天，还是选默认的 OpenRC，毕竟 Gentoo 文档主要围绕它。

为避免出现奇怪的问题，初始化安装的时候，需要选择对应下载的 stage3 包版本的配置文件。主配置文件安装完之后也可以再更改。

之后配置一下基本的全局 USE 变量，比如这些：

.. code-block:: ini

  USE="X initramfs cjk cups crypt udev alsa elogind zsh-completion bash-completion -consolekit -systemd"

因为我的根分区是加密的，所以必须启用 initramfs，后面的内核配置里也得开启。

然后更新 @world 集，这个集合包含了必要的系统软件以及明确选定的软件：

.. code-block:: bash

  emerge --ask --verbose --update --deep --changed-use @world

.. note::

  新系统自带 nano 编辑器，不自带 vim，可以先装一个，习惯使用 vim 的话。

配置 Timezone：

.. code-block:: bash

  ls /usr/share/zoneinfo/Asia/Shanghai
  echo "Asia/Shanghai" > /etc/timezone
  emerge --config sys-libs/timezone-data

配置语言环境（至少一个 UTF-8 编码的）：

.. code-block:: bash

  vim /etc/locale.gen # 这里添上需要的语言，支持的语言可以查看 /usr/share/i18n/SUPPORTED 文件
  locale-gen

之后选择默认的语言：

.. code-block:: bash

  eselect locale list # 列出当前的语言列表

::

  Available targets for the LANG variable:
  [1]  C
  [2]  C.utf8
  [3]  en_HK
  [4]  en_HK.iso88591
  [5]  en_HK.utf8 *
  [6]  en_US.utf8
  [7]  POSIX
  [8]  zh_CN
  [9]  zh_CN.gb2312
  [10] zh_CN.utf8
  [ ]  (free form)

.. code-block:: bash

  eselect locale set 5

现在重载一下当前环境：

.. code-block:: bash

  env-update && source /etc/profile && export PS1="(chroot) $PS1"

至此，基本系统核心文件就已经安装完成。

步骤六： 配置内核
============================================================

这个步骤应该说是安装 Gentoo 时最复杂的一个步骤了， Gentoo 提供了很多内核可选，这里先安装最基础的，先安装源码：

.. code-block:: bash

  emerge --ask sys-kernel/gentoo-sources

然后安装一下固件包，主要是用于某些无线驱动，开源的显卡驱动之类的：

.. code-block:: bash

  emerge --ask sys-kernel/linux-firmware # 选择性启用 savedconfig USE

这里可能需要在 :file:`/etc/portage/package.license` 下添加接受许可。

完成之后就可以开始配置编译内核了，有两种方式，一个手动配置，一个使用 :gepkg:`sys-kernel/genkernel` 工具来配置。我是选择手动配置的，虽然一开始真的看得整个人都是懵的，不过熟练了就好了。手动配置可以大大减少不需要的模块的安装和编译，也有利于启动速度，还可以后续继续熟悉优化内核配置，且把显卡驱动直接编译进内核后，在输入 LUKS 加密分区的密码时，就已经加载完成显卡驱动，屏幕看得也会舒服很多。

先安装两个工具：

.. code-block:: bash

  emerge --ask sys-apps/pciutils # 安装完成后可以使用 lspci 命令查看 pci 设备
                                 # chroot 环境下出现的一些 pcilib 警告是可以忽略的
  emerge --ask sys-kernel/genkernel # 用于生成 initramfs
  
这里还可以配合使用 :code:`lsmod` 命令查看，看安装 CD 下加载了哪些模块，帮助判断启用内核的一些功能。

现在进入内核配置菜单：

.. code-block:: bash

  cd /usr/src/linux
  make menuconfig

主要几个内容：

* CPU 电源管理
* DM-Crypt 支持
* EFI, GPT 支持
* 分区格式支持
* USB 驱动、网卡驱动、声卡驱动、显卡驱动、传感器驱动
* 其它细节项

这里还是看 `原文`_ ，相对复杂不太好简略说明。配置过程中，善用 :kbd:`/` 键搜索， :kbd:`H` 键查看说明，还可以参考金步国的 `内核配置文档翻译`_ ，说是翻译，其实很多都添加了自己的解释，相对官方文档易于理解太多。

配置完成后编译并安装：

.. code-block:: bash

  make -j30 # 数根据实际情况来，如果发现出错，则 make V=1 -j30 2>error.log 后，查看报错信息
  make modules_install && make install
  genkernel --kernel-config=/usr/src/linux/.config initramfs

内核这一部分，写的很少。实在是因为需要的内容太多，后续有机会单独整理吧。在之后的使用过程中，某些程序会需要额外的内核配置，到时候再参考 wiki 操作。

.. note::
  如果是第一次安装 Gentoo 且对内核配置也不熟悉，不要犹豫，直接用 :code:`genkernel` 生成，后续进入系统后再慢慢改内核配置以适配自己的机器。使用它只要一个命令足以（对应配置在 :file:`/etc/genkernel.conf` ）：

  .. code-block:: bash

    genkernel all

  如果在新的无现成内核配置文件的机器上安装的话，我目前觉得一个比较好的方式是： 先使用 :code:`genkernel` 工具生成一次内核，然后去修改生成的配置文件，去掉自己明确知道的不用的模块和功能，修改自己明确知道的一定要加载的模块编译进内核（结合使用 :code:`lspci` , :code:`lsmod` , :code:`hwinfo` , :code:`sensors-detect` 命令）。

  目前 `我的内核配置文件`_ ，对应的硬件是： 1950X CPU + Asus ROG ZENITH EXTREME ALPHA 主板 + AMD Vega 64 公版显卡；对应环境是： Gentoo Linux + BtrFS + LUKS2 根分区加密 + GRUB 引导。其中，主要驱动全部编译进内核，删掉了很多确定自己不需要的模块和功能，后续再行优化。

  **有一点要注意的是，参考 Gentoo 官方的 AMDGPU 配置文档，里面的固件列表是不全的，虽然文档也说明了，但一开始没仔细看，被坑死了；针对我这块显卡，我直接把 vega 开头的固件全部丢进去后.. 才启动，也不去深究哪个是哪个了，极大可能是 vega10/20_vce/uvd.bin**

关于 Microcode， 我的是 AMD 的 CPU，在全局开启 initramfs USE 的情况下，安装 :gepkg:`sys-kernel/linux-firmware` 时，会自动在 :file:`/boot` 目录下，创建一个 CPIO 格式微码文件 :file:`amd-uc.img` ，在 initrd 中使用，需要在 initramfs 前加载，具体规则看下方 initramfs 说明链接， :code:`grub-mkconfig` 会自动识别添加。如果是 Intel 的 CPU，则不会创建这个文件，需要手动创建，或者直接编译进内核，或者使用 :code:`genkernel` 命令生成。

查的部分一些资料，并不全：

* mcelog 不支持 AMD 的 CPU： :code:`mcelog --help` 输出有支持的芯片组
* DMA Engine 主要支持 Intel 的高端 U，AMD 上没看到有支持的： https://cateee.net/lkddb/web-lkddb/DMADEVICES.html
* initramfs 说明： https://wiki.debian.org/initramfs
* 1950x 是否支持 SME： https://github.com/AMDESE/AMDSEV/issues/1
* 我用不到的 IB 接口： https://en.wikipedia.org/wiki/InfiniBand
* 更新 microcode： https://wiki.gentoo.org/wiki/AMD_microcode
* tsc 报错，联系上下文看是正常的，这里关联 PIT HPET 等概念
* 我的 rtc 的驱动名： https://bugs.archlinux.org/task/59824
* 主板传感器芯片 IT8665E 未受支持： https://github.com/lm-sensors/lm-sensors/issues/195
* 某些内核选项需要打开专家模式后才可设置： https://forums.gentoo.org/viewtopic-t-1054448-start-0.html
* PCIE 上又一个报错： https://askubuntu.com/questions/949254/new-system-with-pcie-errors-need-help-debugging
* 无线网卡读取温度报错 bug： https://bugzilla.kernel.org/show_bug.cgi?id=201761
* ata 一个不是 bug 的报错： https://bugzilla.redhat.com/show_bug.cgi?id=653811
* 无线网卡额外固件 regulatory.db 报错： https://forums.gentoo.org/viewtopic-t-1114094-start-0.html 如若编译进内核，这个固件也要一起编译进去

步骤七： 完成系统配置
============================================================

内核配置编译完成后，最麻烦的一步做完了，下面就是需要做最后的系统配置。

先创建 fstab 文件 :file:`/etc/fstab` ，类似如下格式：

.. code-block:: ini

  # <fs>			<mountpoint>	<type>		<opts>		<dump/pass>

  # /dev/sde1
  UUID=<uuid>   /boot     vfat    rw,relatime,fmask=0022,dmask=0022,codepage=437,iocharset=iso8859-1,shortname=mixed,errors=remount-ro 0 2

  # /dev/sda2
  UUID=<uuid>   /boot/efi vfat    rw,relatime,fmask=0022,dmask=0022,codepage=437,iocharset=iso8859-1,shortname=mixed,errors=remount-ro 0 2

  # /dev/mapper/ct0
  UUID=<uuid>   /         btrfs   defaults,noatime,ssd,discard,subvolid=258,subvol=/subvol_root 0 1
  UUID=<uuid>   /home     btrfs   defaults,noatime,ssd,discard,subvolid=259,subvol=/subvol_home 0 2
  UUID=<uuid>   /.sss     btrfs   defaults,noatime,ssd,discard,subvolid=260,subvol=/subvol_snapshots 0 2

注意：

1. 因为我双系统，所以需要复用 Windows 的 EFI 分区并挂载；
2. btrfs 分区的 UUID 是解密后磁盘映射的 UUID
3. 别忘了添上子卷 ID

然后配置网络，这里直接安装 :gepkg:`net-misc/dhcpcd` 自动获取路由器的地址，无线网卡配置等最后再配置。如果仅能使用无线网卡，可以跳到后文去看。

设置硬件时钟 因为是和 Windows 双系统， Windows 写入 BIOS 的是本地时间且不可手动修改，所以需要设置 clock="local" 在 :file:`/etc/conf.d/hwclock`

这里也可以直接配置内核写入，不使用 openrc 的服务，但是两者冲突，需要禁用其中一种，见： https://wiki.gentoo.org/wiki/System_time#In-kernel_method

给 root 用户设置一个密码：

.. code-block:: bash

  passwd root

添加一个常用的非 root 用户，并指定额外的用户组以便使用 :code:`su` 命令：

.. code-block:: bash

  useradd -g users -G wheel <yourname>
  passwd <yourname>

步骤八： 完成系统工具的安装
============================================================

这个步骤可以安装一些需要的特定工具，比如：

* 管理加密分区工具 :gepkg:`sys-fs/cryptsetup`
* 计划任务工具如 :gepkg:`sys-process/cronie`
* 必要的日志工具如 :gepkg:`app-admin/sysklogd`
* 主文件系统工具，比如我是 btrfs 格式分区则用 :gepkg:`sys-fs/btrfs-progs`
* 无线网络配置工具， :gepkg:`net-wireless/iw` 用于网络发现和开放或 WEP 加密网络的连接， :gepkg:`net-wireless/wpa_supplicant` 用于 WPA/WPA2 加密网络的连接。
* 如果主机拨号的话，也需要 PPPoE 客户端 :gepkg:`net-dialup/ppp` ，并在内核下配置对应选项。

主要就是日志工具的启用， DHCP 客户端的启用，其它后面再装也可以：

.. code-block:: bash

  emerge -av app-admin/sysklogd sys-fs/cryptsetup
  rc-update add sysklogd default
  rc-update add dhcpcd default

步骤九： 完成系统引导的配置
============================================================

我选用 grub 作为引导程序，因为是 UEFI 固件启动，所以需要设定全局的 grub 参数，并安装 :gepkg:`sys-boot/grub` ：

.. code-block:: bash

  echo GRUB_PLATFORMS="efi-64" >> /etc/portage/make.conf
  emerge -av sys-boot/grub:2

设置参数是为了确保编译安装 grub 的时候，启用 efi 功能。

然后配置下引导选项，主要用于解密磁盘，在 :file:`/etc/default/grub` 内修改：

.. code-block:: ini

  GRUB_CMDLINE_LINUX="dobtrfs crypt_root=UUID=<uuid> root=UUID=<uuid>"

.. note::
  这里需要使用 UUID 来识别 root 分区，因为我没找到方法指定打开 LUKS 加密分区后的名字，在 Arch Linux 上可以通过在 crypt_root 参数后加 :code:`:<name>` 来指定，但是 Gentoo 尝试后不行，暂时不去理会了。

然后确认挂载完成 :file:`/boot` 和 Windows 复用的 :file:`/boot/efi` 分区后，安装 grub 引导：

.. code-block:: bash

  mount -a
  grub-install --target=x86_64-efi --boot-directory=/boot --efi-directory=/boot/efi/ --bootloader-id=Gentoo --debug
  grub-mkconfig -o /boot/grub/grub.cfg

无报错即安装完成。

.. note::
  某些主板，如果不支持写入 efi 实体位置的话，必须要让 efi 文件以此名称存放在此位置以识别（比如我以前的台式）：

  .. code-block:: bash

    mkdir /boot/efi/EFI/Boot
    cp /boot/efi/EFI/Gentoo/grubx64.efi /boot/efi/EFI/Boot/bootx64.efi
  
不急着配 Windows 双启，先重启查看是否完成：

.. code-block:: bash

  exit
  umount -l /mnt/gentoo/dev{/shm,/pts,}
  umount -Rf /mnt/gentoo
  reboot

不出意外，那么至此，成功启动。

.. image:: /nocimages/gentoo_minimal_install_media_1.png
  :alt: Gentoo 配置完成进入系统过程

步骤十： 收尾
============================================================

现在已经进入了新安装的 Gentoo 系统下了，虽然还没有桌面环境，但各类驱动应该都没有问题了。

后面的任务就是添加常用的非 root 用户，配置桌面环境/窗口管理器，安装需要的各类软件 :del:`，非常简单的 Windows 双启配置` 。

即使目前还没配 GRUB 双启，开机后 BIOS 下选择 Windows 的 EFI 实体也能启动 Windows。

**2020/10/10 更：**

差不多完工了，下面总结一下完成配置时遇到的一些问题。

关于 WM/DE 的选择
----------------------------------------------------

本来我是打算使用 Awesome 窗口管理器的，毕竟在笔记本上一直都是用的它，但是我发现一个问题，最新发布的版本居然还是 2019 年 1 月的，虽然仓库一直都有在更新，所以之前遇到的问题（全屏的 Client 初始打开时不计算任务栏高度，导致下方会被吞掉一小条，需要重新 :kbd:`Mod4` + :kbd:`M` 一下才行）依旧是没解决的，比较影响体验，我也很神奇在笔记本上坚持用了这么久。

其次，独立的 X :ruby:`混成器|Compositor` 效果都差强人意，最开始的 Xcompmgr 没有自带的透明规则，需要 WM 或其他工具配置，不能模糊化； Fork 自 xcompmgr-dana 的 Compton 现在已经无人维护，之前用这个感觉效果是最好的，但是模糊效果比较一般； Fork 自 Compton 的 Picom 是现在活跃维护的可独立运行的混成器，结果 xrender 后端下，模糊背景直接导致 WM 卡死， GLX 后端下模糊背景效果怎么都捣鼓不出来.. 然后再加上 Kwin 自带混成器模糊 Konsole 的磨砂透明背景效果真的很诱人；

并且，一个完整的 DE 可以节省我很多时间去写各种各样的插件脚本，提供了很多我不知道的细节上的设置，还有强大的社区支撑，所以我决定在 Gentoo 上抛弃 Awesome WM，但多年的习惯不想改，所以就需要配置 KDE 的快捷键了，于是我就把 KDE 的快捷键配置到非常类似 Awesome WM，基本上实现了平滑过度： `AwesomeWMLikeKDEShortcuts&CorrespondingScripts`_ .

如何在 Gentoo 上安装 KDE Plasma 桌面环境，直接参考 `官方维基`_ 即可，没有什么坑。整体的编译安装时间也不算长，从修改系统的 Profile 为 desktop/plasma 到完成 plasma-meta 的安装，我查了 :file:`emerge.log` ，确认花了整 1 个小时，那么作为参考，我编译安装完成 Chromium 的时间是 1 小时 44 分钟。

完成 KDE 安装后遇到的问题
----------------------------------------------------

那么安装完成之后遇到了什么问题呢？

.. admonition:: T/S

  首先，在 Awesome WM 下就遇到的问题——计算机睡眠（挂起到内存），唤醒后鼠标和 USB 耳机正常，但键盘无法使用的问题。

  先说结论， 应该是目前 Linux 的 xHCI 驱动对 USB 3.1 Gen 2 接口支持不够完善导致的，但是我不够确定，所以目前我的处理措施是在睡眠计算机时确保该接口不外接设备

具体问题是这样的： 

最开始当睡眠计算机时，出现唤醒后键盘无法输入的情况，但是鼠标正常，因为键盘附带蓝牙切换功能，所以我本以为是 USB 接口在唤醒后出现了掉电的问题导致键盘芯片可能卡住的情况。

这里接触到了很多，最主要的一点是：很多电脑的 BIOS 会在唤醒计算机时，重置 USB 总线，重置后 kernel 的日志会有:

.. code-block:: kmsg

  kernel: [14624.419353] usb usb1: root hub lost power or was reset
 
如此类似的提示信息。对于存储设备来说，设备掉电再唤醒后，就可能无法继续接着之前挂载点使用，于是内核出现了一个设置—— Enable USB persist by default ，这个设置不会改变 BIOS 的重置机制，且我打开了 BIOS 找了一遍也没有发现任何相关这个动作的设置，详细的说明看官方文档： https://www.kernel.org/doc/Documentation/driver-api/usb/persist.rst 也就是大致解决了掉电后无法平滑访问 USB 存储设备的问题。了解之后判断且尝试后发现，这个选项不会导致上述问题的出现。

后来机缘巧合换了一个 USB 接口，突然发现正常了，然后我从 USB 接口入手去排错，尝试了很多次后，发现了最开始说明的情况，即，当系统睡眠时，USB 3.1 Gen 2 口若连接有设备，唤醒后，会出现类似下述报错， 对应 kworker 进入 D state ，在这个状态下，它会一直等待且不会被中断，最明显的表现就是这个 USB 接口无法使用，且 :code:`lsusb` 命令会卡住，无法获取任何信息。并且关机时会卡在最后 Remount / read only... 的位置无法正常关机，同样也会无法正常再次睡眠，应该就是因为内核整个卡住了...

.. code-block:: dmesg

  xhci_hcd 0000:0a:00.0: WARN: xHC restore state timeout
  PM: Device 0000:08:00.0 failed to resume async: error -110
  xhci_hcd 0000:0a:00.0: PCI post-resume error -110!
     …
  udevd[2412]: worker [5384] /devices/pci0000:00/0000:00:01.3/0000:0a:00.0/usb5 is taking a long time
     …
  INFO: task kworker/6:2:2914 blocked for more than 860 seconds.
        Not tainted 5.4.66-gentoo-alpha #25
  "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
  kworker/6:2     D    0  2914      2 0x80004000
  Workqueue: usb_hub_wq hub_event
  Call Trace:
  __schedule+0x2cf/0x740
     …

同时，通过解决这个问题了解到，目前 xHCI 驱动已经兼容了 USB 2.0 和 USB 1.0 设备，除非电脑的主板上有纯粹的 USB 2.0 之类的接口，否则不需要再编译 EHCI/UHCI 驱动进入内核。

还遇到的问题有，

.. admonition:: T/S

  urxvt 下无法切换中文，且会有如下报错：

  .. code-block:: bash

    urxvt: the locale is not supported by Xlib, continuing without locale support.

  排查后发现应该是之前我默认设置了 locale 为 :code:`en_HK.utf8` ，切换到 :code:`en_US.utf8` 后正常。 所以应该就是就是 Xlib 不支持 :code:`en_HK.utf8` .

.. admonition:: T/S

  yubikey 相关问题： 1）无法使用 u2f 功能，每次都无法验证； 2）ykman 获取不到设备信息
  
  1）原因是需要额外的 udev 规则，参阅： https://forums.gentoo.org/viewtopic-p-8504230.html?sid=580f7e5e2cf387e1806d2ec02cc14019 ； 2）则是因为 Gentoo 下默认不会安装 pcsc 驱动，自行安装 :gepkg:`app-crypt/ccid` 即可，同时注意 openrc 用户需在 :file:`/etc/rc.conf` 下添加 :code:`rc_hotplug="pcscd"` .

.. admonition:: T/S

  升级 Plasma 后出现从 SDDM 到 Plasma 加载时间变长的问题

  删除 :file:`~/.Xauthority` 文件重新登录后，有所改善。咱也只不知道为啥...

.. admonition:: T/S

  NextCloud 每次开启会提示 Changes In Synchronized Folders Not Being Tracked Reliably. 并告知某些文件不会立马被同步，可能会每 2 个小时同步一次。

  原因是因为 Gentoo-Sources 这个内核默认写的 :code:`INOTIFY_WATCHES` 只有 8192，这个无法在内核下配置，但是可以开机后修改，可以手动配置，如下：

在 :file:`/etc/sysctl.d/99local.conf` 下添加：

.. code-block:: ini

  fs.inotify.max_user_instances = 512
  fs.inotify.max_user_watches = 524288

这里同时修改了 max_user_instances 的值，因为默认只有 128，默认配置的位置在 :file:`linux/fs/notify/inotify/inotify_user.c`

之后每次开机后会自动应用，当前可执行如下命令立即生效：

.. code-block:: bash

  sysctl --system

备份 LUKS 加密头
----------------------------------------------------

整个系统配置完成后，在进行日常使用时一定要做的就是备份好 LUKS 硬盘加密的加密头信息以及钥匙槽，否则当加密头信息损坏就将永远失去对硬盘信息的访问权限：

.. code-block:: bash

  cryptsetup luksHeaderBackup /dev/<未解锁时的设备块> --header-backup-file <file>

然后可以给备份的头文件做加密后永久性保存，参考 `Cryptsetup wiki`_ 。

LUKS 磁盘上的数据是通过一个主密钥加密和解密的，而这个主密钥存储在加密头内；所以即使修改了当前的加密头内解锁主密钥的密码，备份过的加密头依旧可以使用原密码来解锁主密钥并进一步解锁磁盘上的数据，除非对整个磁盘重新进行加密——即替换主密钥。

值得注意的是，在恢复备用的加密头之前，一定要先测试加密头是否匹配。

配置休眠计算机
----------------------------------------------------

我的文件系统是 BtrFS，且我未配置任何 swap 分区，所以休眠功能需要依赖于 swap 文件，在 BtrFS 下创建 swap 文件依赖于如下命令：

.. code-block:: bash

  truncate -s 0 /swapfile
  chattr +C /swapfile
  btrfs property set /swapfile compression none 
  dd if=/dev/zero of=/swapfile bs=1M count=327688 status=progress
  swapon /swapfile

这样子创建了一个 32G 的 swap ，配置到 fstab 下就不说了。在这里需要解决的问题是如何从这个文件中恢复休眠的系统。

显示需要获取这个文件在对应分区下的偏移量，而 BtrFS 还有别于其他文件系统，不能使用 :code:`filefrag` 命令获取，需要其他工具；在 `ArchLinux Wiki 上`_ ，列出了这么一个工具可以用于获取，也同时说明了如何配置。即： 
 
.. code-block:: bash

  ./btrfs_map_physical /swapfile # 获取返回的第一行偏移量数据 OFFSET
  bc <<< "scale=3;<OFFSET> / $(getconf PAGESIZE)" # 即获取到了需要写入 Grub 的偏移量数据
  findmnt -no UUID -T /swapfile # 获取此 swap 文件对应分区的 UUID

然后配置 Grub，修改如下项：

.. code-block:: bash

  GRUB_CMDLINE_LINUX_DEFAULT="resume=UUID=<UUID> resume_offset=<CalOFFSET>"

这里没有遇到什么坑，只是需要注意，配置完成后，因为当前运行的内核并没有获取到这一数据，所以需要重新启动完成后，才可以正常休眠。

美化 Grub
----------------------------------------------------

这里直接使用现成的主题做修改，详细自行搜索即可，非常简单。不过这里遇到过一个问题：

.. admonition:: T/S

  修改现有 grub 主题替换自定义背景图后（保持了文件名一致），开机却提示 :code:`error: invalid argument` ，然后会进入默认主题。

  排查后发现是因为默认生成了 Progressive JPEG 格式，当替换成 Baseline JPEG 格式后报错消失一切正常，所以应该是 grub 不支持 Progressive JPEG 格式。

开启开机动画？
----------------------------------------------------

本来我是想开启开机动画的，搜索后发现可以使用 plymouth 这个软件，有很多现成的主题， KDE 的 Breeze 主题还存在于 Gentoo 官方仓库下。具体启用步骤主要如下几点：

* 内核下关闭启动 Logo 的显示
* 内核下关闭旧的 Framebuffer 配置
* 内核下开启显卡的 KMS 配置
* 生成支持 Plymouth 的 initramfs
* 配置 grub 启动参数
* 美化 Plymouth 主题
* 配置过渡效果

内核的配置直接看 `Gentoo Wiki`_ ；主要想说一下生成支持 Plymouth 的 initramfs

Gentoo 下默认的也是推荐的 initramfs 生成工具 genkernel 并不支持 Plymouth，虽然之前有一个 genkernel-next 是支持的，但是现在已经不再维护且被 Gentoo 放弃；而目前 Gentoo 下可用的支持 Plymouht 的 initramfs 生成工具只有 dracut. 基本无需配置即可使用，它会自动识别当前系统下安装的程序，然后添加到其生成的 initramfs 中，只要一条命令：

.. code-block:: bash

  dracut --force --hostonly

则会自动在 :file:`/boot` 目录下生成并覆盖原有文件。至于 grub 的启动参数，主要就是如下两个：

.. code-block:: bash

  GRUB_GFXMODE=1920x1200x32,auto
  GRUB_GFXPAYLOAD_LINUX=keep

前者配置一个适合自己屏幕的分辨率和色彩深度，并给一个额外的可选自动配置项；后者告诉内核维持当前的分辨率。然后对于测试成功后即可以配置适合此分辨率的 Plymouth 的主题了。

但我在这里却遇到一个问题，当我在系统内测试一切正常后，却在开机后发现， Plymouth 的 two-step 模块配置下，开机无法显示配置好的开机提示文字，反复测试后确定是 dracut 的问题，且工具在系统明明没有 systemd 的情况下，开机依旧去调用 systemd 相关服务，最后放弃这个工具，那么在 Gentoo 下可能就需要去手动创建 initramfs 以完美支持，不像 Arch Linux 的 mkinitcpio 脚本本身就支持；且 Gentoo 下也没有针对 Plymouth 配有过渡效果的工具包.. 而在没有过渡效果的清空下，开关机体验还是很差的，所以我放弃了这个功能，至少目前。

.. admonition:: T/S

  在尝试过程中遇到过一个问题： 在 Plymouth 的 [boot-up] / [shutdown] 等过程中设置 Title/SubTitle 属性无效的问题。

  查了源码的 commit 记录后发现，当前打包的 0.9.5 版本，依旧还是使用 :code:`_Title` 而不是 :code:`Title` 名来获取该属性，所以需要前缀一个 :code:`_` 符号。

-O3 的尝试
----------------------------------------------------

默认情况下，使用 -O2 来优化 gcc 的编译，而 -O3 会进一步优化编译的二进制文件，使之可以使用 AVX 指令集及 YMM 寄存器。但这不是官方推荐的选项，因为在这个选项下会明显消耗更多的内存，并且使二进制文件更大，而且已知一些包会因为这个选项而编译失败，也并不一定能提升编译后的二进制文件的执行性能，这个非常依赖于代码本身的质量。我现在是使用的 -O3，至于效果如何看长期吧，相对于 -O2 的区别，可以看到的是二进制文件确实变大了一点，但也就只有一点，比如 FireFox 的库目录 从 183M 变成了 189M，运行时的内存目前也没发现明显的区别，当然性能也没有非常直观的体现... 先用着

杂七杂八
----------------------------------------------------

.. code-block:: bash

  # 配置当前 CPU 支持的所有指令集
  echo "*/* $(cpuid2cpuflags)" > /etc/portage/package.use/00cpu-flags

  # 查看一系列 emerge 下编译时间用时
  sed -E '/>>>\s+emerge/bd;/:::/bd;/[0-9]+:\s.+$/d;:d;' e.log | sed -E '/:::/bn;N;s/\n/ /;:n;s/([0-9]{10}):\s+>>>\s+emerge\s*\([0-9of ]+\)\s+([A-Za-z0-9_\+\.\/\-]+)\s+[a-z\/ ]+([0-9]{10}):.*/\1 \3 \2/' | awk -F' ' '{printf $2-$1" "$3"\n"}' | sort -n | less

配置双启不打算配置了，目前直接 :kbd:`F2` 进 BIOS 下选择 Windows 的 UEFI 启动很方便，而且基本不用 Windows

1950X 可以支持 NUMA ， BIOS 下启用它以缩短编译时间， ZENITH EXTREME ALPHA 的 BIOS V2101 对应设置为 memory interleaving 改为 channel 以启用。当然，内核下也要配置开启。

使用 Gentoo 是一个长期的过程，之后遇到的问题以及如何解决我也会继续更新，现在就暂时这样。

TODO:

* pay attention to IT8665E driver and look for an other way to get fan speed and other data
* compare the power consumption between Gentoo and Windows and tuning
* compare the performance between AVX YMM and SSE XMM (-O3 or -O2)
* others


.. _`官方的 wiki`: https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/About
.. _`镜像站点`: https://www.gentoo.org/downloads/mirrors/#CN
.. _`清华的 TUNA 源`: https://mirrors.tuna.tsinghua.edu.cn/gentoo/releases/amd64/autobuilds/current-install-amd64-minimal/
.. _`公钥`: https://www.gentoo.org/downloads/signatures/
.. _`原文`: https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Kernel
.. _`内核配置文档翻译`: http://www.jinbuguo.com/kernel/longterm-linux-kernel-options.html
.. _`我的内核配置文件`: /mis/config-5.4.66-gentoo-alpha.txt
.. _`AwesomeWMLikeKDEShortcuts&CorrespondingScripts`: https://github.com/Bekcpear/AwesomeWM-Like-KDE-Shortcuts
.. _`官方维基`: https://wiki.gentoo.org/wiki/KDE
.. _`Cryptsetup wiki`: https://gitlab.com/cryptsetup/cryptsetup/-/wikis/FrequentlyAskedQuestions#6-backup-and-data-recovery
.. _`Gentoo Wiki`: https://wiki.gentoo.org/wiki/Plymouth#Kernel
.. _`ArchLinux Wiki 上`: https://wiki.archlinux.org/index.php/Power_management/Suspend_and_hibernate#Hibernation_into_swap_file_on_Btrfs