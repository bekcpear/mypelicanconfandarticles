==============================
重新安装Gentoo Linux
==============================

:slug: reinstall_gentoo
:lang: zh
:date: 2016-05-22 23:24
:modified: 2016-05-29 13:56
:tags: gentoo, installation
:description: 安装 Gentoo Linux 的最主要步骤，以方便参考。完整的步骤还是应该去看官方的 wiki。

.. contents::

可能是因为运行了某A开头VPN的Linux客户端安装脚本，加上@world更新以及内核重新配置，导致系统彻底崩溃，试了很多方法无果，干脆重新安装，也好重新整理。

写在前面
============================================================

Gentoo和一般的Linux的发行版的对比就是Gentoo从一开始安装到最后的完善都需要自己慢慢配置，所有的内容都可以很方便地定制与个性化（从内核到桌面以及各种管理软件）。刚刚安装好的Gentoo占用的容量在900M左右，是一个非常非常低的占用量（当然也是因为没有庞大的桌面环境造成的，但是这对于需要轻量级窗口管理器Awesome的我来说再适合不过了）。 `About Gentoo`_

本文主旨在于为自己整理一下以备不时之需，同时也希望有网友可以用于参考（但是要装Gentoo的大部分都会自己去看 `官方的wiki`_ 吧=。=）。文档会尽量详细，但是也不会显得很傻冒。

**安装顺序是怎样的呢？** （ `Gentoo Wiki原文翻译`_ ）

Gentoo的安装可以被看作是10个步骤，我会下后文一一说明，每一步骤完成后都有对应的一个状态：

::

  步骤    完成状态

    1   我们进入了一个可以安装Gentoo的工作环境（livecd）
    2   Live CD 环境已经可以链接互联网络
    3	  准备好了对应的磁盘空间用于存放系统文件（分区、格式化）
    4	  一个最初的Gentoo系统环境已经出现，我们可以使用chroot命令进入这个环境做后续的配置
    5	  完成了Gentoo基本系统的配置
    6	  配置并安装好了Linux内核
    7	  我们配置好了系统的大部分配置文件
    8	  必要的系统工具已经安装好
    9	  安装并配置好了正确的引导程序（Boot Loader）
   10	  一个非常新鲜的Gentoo系统已经被安装好等待检验啦~

正文
============================================================

准备：一个好的U盘、互联网络、一台可控制的主机、也许你还需要一个正常使用的主机（Windows、Mac、类UNIX 皆可）

制作U盘启动
------------------------------------------------------------

**首选需要一个最小化安装的CD文件**，可以从Gentoo的 `镜像站点`_ 获取适合的，可以通过以下四个步骤挑选、下载需要的文件：

* 打开releases/ 文件夹
* 选择相应的计算机架构（比如 amd64/）
* 打开autobuilds/文件夹
* 针对amd64和x86架构的话分别选择current-install-amd64-minimal/ 或者current-install-x86-minimal/文件夹，所有其他的架构请选择current-iso/文件夹，打开文件夹后下载：install-<计算机架构>-minimal-<发布时间>.iso

::

  e.g.:目录/gentoo/releases/amd64/autobuilds/current-install-amd64-minimal/
  ../
  hardened/                                            18-Mar-2016 17:55 -
  install-amd64-minimal-20160317.iso                   18-Mar-2016 14:16 256M
  install-amd64-minimal-20160317.iso.CONTENTS          18-Mar-2016 14:16 3086
  install-amd64-minimal-20160317.iso.DIGESTS           18-Mar-2016 14:16 740
  install-amd64-minimal-20160317.iso.DIGESTS.asc       18-Mar-2016 17:55 1608
  stage3-amd64-20160317.tar.bz2                        18-Mar-2016 14:16 239M
  stage3-amd64-20160317.tar.bz2.CONTENTS               18-Mar-2016 14:16 5M
  stage3-amd64-20160317.tar.bz2.DIGESTS                18-Mar-2016 14:16 720
  stage3-amd64-20160317.tar.bz2.DIGESTS.asc            18-Mar-2016 17:55 1588

**校验下载好的文件（可选步骤）**

对于那些有强迫症的朋友，当然务必校验啦。谁知道在下载过程个会不会被别人做了修改之类的。无法进入安装环境还是小问题，万一被挂马了... 概率很小啦~

.DIGESTS这个是用来校验iso文件的，而.DIGESTS.asc是用来校验.DIGESTS文件是否被篡改的。

我就比较懒了，直接生成iso为hash和.DIGESTS下的数值比较一下，无碍就直接安装了（最主要的一个校验的包稍后会说）。

一致即可，如果需要做完整验证，请移步：https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Media#Microsoft_Windows_based_verification

 
**然后可以开始制作U盘/光盘的启动盘了** （也就是最基本的安装环境），

我说一下我的方法：我先在Windows上加载了一个虚拟机（Virtual Box），直接使用的这个LiveCD（install-amd64-minimal-20160317.iso）加载运行的，然后创建了一个分区临时保存内容，通过U盘将我的文件复制到了虚拟机的分区下，然后使用dd命令将install-amd64-minimal-20160317.iso刻录到了U盘上，

.. code-block:: shell-session

  dd if=/mnt/install-amd64-minimal-20160317.iso of=/dev/sdb/

当然我相信Windows上肯定也是有相关的方法的，比如UltraISO，但是我却没有成功，也不想多折腾。

另外官方的wiki说明的是刻录cd光盘，对于我这种向来不知光驱为何物的人来说。out

等待dd命令结束，U盘启动盘就制作完成了。

启动进入U盘启动盘并确认网络
------------------------------------------------------------

如果启动U盘我就不多说了。根据机器不同，一般是开机后反复敲击F1、F2、F12等选择U盘启动。

启动U盘后，会提示选择什么内核启动，一般输入gentoo回车即可，再次进过键盘布局的选择后我们来到了livecd的环境下，首先看一下目前我的磁盘分配情况：

.. code-block:: shell-session

  livecd ~ # lsblk
  NAME  MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
  sda     8:0   0  223.6G  0 disk
  |-sda1  8:1   0      2M  0 part
  |-sda2  8:2   0    128M  0 part
  |-sda3  8:3   0     20G  0 part
  |-sda4  8:4   0    100G  0 part
  `-sda5  8:5   0  103.5G  0 part
  sdb     8:16  1   29.1G  0 disk
  `-sdb1  8:17  1    256M  0 part /mnt/cdrom
  loop0   7:0   0  224.6M  1 loop /mnt/livecd

sda即我的主硬盘，那么多分区就是之前的系统用的，sdb为刚刚制作好的U盘启动盘，而loop0...额...

livecd默认dhcp服务开启的，直接获取网络访问权限，开始下一步。

分区
------------------------------------------------------------

我这次准备使用btrfs的分区格式，同样还是GPT分区表 UEFI、Grub2引导。使用btrfs的原因是：1.更加合适SSD，可以提高SSD的寿命且独有的Subvolumes非常适合我这样子对分区大小总是无法确定的人类。虽然技术还不稳定，个人用用无碍啦，还可以学习学习。

UEFI分区表的话，一般使用parted工具，下面直接列操作（输入的内容加粗显示）：

.. code-block:: shell-session

  livecd ~ # parted /dev/sda
  GNU Parted 3.2
  Using /dev/sda
  Welcome to GNU Parted! Type 'help' to view a list of commands.
  (parted) unit mib
  (parted) print
  Model: ATA INTEL SSDSC2BP24 (scsi)
  Disk /dev/sda: 228937MiB
  Sector size (logical/physical): 512B/512B
  Partition Table: gpt
  Disk Flags:

  Number  Start      End        Size       File system  Name    Flags
  1      1.00MiB    3.00MiB    2.00MiB    fat32        grub    bios_grub
  2      3.00MiB    131MiB     128MiB     fat32        boot    boot, esp
  3      131MiB     20611MiB   20480MiB   ext4         rootfs
  4      20612MiB   123012MiB  102400MiB  ext4         home
  5      123013MiB  228936MiB  105923MiB  ext4         vm

  (parted) mklabel gpt
  Warning: The existing disk label on /dev/sda will be destroyed and all data on this disk will be lost. Do you want
  to continue?
  Yes/No? yes
  (parted) print
  Model: ATA INTEL SSDSC2BP24 (scsi)
  Disk /dev/sda: 228937MiB
  Sector size (logical/physical): 512B/512B
  Partition Table: gpt
  Disk Flags:

  Number Start End Size File system Name Flags

  (parted) mkpart primary 1 3
  (parted) name 1 grub
  (parted) set 1 bios_grub on
  (parted) mkpart primary 3 131
  (parted) name 2 boot
  (parted) set 2 boot on
  (parted) mkpart primary 131 123011
  (parted) name 3 gentoo
  (parted) mkpart primary 123011 -1
  (parted) name 4 vms
  (parted) print
  Model: ATA INTEL SSDSC2BP24 (scsi)
  Disk /dev/sda: 228937MiB
  Sector size (logical/physical): 512B/512B
  Partition Table: gpt
  Disk Flags:

  Number  Start      End        Size       File system  Name    Flags
  1      1.00MiB    3.00MiB    2.00MiB                 grub    bios_grub
  2      3.00MiB    131MiB     128MiB                  boot    boot, esp
  3      131MiB     123011MiB  122880MiB               gentoo
  4      123011MiB  228936MiB  105925MiB               vms

  (parted) quit
  livecd ~ # mkfs.vfat -F 32 /dev/sda2
  mkfs.fat 3.0.28 (2015-05-16)
  livecd ~ # mkfs.btrfs -f /dev/sda3
  Detected a SSD, turning off metadata duplication. Mkfs with -m dup if you want to force metadata duplication.
  btrfs-progs v4.0.1
  See http://btrfs.wiki.kernel.org for more information.

  Performing full device TRIM (120.00GiB) ...
  Turning ON incompat feature 'extref': increased hardlink limit per file to 65536
  Turning ON incompat feature 'skinny-metadata': reduced-size metadata extent refs
  fs created label (null) on /dev/sda3
  nodesize 16384 leafsize 16384 sectorsize 4096 size 120.00GiB
  livecd ~ # mkfs.btrfs -f /dev/sda4
  Detected a SSD, turning off metadata duplication. Mkfs with -m dup if you want to force metadata duplication.
  btrfs-progs v4.0.1
  See http://btrfs.wiki.kernel.org for more information.

  Performing full device TRIM (103.44GiB) ...
  Turning ON incompat feature 'extref': increased hardlink limit per file to 65536
  Turning ON incompat feature 'skinny-metadata': reduced-size metadata extent refs
  fs created label (null) on /dev/sda4
  nodesize 16384 leafsize 16384 sectorsize 4096 size 103.44GiB
  livecd ~ # parted /dev/sda print
  Model: ATA INTEL SSDSC2BP24 (scsi)
  Disk /dev/sda: 240GB
  Sector size (logical/physical): 512B/512B
  Partition Table: gpt
  Disk Flags:

  Number  Start   End     Size    File system  Name    Flags
  1      1049kB  3146kB  2097kB  fat32        grub    bios_grub
  2      3146kB  137MB   134MB   fat32        boot    boot, esp
  3      137MB   129GB   129GB   btrfs        gentoo
  4      129GB   240GB   111GB   btrfs        vms

  livecd ~ # mount /dev/sda3 /mnt/gentoo

到这个位置，就已经准备好了磁盘和分区了。

获取基本的系统文件
------------------------------------------------------------

.. code-block:: shell-session

  livecd gentoo # date
  Mon Apr 11 00:24:46 UTC 2016
  livecd gentoo # cd /mnt/gentoo/
  livecd gentoo # links https://www.gentoo.org/downloads/mirrors/
  # 下载stage3包，选择镜像站点后，在releases/amd64/autobuilds/目录下
  livecd gentoo # gpg --keyserver hkps.pool.sks-keyservers.net --recv-keys 0xBB572E0E2D182910
  gpg: keyring `/root/.gnupg/secring.gpg' created
  gpg: requesting key 2D182910 from hkp server hkps.pool.sks-keyservers.net
  gpg: /root/.gnupg/trustdb.gpg: trustdb created
  gpg: key 2D182910: public key "Gentoo Linux Release Engineering (Automated Weekly Release Key) <releng@gentoo.org>" imported
  gpg: no ultimately trusted keys found
  gpg: Total number processed: 1
  gpg: imported: 1 (RSA: 1)
  livecd gentoo # gpg --verify stage3-amd64-20160407.tar.bz2.DIGESTS.asc gpg: Signature made Fri Apr 8 08:41:03 2016 UTC using RSA key ID 2D182910
  gpg: Good signature from "Gentoo Linux Release Engineering (Automated Weekly Release Key) <releng@gentoo.org>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg: There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 13EB BDBE DE7A 1277 5DFD B1BA BB57 2E0E 2D18 2910
  gpg: WARNING: not a detached signature; file 'stage3-amd64-20160407.tar.bz2.DIGESTS' was NOT verified!
  # Verify the key on https://www.gentoo.org/downloads/signatures/ ，manually.
  livecd gentoo # grep -A 1 -i sha512 stage3-amd64-20160407.tar.bz2.DIGESTS.asc
  # SHA512 HASH
  adfd313aa0101aae3635a59db99984d9d1c0fc950227db85cb0a12927cde9469bafa469033bca1c8efe48b4e408045c9a84a019d66c1f2177405233be680bd6c stage3-amd64-20160407.tar.bz2
  --
  # SHA512 HASH
  75828af39c6dc448c637edd07adba9e4ab82b9ec445f1987a7c55bf9b36396b596e398087184773dc254ab07d81efab66f8eefec6e562d9ba02134d0dafedf64 stage3-amd64-20160407.tar.bz2.CONTENTS
  livecd gentoo # sha512sum stage3-amd64-20160407.tar.bz2
  adfd313aa0101aae3635a59db99984d9d1c0fc950227db85cb0a12927cde9469bafa469033bca1c8efe48b4e408045c9a84a019d66c1f2177405233be680bd6c stage3-amd64-20160407.tar.bz2
  livecd gentoo # tar xvjpf stage3-*.tar.bz2 --xattrs
  # x是解压，v输入详细信息，j表示压缩格式为bzip2，p为了保证权限设置不被更改，f表示需要解压成文件，而不是输出显示。xattrs为了使解压的文件的其他附加属性也得到保留。

上面获取了基本的系统文件，下面要针对本机配置一下编译环境。

打开/mnt/gentoo/etc/portage/make.conf文件，简单编辑常用的选项（语法：VARIABLE="content"）：

CFLAGS/CXXFLAGS，主要是为了优化gcc/C 编译

* -march= / -mtune= ：计算机的架构，一般使用native告知编译针对本机。
* -O ：gcc优化的标签，s优化大小，0不做优化，1、2、3优化编译速度，一般使用-O2
* -pipe ：占用更多的内存，避免编译时出现碰撞现象而使用管道代替临时文件，内存大的话，建议开启
* -fomit-frame-pointer ：具体这个不太了解，大致意思就是释放多余的指针，但是对于debug有负面影响

::

  CFLAGS="-march=native -O2 -pipe"
  # Use the same settings for both variables
  CXXFLAGS="${CFLAGS}"

MAKEOPTS，这个决定了每次并行运行几个编译进程，一般是CPU的个数 1

::

  MAKEOPTS="-j2"

其他的暂时不需要修改。

安装环境完成，可以chroot后开始安装基本的系统了。

安装基本的系统
------------------------------------------------------------

.. code-block:: shell-session

  livecd gentoo # mirrorselect -i -o >> /mnt/gentoo/etc/portage/make.conf
  * Using url: https://api.gentoo.org/mirrors/distfiles.xml
  * Downloading a list of mirrors...
  Got 154 mirrors.
  ...
  ...
  livecd gentoo # mkdir /mnt/gentoo/etc/portage/repos.conf
  livecd gentoo # cp /mnt/gentoo/usr/share/portage/config/repos.conf /mnt/gentoo/etc/portage/repos.conf/gentoo.conf
  livecd gentoo # cp -L /etc/resolv.conf /mnt/gentoo/etc/
  livecd gentoo # mount -t proc proc /mnt/gentoo/proc
  livecd gentoo # mount --rbind /sys /mnt/gentoo/sys
  livecd gentoo # mount --rbind /dev /mnt/gentoo/dev
  livecd gentoo # chroot /mnt/gentoo /bin/bash
  livecd / # source /etc/profile
  livecd / # export PS1="(chroot) $PS1"
  (chroot) livecd / # emerge-webrsync
  (chroot) livecd / # emerge --sync
  (chroot) livecd / # eselect profile list
  Available profile symlink targets:
  [1] default/linux/amd64/13.0 *
  [2] default/linux/amd64/13.0/selinux
  [3] default/linux/amd64/13.0/desktop
  [4] default/linux/amd64/13.0/desktop/gnome
  [5] default/linux/amd64/13.0/desktop/gnome/systemd
  [6] default/linux/amd64/13.0/desktop/kde
  [7] default/linux/amd64/13.0/desktop/kde/systemd
  [8] default/linux/amd64/13.0/desktop/plasma
  [9] default/linux/amd64/13.0/desktop/plasma/systemd
  [10] default/linux/amd64/13.0/developer
  [11] default/linux/amd64/13.0/no-multilib
  [12] default/linux/amd64/13.0/systemd
  [13] default/linux/amd64/13.0/x32
  [14] hardened/linux/amd64
  [15] hardened/linux/amd64/selinux
  [16] hardened/linux/amd64/no-multilib
  [17] hardened/linux/amd64/no-multilib/selinux
  [18] hardened/linux/amd64/x32
  [19] hardened/linux/musl/amd64
  [20] hardened/linux/musl/amd64/x32
  [21] default/linux/uclibc/amd64
  [22] hardened/linux/uclibc/amd64
  # 这里可以选择你需要安装的系统类型，eselect profile set [number]
  (chroot) livecd / # emerge --ask --update --deep --newuse @world
  (chroot) livecd / # ls /usr/share/zoneinfo
  Africa      Canada   Factory   Iceland    MST7MDT   ROC        Zulu
  America     Chile    GB        Indian     Mexico    ROK        iso3166.tab
  Antarctica  Cuba     GB-Eire   Iran       NZ        Singapore  localtime
  Arctic      EET      GMT       Israel     NZ-CHAT   Turkey     posixrules
  Asia        EST      GMT 0     Jamaica    Navajo    UCT        zone.tab
  Atlantic    EST5EDT  GMT-0     Japan      PRC       US         zone1970.tab
  Australia   Egypt    GMT0      Kwajalein  PST8PDT   UTC
  Brazil      Eire     Greenwich Libya      Pacific   Universal
  CET         Etc      HST       MET        Poland    W-SU
  CST6CDT     Europe   Hongkong  MST        Portugal  WET
  (chroot) livecd / # ls /usr/share/zoneinfo/Asia/Shanghai
  /usr/share/zoneinfo/Asia/Shanghai
  (chroot) livecd / # echo "Asia/Shanghai" > /etc/timezone
  (chroot) livecd / # emerge --config sys-libs/timezone-data


  Configuring pkg...

  * Updating /etc/localtime with /usr/share/zoneinfo/Asia/Shanghai

  (chroot) livecd / # vim /etc/locale.gen
  # vim不是自带的编辑器，自带的是nano，用法 nano -w [file]，为了节约编译时间，创建/etc/portage/package.use/vim文件，写入app-editors/vim minimal
  (chroot) livecd / # locale-gen
  * Generating locale-archive: forcing # of jobs to 1
  * Generating 3 locales (this might take a while) with 1 jobs
  * (1/3) Generating en_US.ISO-8859-1 ... [ ok ]
  * (2/3) Generating en_US.UTF-8 ... [ ok ]
  * (3/3) Generating zh_CN.UTF-8 ... [ ok ]
  * Generation complete
  (chroot) livecd / # eselect locale list
  Available targets for the LANG variable:
  [1] C
  [2] POSIX
  [3] en_US
  [4] en_US.iso88591
  [5] en_US.utf8
  [6] zh_CN.utf8
  [ ] (free form)
  (chroot) livecd / # eselect locale set 5
  Setting LANG to en_US.utf8 ...
  Run ". /etc/profile" to update the variable in your shell.
  (chroot) livecd / # cat /etc/env.d/02locale
  # Configuration file for eselect
  # This file has been automatically generated.
  LANG="en_US.utf8"
  (chroot) livecd / # env-update && source /etc/profile && export PS1="(chroot) $PS1"
  >>> Regenerating /etc/ld.so.cache...
  (chroot) livecd / #

至此，单单系统文件就已经配置好了，接下来我们需要配置内核

内核配置
------------------------------------------------------------

.. code-block:: shell-session

  (chroot) livecd / # emerge --ask sys-kernel/gentoo-sources
  ...
  ...
  (chroot) livecd / # emerge --ask sys-apps/pciutils
  (chroot) livecd / # emerge --ask sys-apps/usbutils
  (chroot) livecd / # cd /usr/src/linux
  (chroot) livecd linux # make menuconfig

这个非常复杂，需要启用你知道的所有的硬件设备，可能一次配置还配置不好。通过lspci、lsusb 命令来先看看机器的硬件情况。 主要几个内容（详细的看 `原文`_ ）：

* CPU电源管理
* EFI、GPT支持
* 分区格式支持
* USB驱动、网卡驱动、声卡驱动、显卡驱动

不多说，我也不是很懂，详细的配置还是google之，但是知道开启尽量少的模块可以加速启动。

.. code-block:: shell-session

  (chroot) livecd linux # make && make modules_install
  ...
  ...
  (chroot) livecd linux # make install
  sh ./arch/x86/boot/install.sh 4.1.15-gentoo-r1 arch/x86/boot/bzImage 
   System.map "/boot"

内核这一部分，写的很少。实在是因为需要的内容太多，后续有机会单独整理吧。

配置系统
------------------------------------------------------------

.. code-block:: shell-session

  (chroot) livecd linux # ls /dev/disk/by-uuid/ -l
  total 0
  lrwxrwxrwx 1 root root 10 Apr 11 07:27 2016-02-25-07-00-57-78 -> ../../sdb1
  lrwxrwxrwx 1 root root 10 Apr 11 07:27 C729-3740 -> ../../sda1
  lrwxrwxrwx 1 root root 10 Apr 11 07:27 CAA2-51E6 -> ../../sda2
  lrwxrwxrwx 1 root root 10 Apr 11 07:27 cb8154eb-3cbd-48c2-aa1e-26117aede3a8 -> ../../sda4
  lrwxrwxrwx 1 root root 10 Apr 11 07:27 e0de03bf-b198-4162-9c7e-8250e29c6aab -> ../../sda3
  (chroot) livecd linux # vim /etc/fstab
  ---
  UUID=CAA2-51E6                             /boot/efi/  fat32  defaults,noatime              0 2
  UUID=e0de03bf-b198-4162-9c7e-8250e29c6aab  /           btrfs  defaults,ssd,discard,noatime  0 1
  ---
  (chroot) livecd linux # emerge --ask --noreplace net-misc/netifrc
  (chroot) livecd linux # vim /etc/conf.d/net
  ---
  config_enp0s31f6="192.168.1.199 netmask 255.255.255.0 brd 192.168.1.255"
  routes_enp0s31f6="default via 192.168.1.1"
  ---
  (chroot) livecd linux # cd /etc/init.d
  (chroot) livecd linux # ln -s net.lo net.enp0s31f6
  (chroot) livecd linux # rc-update add net.enp0s31f6 default
  (chroot) livecd linux # passwd
  New password:
  Retype new password:
  passwd: password updated successfully
  (chroot) livecd linux # 

安装系统工具
------------------------------------------------------------

我就简单例举了几个，有需要的等待开机后再安装不迟

.. code-block:: shell-session

  (chroot) livecd linux # emerge --ask app-admin/sysklogd
  (chroot) livecd linux # rc-update add sysklogd default
  * service sysklogd added to runlevel default
  (chroot) livecd linux # rc-update add sshd default
  * service sshd added to runlevel default
  (chroot) livecd linux #

配置系统引导
------------------------------------------------------------

.. code-block:: shell-session

  (chroot) livecd linux # echo GRUB_PLATFORMS="efi-64" >> /etc/portage/make.conf
  (chroot) livecd linux # emerge --ask sys-boot/grub:2
  ...
  ...
  (chroot) livecd linux # mkdir /boot/efi
  (chroot) livecd linux # mount UUID=CAA2-51E6 /boot/efi/
  (chroot) livecd linux # grub2-install --target=x86_64-efi --efi-directory=/boot/efi/ --bootloader-id=grub --boot-directory=/boot/efi/ --debug
  ...
  ...
  (chroot) livecd linux # grub2-mkconfig -o /boot/efi/grub/grub.cfg
  Generating grub configuration file ...
  Found linux image: /boot/vmlinuz-4.1.15-gentoo-r1
  done
  (chroot) livecd linux # mkdir /boot/efi/EFI/boot
  (chroot) livecd linux # cp /boot/efi/EFI/grub/grubx64.efi /boot/efi/EFI/boot/bootx64.efi
  ---某些特定的主板有必须要让efi以这个名称存在固定的位置，比如我的渣渣主板就是这个样子的---
  (chroot) livecd linux # exit
  exit
  livecd gentoo # umount -l /mnt/gentoo/dev{/shm,/pts,}
  livecd gentoo # umount /mnt/gentoo{/boot,/sys,/proc,}
  umount: /mnt/gentoo/boot: not mounted
  umount: /mnt/gentoo/sys: target is busy
  (In some cases useful info about processes that
  use the device is found by lsof(8) or fuser(1).)
  umount: /mnt/gentoo: target is busy
  (In some cases useful info about processes that
  use the device is found by lsof(8) or fuser(1).)
  livecd gentoo # reboot

至此，成功启动。

下面就是安装显卡驱动，安装我的awesome窗口管理器，等等配置了。

.. _`About Gentoo`: https://www.gentoo.org/get-started/about/
.. _`官方的wiki`: https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/About
.. _`Gentoo Wiki原文翻译`: https://wiki.gentoo.org/wiki/Handbook:AMD64/Full/Installation#How_the_installation_is_structured
.. _`镜像站点`: https://www.gentoo.org/downloads/mirrors/
.. _`原文`: https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Kernel
