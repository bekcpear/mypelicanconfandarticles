======================================================================
Windows10下的UEFI引导流程解析和引导修复说明
======================================================================

:slug: Windows10_UEFI_Boot_Process
:lang: zh
:date: 2016-07-14 11:54
:tags: windows, bootloader, UEFI
:status: draft 
:noindent: true

.. contents::

**翻出来的一篇，有点不确定是否完全正确**

Windows10下EFI分区文件结构(仅说明3个必要文件)：
------------------------------------------------------------------------------------------

::

  (EFI分区)..................此分区必须为Fat32格式，不然UEFI固件将无法识别
  |
  +--EFI
    |--Microsoft
    |  +--Boot
    |     |--bootmgfw.efi...一个针对Windows的efi应用，使Boot Menu界面上的Windows Boot Manager可以工作
    |     +--BCD............启动配置文件，用户编辑启动菜单以及默认的启动顺序等
    |--Boot
        +--bootx64.efi.......一个针对UEFI的统一efi应用，可以针对所有的系统。如果是32位系统，则是boota32.ef

.. PELICAN_END_SUMMARY

引导流程
------------------------------------------------------------------------------------------

::

                                       计算机加电
                                          |
                                        BIOS自检
                                          |
                                      UEFI固件启动
                                          |
                          根据NVRAM下的BootOrder顺序加载启动设备
                                          |
                获取对应启动设备下第一个存有正确efi应用的Fat32格式分区并加载
                                          |
                              读取efi应用信息，加载到BCD文件
                                          |
  读取BCD文件下的记录以加载系统，默认Windows10系统是加载C:\Windows\System32\winload.efi应用
                                          |
                    接下来就交给系统服务了。这样子就完成了系统的启动过程


说明一下：

* 什么叫做根据NVRAM下的BootOrder顺序加载启动设备，这个里面有几个知识点

  1. **NVRAM（非易失性存储器）** 是BIOS用于存储本计算机启动设备信息的载体，可以通过 :code:`bcdedit /enum firmware` 来查看信息，参考 `这个 <https://technet.microsoft.com/zh-cn/library/cc749510(v=ws.10).aspx>`_ 
  2. **BootOrder** 顾名思义就是一个引导顺序，可以在BIOS下调节，比如先引导Windows Boot Manager还是先引导ATA HDD0这个设备

* 什么叫做获取对应启动设备下第一个存有正确efi应用的Fat32格式分区并加载？正常情况来说，一个硬盘分区仅有一个Fat32格式的EFI分区，并且往往是在第一个，但是当出现多了EFI分区那么UEFI固件将如何加载呢？对于首选启动已经设置为了Windows Boot Manager的情况下可以忽略，因为这个里面已经明确定义了加载哪块硬盘的哪个分区下哪个文件。当没有这个Windows Boot Manager项目而只能通过ATA HDDX下的分区查找时，经测试。会加载上可识别的拥有正确efi应用（位置：`(EFI_Partition)\\EFI\\Boot\\bootx64.efi`）的第一个EFI分区，并根据efi应用的信息加载对应的BCD文件。

So，总结如下。可以没有 :code:`(EFI_Partition)\\EFI\\Boot\\bootx64.efi` ，也可以没有: :code:`(EFI_Partition)\\EFI\\Microsoft\\Boot\\bootmgfw.efi` ，但是不能2个同时没有，存在 :code:`(EFI_Partition)\\EFI\\Boot\\bootx64.efi` 的情况下，可以在BIOS的Boot Menu界面选择ATA HDDX启动，存在 :code:`(EFI_Partition)\\EFI\\Microsoft\\Boot\\bootmgfw.efi` 并设置正确的情况下，可以在BIOS的Boot Menu界面上选择 Windows Boot Manager启动。

说几个关于引导的命令
------------------------------------------------------------------------------------------

* mountvol 用于加载分区，比如 :code:`mountvol K: /s` 加载默认的EFI分区到K盘
* bcdboot 用于修复efi文件，比如 :code:`bcdboot C:\\Windows /l en-us` 将同时修复 :code:`(EFI_Partition)\\EFI\\Boot\\bootx64.efi` 和 :code:`(EFI_Partition)\\EFI\\Microsoft\\Boot\\bootmgfw.efi` 2个文件
* bootrec 可用于重新创建BCD文件，比如 :code:`bootrec /rebulidbcd` 会在默认的位置 :code:`(EFI_Partition)\\EFI\\Microsoft\\Boot` 重新生成识别到的系统的BCD文件
* bcdedit 用于编辑BCD文件

命令的用法都可以非常方便的在微软的文档下找到，或者使用系统下命令提示符下的 :code:`HELP [Commmad]` 命令

以上
