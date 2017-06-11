======================================================================
Windows10下的UEFI引導流程解析和引導修復說明
======================================================================

:slug: Windows10_UEFI_Boot_Process
:lang: zht
:date: 2016-07-14 11:54
:tags: windows, bootloader, UEFI
:status: draft

.. contents::

Windows10下EFI分割槽檔案結構(僅說明3個必要檔案)：
------------------------------------------------------------------------------------------

::

  (EFI分割槽)..................此分割槽必須為Fat32格式，不然UEFI韌體將無法識別
  |
  +--EFI
    |--Microsoft
    |  +--Boot
    |     |--bootmgfw.efi...一個針對Windows的efi應用，使Boot Menu介面上的Windows Boot Manager可以工作
    |     +--BCD............啟動配置檔案，使用者編輯啟動選單以及預設的啟動順序等
    |--Boot
        +--bootx64.efi.......一個針對UEFI的統一efi應用，可以針對所有的系統。如果是32位系統，則是boota32.ef

.. PELICAN_END_SUMMARY

引導流程
------------------------------------------------------------------------------------------

::

                                       計算機加電
                                          |
                                        BIOS自檢
                                          |
                                      UEFI韌體啟動
                                          |
                          根據NVRAM下的BootOrder順序載入啟動裝置
                                          |
                獲取對應啟動裝置下第一個存有正確efi應用的Fat32格式分割槽並載入
                                          |
                              讀取efi應用資訊，載入到BCD檔案
                                          |
  讀取BCD檔案下的記錄以載入系統，預設Windows10系統是載入C:\Windows\System32\winload.efi應用
                                          |
                    接下來就交給系統服務了。這樣子就完成了系統的啟動過程


說明一下：

* 什麼叫做根據NVRAM下的BootOrder順序載入啟動裝置，這個裡面有幾個知識點

  1. **NVRAM（非易失性儲存器）** 是BIOS用於儲存本計算機啟動裝置資訊的載體，可以通過 :code:`bcdedit /enum firmware` 來檢視資訊，參考 `這個 <https://technet.microsoft.com/zh-cn/library/cc749510(v=ws.10).aspx>`_ 
  2. **BootOrder** 顧名思義就是一個引導順序，可以在BIOS下調節，比如先引導Windows Boot Manager還是先引導ATA HDD0這個裝置

* 什麼叫做獲取對應啟動裝置下第一個存有正確efi應用的Fat32格式分割槽並載入？正常情況來說，一個硬碟分割槽僅有一個Fat32格式的EFI分割槽，並且往往是在第一個，但是當出現多了EFI分割槽那麼UEFI韌體將如何載入呢？對於首選啟動已經設定為了Windows Boot Manager的情況下可以忽略，因為這個裡面已經明確定義了載入哪塊硬碟的哪個分割槽下哪個檔案。當沒有這個Windows Boot Manager專案而只能通過ATA HDDX下的分割槽查詢時，經測試。會載入上可識別的擁有正確efi應用（位置：`(EFI_Partition)\EFI\Boot\bootx64.efi`）的第一個EFI分割槽，並根據efi應用的資訊載入對應的BCD檔案。

So，總結如下。可以沒有 :code:`(EFI_Partition)\EFI\Boot\bootx64.efi` ，也可以沒有: :code:`(EFI_Partition)\EFI\Microsoft\Boot\bootmgfw.efi` ，但是不能2個同時沒有，存在 :code:`(EFI_Partition)\EFI\Boot\bootx64.efi` 的情況下，可以在BIOS的Boot Menu介面選擇ATA HDDX啟動，存在 :code:`(EFI_Partition)\EFI\Microsoft\Boot\bootmgfw.efi` 並設定正確的情況下，可以在BIOS的Boot Menu介面上選擇 Windows Boot Manager啟動。

說幾個關於引導的命令
------------------------------------------------------------------------------------------

* mountvol 用於載入分割槽，比如 :code:`mountvol K: /s` 載入預設的EFI分割槽到K盤
* bcdboot 用於修復efi檔案，比如 :code:`bcdboot C:\Windows /l en-us` 將同時修復 :code:`(EFI_Partition)\EFI\Boot\bootx64.efi` 和 :code:`(EFI_Partition)\EFI\Microsoft\Boot\bootmgfw.efi` 2個檔案
* bootrec 可用於重新建立BCD檔案，比如 :code:`bootrec /rebulidbcd` 會在預設的位置 :code:`(EFI_Partition)\EFI\Microsoft\Boot` 重新生成識別到的系統的BCD檔案
* bcdedit 用於編輯BCD檔案

命令的用法都可以非常方便的在微軟的文件下找到，或者使用系統下命令提示符下的 :code:`HELP [Commmad]` 命令

以上
