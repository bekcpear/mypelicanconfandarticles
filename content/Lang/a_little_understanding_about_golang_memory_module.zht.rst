==============================
關於 Golang 記憶體模型
==============================

:slug: a_little_understanding_about_golang_memory_module
:lang: zht
:date: 2017-02-19 23:19
:tags: golang, reference, gochannel
:description: Go 語言 channel 在傳送/接收時如何動作

.. contents::

最近開始學習 Go 語言，在看到其 `記憶體模型`_ 的時候一度懵逼了，主要是碰到關於通道的其中兩句概念整理以為衝突了，先整理自己的理解如下。

原文
------------------------------

  A send on a channel happens before the corresponding receive from that channel completes.

  A receive from an unbuffered channel happens before the send on that channel completes.

從字面意思來看：

1. 傳送到通道的動作發生在對應的接收動作完成之前（這個是針對帶緩衝區域和不帶緩衝區域的）
2. 針對不帶緩衝的通道，從通道接收的動作要發生在傳送資料到通道動作完成之前。

一開始怎麼也無法理解，然後查到 `郵件列表的討論`_ ，特別注意到了 **completes** 這個詞。 *這篇對話很長，英語渣實在看不下去了，先如下理解了，等以後慢慢摸索*


關於自己的理解
------------------------------

前一句話很容易搞懂，既然要獲取資料，那麼肯定是要先把資料傳送到通道了才能從通道獲取，主要是後一句話，要明確不帶緩衝區域就意味著這個變數儲存不了資料（我是這麼理解的），接收動作和傳送動作是需要同時進行的。

比如這段程式碼：

.. code-block:: go

  package main

  import "fmt"

  var c = make(chan int32)
  var s int32 = 1

  func f(){
    s = <-c
  }

  func main(){
    go f()
    c <- 1234567890
    fmt.Println(s)
  }

輸出的是 1234567890 (01001001100101100000001011010010) 這個值。我理解的傳送和接收圖解說明：

::

  int32 是 32bits 的長度，下面則是這個通道可以接收的資料量
                  31                                                             0
                  | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
                   0 1 0 0 1 0 0 1 1 0                                                0101100000001011010010 <---send
                 <比如傳送到通道的時候，才傳送了高位的 10 個字，接收動作就需要開始了>
  01001 <---recv             0 0 1 1 0 0 1 0 1 1 0                                    0000001011010010 <---send

那麼歸納一下就是帶緩衝區域的 channel 只要有值就可以獲取，否則無法獲取報錯。不帶緩衝區域的一定要同時傳送和獲取，否則報錯。

還遇到了這樣子的一個問題，程式碼如下：

.. code-block:: go

  package main

  import (
    "fmt"
    "time"
  )

  var c = make(chan int)
  var s int = 1

  func f(){
    s = <-c
  }

  func main(){
    go f()
    time.Sleep(time.Duration(1000)*time.Nanosecond)
    c <- 1234567890123
    fmt.Println(s)
  }

輸出結果是 1
如果調整數值 1000 為 600 則可以正常輸出 1234567890123 這個值根據不同執行環境有區別。
我覺得可能是等待超時了，先標記

.. _`記憶體模型`: https://golang.org/ref/mem
.. _`郵件列表的討論`: https://groups.google.com/forum/#!topic/golang-nuts/NvB_hXkI9PE
