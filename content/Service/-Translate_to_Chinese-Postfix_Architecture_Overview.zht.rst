========================================================================
[原文翻譯] Postfix Architecture Overview
========================================================================

:slug: -Translate_to_Chinese-Postfix_Architecture_Overview
:lang: zht
:date: 2016-07-25 03:23
:tags: postfix, server
:notoriginal: true
:status: draft

.. contents::

本文翻譯自 http://www.postfix.org/OVERVIEW.html ，草稿不釋出，原始協議未知。


介紹
------------------------------

這個文件展現了Postfix結構的總覽，並將每一個Postfix的命令和伺服器程式超連結到其他的文件進行描述。文章給出了每個使用的命令和伺服器程式的大體資訊，並將特殊的使用案例和背景資訊超連結到別的文件。（關於這個，我這邊僅僅會挑選自認為重點的描述在文件的結尾）

本文包含的主題有：

* Postfix如何接收郵件
* Postfix如何傳送郵件
* Posffix後臺執行過程
* Postfix支援的命令

Postfix符合接收郵件
------------------------------

當一封郵件到達了Postfix的郵件系統時，首先停留在了incoming佇列。下面的圖顯示了一封新郵件參與的主要程序。名稱後面跟有數字的是Postfix命令或者伺服器程式，名稱為[大寫]的是Postfix佇列（原文是寫的不跟數字且有陰影的為佇列，我這邊因為作圖使用code標籤所以就不弄陰影了）。

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

* 網路郵件通過 :code:`smtpd(8)` 或者 :code:`qmqpd(8)` 伺服器進入Postfix，這2種伺服器會去除SMTP或QMQP的協議封裝，為了保護Postfix也會同時執行一些必要的檢查，然後就把傳送者、接收者和郵件內容傳輸給 :code:`cleanup(8)` 伺服器了。 :code:`smtpd(8)` 伺服器通過一些配置就可以用於遮蔽不需要的郵件，請看文件 `SMTPD ACCESS README <http://www.postfix.org/SMTPD_ACCESS_README.html>`_ 。
* 本地寄送郵件由被Postfix相容的 :code:`sendmail(1)` 命令接收，並被特權命令工具 :code:`postdrop(1)` 放到了MAILDROP佇列。即使當Postfix郵件系統不工作的時候，這個操作也是會執行的（估計是純粹的命令工具操作不依賴伺服器）。本地的 :code:`pickup(8)` 命令則用於挑選本地提交的郵件，同樣也會做一些有利於伺服器的檢測，然後將郵件內容傳送給 :code:`cleanup(8)` 伺服器。
* 郵件系統內部源的郵件會被直接傳送到 :code:`cleanip(8)` 伺服器，這個 **內部源** 並沒有出現在上述的圖例裡面
