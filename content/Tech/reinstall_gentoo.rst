=====================================================================================================================
重新安装 Gentoo Linux （硬盘加密， Windows 10 双系统）
=====================================================================================================================

:slug: reinstall_gentoo
:date: 2016-05-22 23:24
:modified: 2020-09-29 00:09
:lang: zh_hans
:tags: gentoo, installation, luks
:description: 安装 Gentoo Linux 的最主要步骤，以方便参考。完整的步骤还是应该去看官方的 wiki。
:color: #463c65
:summary:

.. contents::

:del:`可能是因为运行了某A开头VPN的Linux客户端安装脚本，加上@world更新以及内核重新配置，导致系统彻底崩溃，试了很多方法无果，干脆重新安装，也好重新整理。`

.. PELICAN_BEGIN_SUMMARY

时隔 4 年，我又来装 Gentoo 啦～ 之前换了个台式，平台太新了，怎么都搞不定显卡的驱动，后来就一直笔记本用的 Arch，但是现在笔记本越来越卡.. 于是.. 我又拿台式装 Gentoo 了，台式很牛B， 16 核 32 线程，跑起 Gentoo 肯定很爽～

此次，我是在已有 Windows 10 系统的情况下，用一块额外完整的硬盘安装 Gentoo，并配置双系统引导，同时开启硬盘加密。

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

1. 需要的是这个 .iso 的文件，下载它。（ .CONTENTS.gz 文件是一个文本文件压缩包，该文本内存储了 .iso 文件内所有文件的列表）
2. 下载校验文件， .DIGESTS 文件不带签名，里面存储了 .iso 以及 .CONTENTS.gz 散列值。而 .DIGESTS.asc 是前者的带签名版，直接下载这个。
3. 导入 `公钥`_ 并校验：

.. code-block:: bash

  gpg --keyserver keys.gnupg.net --recv-keys 13EBBDBEDE7A12775DFDB1BABB572E0E2D182910 # 导入对应公钥
  gpg --verify install-amd64-minimal-20200920T214503Z.iso.DIGESTS.asc # 检查文件完整性
  sha512sum install-amd64-minimal-20200920T214503Z.iso # 然后与文件内散列值进行比对验证

制作盘启动盘并进入安装环境
------------------------------------------------------------

校验没问题后就制作 U 盘启动盘， 习惯性使用 :code:`dd` 命令：

.. code-block:: bash

  dd bs=4M if=./install-amd64-minimal-20200920T214503Z.iso of=/dev/sdc status=progress oflag=sync

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

.. pull-quote::
  
  这里遇到一个问题，本以为主板上默认的千兆网卡驱动是被加载的，结果后来发现默认加载的是万兆网卡，所以当发现接口状态怎么都是 DOWN 时，考虑加载的网卡接口不对。这里可以使用 :code:`lspci | grep -i eth` 查看所有网卡接口，然后 :code:`lspci -v -s<slot>` 查看哪些有加载完成驱动。

或者开启 dhcpcd 服务，Gentoo 默认使用 OpenRC，所以可以运行：

.. code-block:: bash

  /etc/init.d/dhcpcd start

启动 dhcpcd 服务。其它方式可以自行查找官方文档，比如无线使用 :code:`iw` 命令， 拨号使用 :code:`pppoe-setup` 和 :code:`pppoe-start` 命令之类的。

测试网络连通后，这个步骤结束。

步骤三： 准备好硬盘
============================================================

因为我打算加密硬盘，所以加密操作也需要在这个步骤完成。也就是在这个步骤，需要确定使用的 BIOS 固件接口及引导程序，做分区，确定选用的文件系统，加密分区/硬盘，格式化，挂载。

因为需要使用双系统引导，所以复用 Windows 的 EFI 分区，使用 UEFI，但是这里还是要留出足够的 EFI 分区空间以备以后单硬盘单系统使用。 :code:`/boot` 分区单分，其它分区完整一个加密盘，所以硬盘的分区结果如下：

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

然后重新挂载子卷到 /mnt/gentoo 下：

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

之后切换到挂载的 gentoo 目录后，解压 stage3：

.. code-block:: bash

  cd /mnt/gentoo
  tar xpvf stage3-*.tar.xz --xattrs-include='*.*' --numeric-owner #解压选项不要漏错

然后要针对本机配置一下编译环境。

打开 etc/portage/make.conf 文件，简单编辑常用的选项（语法： VARIABLE="content" ）：

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

MAKEOPTS，这个决定了每次并行运行几个编译进程，一般是 CPU 的个数/核心数 +1，核心太多的话，也可以适度减少以留出余量运行其它程序。

.. code-block:: bash

  MAKEOPTS="-j28"

其他的暂时不需要修改。

安装环境完成，可以 chroot 后开始安装基本的系统了。

步骤五： 安装基本的系统
============================================================

先选择一个/多个足够快的镜像地址（下载源码用于编译的安装）：

.. code-block:: bash

  mirrorselect -i -o >> /mnt/gentoo/etc/portage/make.conf

选择 163/TUNA 的源就好。然后可以再设定一个更快的 ebuild 资料库同步地址，如需设定，使用一下命令即可：

.. code-block:: bash

  mkdir /mnt/gentoo/etc/portage/repos.conf
  cp /mnt/gentoo/usr/share/portage/config/repos.conf /mnt/gentoo/etc/portage/repos.conf/gentoo.conf

以 TUNA 源 rsync 方式为例，编辑 gentoo.conf 文件，替换

.. code-block:: ini

  sync-uri = rsync://rsync.gentoo.org/gentoo-portage

为

.. code-block:: ini

  sync-uri = rsync://mirrors.tuna.tsinghua.edu.cn/gentoo-portage

不过我觉得少量的同步，采用官方源即可，也可以不替换。且这些以后都可以再改。

设置 DNS 服务器地址，可以直接复制之前配置的：

.. code-block:: bash

  cp -L /etc/resolv.conf /mnt/gentoo/etc/

然后挂载需要的文件系统： :code:`/proc/` 和 :code:`/sys/` 是伪文件系统，记录了 Linux 内核向环境所暴露的信息，后者原打算用于取代前者，输出内容更加结构化。 :code:`/dev/` 则是常规文件系统，部分由 Linux 设备管理器管理，包含了所有的设备文件。 

.. code-block:: bash

  mount --types proc /proc /mnt/gentoo/proc
  mount --rbind /sys /mnt/gentoo/sys
  mount --make-rslave /mnt/gentoo/sys
  mount --rbind /dev /mnt/gentoo/dev
  mount --make-rslave /mnt/gentoo/dev

.. pull-quote::

  安装 systemd 支持一定需要 :code:`--make-rslave` 操作。

现在 chroot 到新的环境下：

.. code-block:: bash

  chroot /mnt/gentoo /bin/bash
  source /etc/profile
  export PS1="(chroot) $PS1"

挂载 /boot 分区用于后续内核及引导的安装：

.. code-block:: bash

  mount /dev/sde1 /mnt/gentoo/boot

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

  emerge --ask --verbose --update --deep --newuse @world

.. pull-quote::

  新系统自带 nano 编辑器，不自带 vim，可以先装一个，习惯使用 vim 的话。

配置 Timezone：

.. code-block:: bash

  ls /usr/share/zoneinfo/Asia/Shanghai
  echo "Asia/Shanghai" > /etc/timezone
  emerge --config sys-libs/timezone-data

配置语言环境（至少一个 UTF-8 编码的）：

.. code-block:: bash

  nano -w /etc/locale.gen # 这里添上需要的语言，支持的语言可以查看 /usr/share/i18n/SUPPORTED 文件
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

  emerge --ask sys-kernel/linux-firmware # 启用下 savedconfig USE

这里可能需要在 :code:`/etc/portage/package.license` 下添加接受许可。

完成之后就可以开始配置编译内核了，有两种方式，一个手动配置，一个使用 :code:`genkernel` 工具来配置。我是选择手动配置的，虽然一开始真的看得整个人都是懵的，不过熟练了就好了。手动配置可以大大减少不需要的模块的安装和编译，也有利于启动速度，还可以后续继续熟悉优化内核配置，且把显卡驱动直接编译进内核后，在输入 LUKS 加密分区的密码时，就已经加载完成显卡驱动，屏幕看得也会舒服很多。

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

这里还是看 `原文`_ ，相对复杂不太好简略说明。配置过程中，善用 :code:`H` 键查看说明，还可以参考金步国的 `内核配置文档翻译`_ ，说是翻译，其实很多都添加了自己的解释，相对官方文档易于理解太多。

配置完成后编译并安装：

.. code-block:: bash

  make -j30 # 数根据实际情况来，如果发现出错，则 make V=1 -j30 2>error.log 后，查看报错信息
  make modules_install && make install
  genkernel --kernel-config=/usr/src/linux/.config initramfs

内核这一部分，写的很少。实在是因为需要的内容太多，后续有机会单独整理吧。在之后的使用过程中，某些程序会需要额外的内核配置，到时候再参考 wiki 操作。

  我目前觉得一个比较好的方式是： 先使用 :code:`genkernel` 工具生成一次内核，然后去修改生成的配置文件，去掉自己明确知道的不用的模块和功能，修改自己明确知道的一定要加载的模块编译进内核（结合使用 :code:`lspci` , :code:`lsmod` , :code:`hwinfo` , :code:`sensors-detect` 命令）。

  目前 `我的内核配置文件`_ ，对应的硬件是： 1950X CPU + Asus ROG ZENITH EXTREME ALPHA 主板 + AMD Vega 64 公版显卡；对应环境是： Gentoo Linux + BtrFS + LUKS2 根分区加密 + GRUB 引导。其中，主要驱动全部编译进内核，删掉了很多确定自己不需要的模块和功能，后续再行优化。

  *有一点要注意的是，参考 Gentoo 官方的 AMDGPU 配置文档，里面的固件列表是不全的，文档也说明了，针对我这块显卡，我直接把 vega 开头的固件全部丢进了... 一开始被坑死了，没仔细看，直接按照上面列出的列表放了，怎么都起不起来。*

关于 Microcode， 我的是 AMD 的 CPU，在全局开启 initramfs USE 的情况下，安装 Linux-Firmware 时，会自动在 :code:`/boot` 目录下，创建一个 amd-uc.img CPIO 格式微码文件，在 initrd 中使用，需要在 initramfs 前加载，具体规则看下方 initramfs 说明链接， :code:`grub-mkconfig` 会自动识别添加。如果是 Intel 的 CPU，则不会创建这个文件，需要手动创建，或者直接编译进内核，或者使用 :code:`genkernel` 命令生成。

  我这个文档的顺序是根据官方文档的顺序来整理的，但是我就觉得，内核配置应该放在引导配置前，毕竟.. 不用 genkernel 的话，大概率配置不好，除非有同样硬件的配置文件直接拿来用，否则放在和引导配置一起，更顺滑。

查的部分一些资料，并不全：

| mcelog 不支持 AMD 的 CPU： :code:`mcelog --help` 输出有支持的芯片组
| DMA Engine 主要支持 Intel 的高端 U，AMD 上没看到有支持的： https://cateee.net/lkddb/web-lkddb/DMADEVICES.html
| initramfs 说明： https://wiki.debian.org/initramfs
| 1950x 是否支持 SME： https://github.com/AMDESE/AMDSEV/issues/1
| 我用不到的 IB 接口： https://en.wikipedia.org/wiki/InfiniBand
| 更新 microcode： https://wiki.gentoo.org/wiki/AMD_microcode
| tsc 报错，或许正常： https://miguelmenendez.pro/en/blog/fast-tsc-calibration-failed/
| 我的 rtc 的驱动名： https://bugs.archlinux.org/task/59824
| 主板传感器芯片 IT8665E 未受支持： https://github.com/lm-sensors/lm-sensors/issues/195
| 某些内核选项需要打开专家模式后才可设置： https://forums.gentoo.org/viewtopic-t-1054448-start-0.html
| PCIE 上又一个报错： https://askubuntu.com/questions/949254/new-system-with-pcie-errors-need-help-debugging
| 无线网卡读取温度报错 bug： https://bugzilla.kernel.org/show_bug.cgi?id=201761
| ata 一个不是 bug 的报错： https://bugzilla.redhat.com/show_bug.cgi?id=653811
| 无线网卡额外固件 regulatory.db 报错： https://forums.gentoo.org/viewtopic-t-1114094-start-0.html 如若编译进内核，这个固件也要一起编译进去

步骤七： 完成系统配置
============================================================

内核配置编译完成后，最麻烦的一步做完了，下面就是需要做最后的系统配置。

先创建 fstab 文件 :code:`/etc/fstab` ，类似如下格式：

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

然后配置网络，这里直接安装 :code:`net-misc/dhcpcd` 自动获取路由器的地址，无线网卡配置等最后再配置。如果仅能使用无线网卡，可以跳到后文去看。

设置硬件时钟 因为是和 Windows 双系统， Windows 写入 BIOS 的是本地时间且不可手动修改，所以需要设置 clock="local" 在 :code:`/etc/conf.d/hwclock`

这里也可以直接配置内核写入，不使用 openrc 的服务，但是两者冲突，需要禁用其中一种，见： https://wiki.gentoo.org/wiki/System_time#In-kernel_method

步骤八： 完成系统工具的安装
============================================================

安装 cryptsetup, cron, 必要的日志工具，文件系统工具，无线网络配置工具等，其实主要就是日志工具和 cryptsetup 工具，其它后面再装一样，不多说了。

.. code-block:: bash

  emerge -av app-admin/sysklogd sys-fs/cryptsetup
  rc-update add sysklogd default

步骤九： 完成系统引导的配置
============================================================

我选用 grub 作为引导程序，因为是 UEFI 固件启动，所以需要设定全局的 grub 参数，并安装 grub：

.. code-block:: bash

  echo GRUB_PLATFORMS="efi-64" >> /etc/portage/make.conf
  emerge -av sys-boot/grub:2

设置参数是为了确保编译安装 grub 的时候，启用 efi 功能。

然后配置下引导选项，主要解密磁盘，在 :code:`/etc/default/grub` 内修改：

.. code-block:: ini

  GRUB_CMDLINE_LINUX="dobtrfs crypt_root=UUID=<uuid> root=UUID=<uuid>"

.. pull-quote::

  这里需要使用 UUID 来识别 root 分区，因为我没找到方法指定打开 LUKS 加密分区后的名字，在 Arch Linux 上可以通过在 crypt_root 参数后加 :code:`:<name>` 来指定，但是 Gentoo 尝试后不行，所以暂时不去理会了。

然后确认挂载完成 :code:`/boot` 和 Windows 复用的 :code:`/boot/efi` 分区后，安装 grub 引导：

.. code-block:: bash

  mount -a
  grub-install --target=x86_64-efi --boot-directory=/boot --efi-directory=/boot/efi/ --bootloader-id=Gentoo --debug
  grub-mkconfig -o /boot/grub/grub.cfg

无报错即安装完成。

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

后面的任务就是添加常用的非 root 用户，配置桌面环境/窗口管理器，安装需要的各类软件，非常简单的 Windows 双启配置。

容我后续更新。

TODO: understand luks tcrypt encryption option


.. _`About Gentoo`: https://www.gentoo.org/get-started/about/
.. _`官方的 wiki`: https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/About
.. _`Gentoo Wiki 原文`: https://wiki.gentoo.org/wiki/Handbook:AMD64/Full/Installation#How_the_installation_is_structured
.. _`镜像站点`: https://www.gentoo.org/downloads/mirrors/
.. _`清华的 TUNA 源`: https://mirrors.tuna.tsinghua.edu.cn/gentoo/releases/amd64/autobuilds/current-install-amd64-minimal/
.. _`公钥`: https://www.gentoo.org/downloads/signatures/
.. _`原文`: https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Kernel
.. _`内核配置文档翻译`: http://www.jinbuguo.com/kernel/longterm-linux-kernel-options.html
.. _`我的内核配置文件`: /mis/config-5.4.66-gentoo-alpha.txt
