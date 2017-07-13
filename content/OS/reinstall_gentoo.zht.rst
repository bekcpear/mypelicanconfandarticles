==============================
重新安裝Gentoo Linux
==============================

:slug: reinstall_gentoo
:lang: zht
:date: 2016-05-22 23:24
:modified: 2016-05-29 13:56
:tags: gentoo, installation
:description: 安裝 Gentoo Linux 的最主要步驟，以方便參考。完整的步驟還是應該去看官方的 wiki。

.. contents::

可能是因為運行了某A開頭VPN的Linux客戶端安裝指令碼，加上@world更新以及核心重新配置，導致系統徹底崩潰，試了很多方法無果，乾脆重新安裝，也好重新整理。

寫在前面
============================================================

Gentoo和一般的Linux的發行版的對比就是Gentoo從一開始安裝到最後的完善都需要自己慢慢配置，所有的內容都可以很方便地定製與個性化（從核心到桌面以及各種管理軟體）。剛剛安裝好的Gentoo佔用的容量在900M左右，是一個非常非常低的佔用量（當然也是因為沒有龐大的桌面環境造成的，但是這對於需要輕量級視窗管理器Awesome的我來說再適合不過了）。 `About Gentoo`_

本文主旨在於為自己整理一下以備不時之需，同時也希望有網友可以用於參考（但是要裝Gentoo的大部分都會自己去看 `官方的wiki`_ 吧=。=）。文件會盡量詳細，但是也不會顯得很傻冒。

**安裝順序是怎樣的呢？** （ `Gentoo Wiki原文翻譯`_ ）

Gentoo的安裝可以被看作是10個步驟，我會下後文一一說明，每一步驟完成後都有對應的一個狀態：

::

  步驟    完成狀態

    1   我們進入了一個可以安裝Gentoo的工作環境（livecd）
    2   Live CD 環境已經可以連結網際網路絡
    3	  準備好了對應的磁碟空間用於存放系統檔案（分割槽、格式化）
    4	  一個最初的Gentoo系統環境已經出現，我們可以使用chroot命令進入這個環境做後續的配置
    5	  完成了Gentoo基本系統的配置
    6	  配置並安裝好了Linux核心
    7	  我們配置好了系統的大部分配置檔案
    8	  必要的系統工具已經安裝好
    9	  安裝並配置好了正確的載入程式（Boot Loader）
   10	  一個非常新鮮的Gentoo系統已經被安裝好等待檢驗啦~

正文
============================================================

準備：一個好的U盤、網際網路絡、一臺可控制的主機、也許你還需要一個正常使用的主機（Windows、Mac、類UNIX 皆可）

製作U盤啟動
------------------------------------------------------------

**首選需要一個最小化安裝的CD檔案**，可以從Gentoo的 `映象站點`_ 獲取適合的，可以通過以下四個步驟挑選、下載需要的檔案：

* 開啟releases/ 資料夾
* 選擇相應的計算機架構（比如 amd64/）
* 開啟autobuilds/資料夾
* 針對amd64和x86架構的話分別選擇current-install-amd64-minimal/ 或者current-install-x86-minimal/資料夾，所有其他的架構請選擇current-iso/資料夾，開啟資料夾後下載：install-<計算機架構>-minimal-<釋出時間>.iso

::

  e.g.:目錄/gentoo/releases/amd64/autobuilds/current-install-amd64-minimal/
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

**校驗下載好的檔案（可選步驟）**

對於那些有強迫症的朋友，當然務必校驗啦。誰知道在下載過程個會不會被別人做了修改之類的。無法進入安裝環境還是小問題，萬一被掛馬了... 概率很小啦~

.DIGESTS這個是用來校驗iso檔案的，而.DIGESTS.asc是用來校驗.DIGESTS檔案是否被篡改的。

我就比較懶了，直接生成iso為hash和.DIGESTS下的數值比較一下，無礙就直接安裝了（最主要的一個校驗的包稍後會說）。

一致即可，如果需要做完整驗證，請移步：https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Media#Microsoft_Windows_based_verification

 
**然後可以開始製作U盤/光碟的啟動盤了** （也就是最基本的安裝環境），

我說一下我的方法：我先在Windows上載入了一個虛擬機器（Virtual Box），直接使用的這個LiveCD（install-amd64-minimal-20160317.iso）載入執行的，然後建立了一個分割槽臨時儲存內容，通過U盤將我的檔案複製到了虛擬機器的分割槽下，然後使用dd命令將install-amd64-minimal-20160317.iso刻錄到了U盤上，

.. code-block:: shell-session

  dd if=/mnt/install-amd64-minimal-20160317.iso of=/dev/sdb/

當然我相信Windows上肯定也是有相關的方法的，比如UltraISO，但是我卻沒有成功，也不想多折騰。

另外官方的wiki說明的是燒錄cd光碟，對於我這種向來不知光碟機為何物的人來說。out

等待dd命令結束，U盤啟動盤就製作完成了。

啟動進入U盤啟動盤並確認網路
------------------------------------------------------------

如果啟動U盤我就不多說了。根據機器不同，一般是開機後反覆敲擊F1、F2、F12等選擇U盤啟動。

啟動U盤後，會提示選擇什麼核心啟動，一般輸入gentoo回車即可，再次進過鍵盤佈局的選擇後我們來到了livecd的環境下，首先看一下目前我的磁碟分配情況：

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

sda即我的主硬碟，那麼多分割槽就是之前的系統用的，sdb為剛剛製作好的U盤啟動盤，而loop0...額...

livecd預設dhcp服務開啟的，直接獲取網路訪問許可權，開始下一步。

分割槽
------------------------------------------------------------

我這次準備使用btrfs的分割槽格式，同樣還是GPT分割槽表 UEFI、Grub2引導。使用btrfs的原因是：1.更加合適SSD，可以提高SSD的壽命且獨有的Subvolumes非常適合我這樣子對分割槽大小總是無法確定的人類。雖然技術還不穩定，個人用用無礙啦，還可以學習學習。

UEFI分割槽表的話，一般使用parted工具，下面直接列操作（輸入的內容加粗顯示）：

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

到這個位置，就已經準備好了磁碟和分割槽了。

獲取基本的系統檔案
------------------------------------------------------------

.. code-block:: shell-session

  livecd gentoo # date
  Mon Apr 11 00:24:46 UTC 2016
  livecd gentoo # cd /mnt/gentoo/
  livecd gentoo # links https://www.gentoo.org/downloads/mirrors/
  # 下載stage3包，選擇映象站點後，在releases/amd64/autobuilds/目錄下
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
  # x是解壓，v輸入詳細資訊，j表示壓縮格式為bzip2，p為了保證許可權設定不被更改，f表示需要解壓成檔案，而不是輸出顯示。xattrs為了使解壓的檔案的其他附加屬性也得到保留。

上面獲取了基本的系統檔案，下面要針對本機配置一下編譯環境。

開啟/mnt/gentoo/etc/portage/make.conf檔案，簡單編輯常用的選項（語法：VARIABLE="content"）：

CFLAGS/CXXFLAGS，主要是為了優化gcc/C 編譯

* -march= / -mtune= ：計算機的架構，一般使用native告知編譯針對本機。
* -O ：gcc優化的標籤，s優化大小，0不做優化，1、2、3優化編譯速度，一般使用-O2
* -pipe ：佔用更多的記憶體，避免編譯時出現碰撞現象而使用管道代替臨時檔案，記憶體大的話，建議開啟
* -fomit-frame-pointer ：具體這個不太瞭解，大致意思就是釋放多餘的指標，但是對於debug有負面影響

::

  CFLAGS="-march=native -O2 -pipe"
  # Use the same settings for both variables
  CXXFLAGS="${CFLAGS}"

MAKEOPTS，這個決定了每次並行執行幾個編譯程序，一般是CPU的個數 1

::

  MAKEOPTS="-j2"

其他的暫時不需要修改。

安裝環境完成，可以chroot後開始安裝基本的系統了。

安裝基本的系統
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
  # 這裡可以選擇你需要安裝的系統型別，eselect profile set [number]
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
  # vim不是自帶的編輯器，自帶的是nano，用法 nano -w [file]，為了節約編譯時間，建立/etc/portage/package.use/vim檔案，寫入app-editors/vim minimal
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

至此，單單系統檔案就已經配置好了，接下來我們需要配置核心

核心配置
------------------------------------------------------------

.. code-block:: shell-session

  (chroot) livecd / # emerge --ask sys-kernel/gentoo-sources
  ...
  ...
  (chroot) livecd / # emerge --ask sys-apps/pciutils
  (chroot) livecd / # emerge --ask sys-apps/usbutils
  (chroot) livecd / # cd /usr/src/linux
  (chroot) livecd linux # make menuconfig

這個非常複雜，需要啟用你知道的所有的硬體裝置，可能一次配置還配置不好。通過lspci、lsusb 命令來先看看機器的硬體情況。 主要幾個內容（詳細的看 `原文`_ ）：

* CPU電源管理
* EFI、GPT支援
* 分割槽格式支援
* USB驅動、網絡卡驅動、音效卡驅動、顯示卡驅動

不多說，我也不是很懂，詳細的配置還是google之，但是知道開啟儘量少的模組可以加速啟動。

.. code-block:: shell-session

  (chroot) livecd linux # make && make modules_install
  ...
  ...
  (chroot) livecd linux # make install
  sh ./arch/x86/boot/install.sh 4.1.15-gentoo-r1 arch/x86/boot/bzImage 
   System.map "/boot"

核心這一部分，寫的很少。實在是因為需要的內容太多，後續有機會單獨整理吧。

配置系統
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

安裝系統工具
------------------------------------------------------------

我就簡單例舉了幾個，有需要的等待開機後再安裝不遲

.. code-block:: shell-session

  (chroot) livecd linux # emerge --ask app-admin/sysklogd
  (chroot) livecd linux # rc-update add sysklogd default
  * service sysklogd added to runlevel default
  (chroot) livecd linux # rc-update add sshd default
  * service sshd added to runlevel default
  (chroot) livecd linux #

配置系統引導
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
  ---某些特定的主機板有必須要讓efi以這個名稱存在固定的位置，比如我的渣渣主機板就是這個樣子的---
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

至此，成功啟動。

下面就是安裝顯示卡驅動，安裝我的awesome視窗管理器，等等配置了。

.. _`About Gentoo`: https://www.gentoo.org/get-started/about/
.. _`官方的wiki`: https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/About
.. _`Gentoo Wiki原文翻譯`: https://wiki.gentoo.org/wiki/Handbook:AMD64/Full/Installation#How_the_installation_is_structured
.. _`映象站點`: https://www.gentoo.org/downloads/mirrors/
.. _`原文`: https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Kernel
