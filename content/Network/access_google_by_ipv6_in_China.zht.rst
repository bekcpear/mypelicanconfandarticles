==========================================================================================
給路由器設定 IPv6 地址以訪問 Google 服務（主要針對中國大陸地區）
==========================================================================================

:slug: access_google_by_ipv6_in_China
:lang: zht
:date: 2017-01-09 10:09
:tags: tunnelbroker, IPv6, DNS

.. contents::

這篇文章要說的，是通過路由器設定 IPv6 地址來訪問 IPv4 所無法訪問的網站（主要是記錄一下本次折騰過程以後可能有用，其實這個方法應該很早以前就可以使用了，不過無所謂啦）。目前 GFW 是沒有針對 IPv6 有很好的限制手段（以後的話以後再說吧），只是針對 IPv6 的 DNS 解析汙染是很嚴重的（ IPv4 的 DNS 汙染更嚴重，不過就算沒汙染也無法訪問就不去考慮啦）。

兩個前提條件
----------------------------------------

* 一個公網的 IPv4 地址（無所謂動態還是靜態）
* 一臺支援刷第三方韌體的路由器，我用的是 OpenWRT ，所以別的也就不清楚啦（如果就單單一臺電腦需要上網，那就更簡單了，就不多說明了，只在下面提一下）

準備好路由器
----------------------------------------

我的路由器是 網件的 R6250 和 華碩的 AC55U （掩面，都是渣渣，不過能用）。 R6250 是用於做外網閘道器的， AC55U 是相當於做 AP 的（因為 R6250 刷了 OpenWRT 後無線訊號渣成翔啊有木有）。關於如何給 R6250 刷 OpenWRT 就不說了，資料一查一大堆（其他也一樣，主要是講原理）。

申請一個 IPv6 地址
----------------------------------------

可以去 `tunnelbroker.net <https://tunnelbroker.net/)>`_ 或者其它服務商申請

雖然部分地區已經有運營商分 IPv6 了，比如江蘇電信，但是速度太慢完全沒法用，分到的應該也就一個 /64 的地址，預設就只能用於一臺裝置，如果需要用於給多臺裝置分 IPv6 ，還需要更復雜的設定。（其他運營商的 IPv6 還沒有用到過，當然教育網的 IPv6 速度非常好）

關於 IPv6 和 IPv4 的區別可以看 `這篇文章 <https://www.ibm.com/support/knowledgecenter/zh/ssw_ibm_i_72/rzai2/rzai2compipv4ipv6.htm>`_ ，從實際體驗上來看，用了 IPv6 後你會發現的是基本不存在區域網的概念了

HE 公司的 tunnelbroker.net 上一個賬戶可以申請最多5個 IPv6 地址，使用原理是把 IPv6 封包再封成為 IPv4 封包，通過 IPv4 網路傳送到 HE 提供的服務端解包後去訪問世界上的 IPv6 網路。

除了這個還有國內的比如 6plat 、 6box 這樣子的服務，前者申請麻煩還要提供身份證，且需要先設定 DDNS ，後者有點貴，所以我不考慮了。

還有一種是可以使用清大 ISATAP 隧道，但是這個基於一個公網 IP 只能分一個 /64 地址，且會根據公網 IPv4 地址不同而變化，可以看如下幾篇文章：

* `關於如何在 nat 後面使用 isatap <https://wiki.tuna.tsinghua.edu.cn/IsatapBehindNat>`_
* `github.com/tuna/ipv6.tsinghua.edu.cn/blob/master/isatap.md <https://github.com/tuna/ipv6.tsinghua.edu.cn/blob/master/isatap.md>`_
* `OpenWRT 配置 IPv6 的 NAT （一般結合 isatap 使用） <https://blog.blahgeek.com/2014/02/22/openwrt-ipv6-nat/>`_

我使用 Windows 嘗試了一下上述第二篇文章的內容，不過失敗了，沒去深究。有興趣的可以看看，聽說清華的 ISATAP 隧道速度頻寬都很足。

我根據自己的實際地理位置（江蘇電信）選擇的是一個 Los Angeles 的埠，建立好後在 'IPv6 Tunnel' 這個標籤下會有幾個資訊：

* Server IPv4 Address
* Server IPv6 Address
* Client IPv4 Address
* Client IPv6 Address

顧名思義，不多解釋，需要解釋的是下面 2 個：

* Routed /64  這個是預設就有的，用來給本地網路其他裝置分配公網 IPv6 的。HE 已經自動把這個地址段路由到 Client IPv6 Address 了。
* Routed /48  這個預設不生成，但是可以點選後面的 Assign/48 去請求分配一個，同樣已經自動把這個地址段路由到 Client IPv6 Address 了，用途是這樣子的：如果本地不止一個路由器來分配 IPv6 ，那麼可以給主路由分配這個字首上的一個地址，然後給其他路由分配主路由上這個字首對應的 /64 地址作為字首再分配給其他路由連線的裝置，解釋可能有點蒼白，後面設定的時候就知道了。

tunnelbroker.net 對應頁面有更詳細的解釋，可以自己去看。

給路由器設定好 IPv6 地址和路由
----------------------------------------

我這裡已經被分配到電信的 IPv6 地址了，但正如我上面所說，渣成X，所以可以在 OpenWRT 的設定介面上取消獲取 IPv6 （不多解釋如何操作了，不取消也沒關係）。

在 Tunnelbroker 建立好了 IPv6 後 'Example Configurations' 標籤頁有很多系統下的配置例子，非常方便， OpenWRT 選擇 'OpenWRT Barrier Breaker' 這個的配置比較合適，我貼在下面來說明：

.. code-block:: shell-session

  root# opkg update                                             # 如果重啟了系統後沒有更新過這個軟體庫的話一定要先更新一下，不然會搜尋不到
  root# opkg install 6in4                                       # 這個是啟用 Tunnel IPv6inIPv4 必備的，其他依賴會自動安裝

  root# uci set network.henet=interface                         # 從這裡開始一組是用來新建一個埠的，看你上面的配置，別看我的
  root# uci set network.henet.proto=6in4
  root# uci set network.henet.peeraddr=216.x.x.x
  root# uci set network.henet.ip6addr='2001:470:x8:xxxx::2/64'
  root# uci set network.henet.ip6prefix='2001:470:fxxx::/48'    # 這個就是我上面有解釋的 Routed /64 ，注意：就算請求生成了 Routed /48 也不會在這邊顯示，但是你替換一下就好了
  root# uci set network.henet.tunnelid=xxxxxx
  root# uci set network.henet.username=xxxxxx
  root# uci set network.henet.password='UPDATE_KEY_OR_PASSWORD' # 這邊需要輸入你的更新密碼，在 'Advanced' 標籤下有個 'Update Key' 。如果你的公網 IPv4 地址是動態的，OpenWRT 已經有內建了更新的指令碼，也是通過這個密碼來更新的
  root# uci set network.henet.defaultroute='0'                  # 這個設定在 tunnelbroker 上是沒有寫的，但是我建議設定一下，不然之後的路由會有問題（至少我這裡是這樣子的）
  root# uci commit network                                      # 提交修改

  root# uci set firewall.@zone[1].network='wan henet'           # 下面的是通用的設定和重啟服務
  root# uci commit firewall

  root# /etc/init.d/network restart
  root# /etc/init.d/firewall reload

**設定路由，這塊是重點**

當設定好了上面的部分後，路由器上目前的地址和路由情況應該是類似這樣子的:

.. code-block:: shell-session

  root# ip -6 addr
  1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 
      inet6 ::1/128 scope host 
      valid_lft forever preferred_lft forever
  2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qlen 1000
      inet6 fe80::526a:3ff:fecb:1b0b/64 scope link 
      valid_lft forever preferred_lft forever
  7: br-lan: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 
      inet6 2001:470:fxxx::1/48 scope global noprefixroute 
      valid_lft forever preferred_lft forever
      inet6 fe80::xxxx:3ff:fecb:1b0b/64 scope link 
      valid_lft forever preferred_lft forever
  11: 6in4-henet@NONE: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1280 
      inet6 2001:470:x8:xxxx::2/64 scope global 
      valid_lft forever preferred_lft forever
      inet6 fe80::xxxx:964d/64 scope link 
      valid_lft forever preferred_lft forever
  
  root# ip -6 route
  2001:470:x8:xxxx::/64 dev 6in4-henet  proto kernel  metric 256 
  2001:470:fxxx::/64 dev br-lan  metric 1024 
  unreachable 2001:470:fxxx::/48 dev lo metric 1024  error -101
  fe80::/64 dev eth0  proto kernel  metric 256 
  fe80::/64 dev br-lan  proto kernel  metric 256 
  fe80::/64 dev 6in4-henet  proto kernel  metric 256 

這是無法正常使用的，因為我是 2 個路由器，所以我是按照 /48 的配置的， /64 的只會更簡單。

首選判斷出上面錯誤的路由有 2 個， **2001:470:fxxx::/64 dev br-lan  metric 1024** 和 **unreachable 2001:470:fxxx::/48 dev lo metric 1024  error -101** 。刪掉它們：

.. code-block:: shell-session

  root# ip -6 route del 2001:470:fxxx::/64 dev br-lan
  root# ip -6 route del unreachable 2001:470:fxxx::/48 dev lo

然後要建立起有用的路由表，設定好預設路由，先讓主路由可以通過 IPv6 連線上網際網路絡，需要這樣子新增：

.. code-block:: shell-session

  root# ip -6 route add default via 2001:470:x8:xxxx::1 dev 6in4-henet # 注意這裡需要指定一下連線網際網路的閘道器地址，就是 HE 提供的 'Server IPv6 Address'

在這裡需要定好幾點：

1. 我的主路由用什麼網段來分配給連線該路由器的其他裝置？ A: 2001:470:fxxx::/64
2. 我的另外一臺路由器用什麼地址做閘道器？ A: 我定為 2001:470:fxxx::1/64
3. 我的另外一臺路由器用什麼地址做 IPv6 的 WAN 口地址？ A: 我定為 2001:470:fxxx::2/64
4. 我的另外一臺路由器用什麼地址段來分配給連線該路由器的其他裝置？ A: 我定為 2001:470:fxxx:10e1::/64

因為都是通過 :code:`br-lan` 這個網橋連線的，所以要這樣子新增：

.. code-block:: shell-session

  root# ip -6 route add 2001:470:fxxx::/48 dev br-lan # 這邊因為我可以完全控制 2001:470:fxxx::/48 這個 IP 段，所以直接 /48 不用 /64
  root# ip -6 route add 2001:470:fxxx:10e1::/64 via 2001:470:fxxx::2 dev br-lan 

這樣子主路由器的路由就設定好了，可以把上述刪添路由的命令加入到 OpenWRT 的開機啟動指令碼下。

測試發現，當重啟路由器後可能不會自動去更新 tunnelbroker 伺服器上的本地 IPv4 記錄（非重啟重新撥號是可以自動更新的，OpenWRT 下），那麼可以在開機指令碼新增如下命令（關於這個連結可以在 tunnelbroker.net 的 Tunnel Details 頁面上的 Advanced 標籤下看到）：

如果不需要路由器，直接電腦設定的話，tunnelbroker.net 的 Tunnel Details 頁面上的 Example Configurations 標籤下有很多執行緒的系統的配置， Linux 和 Windows 的都有。

.. code-block:: shell-session

  curl https://xxxxx:xxxxxxxxxxxxx@ipv4.tunnelbroker.net/nic/update?hostname=xxxxxx

然後下面就是設定第二個路由器的 IPv6 了，找到設定 IPv6 的介面，選擇靜態 IPv6 地址， WAN 口 IP 設定為 2001:470:fxxx::2 ，字首設定為 64 位，閘道器設定為 2001:470:fxxx::1 ， LAN 口的 IP 設定為 2001:470:fxxx:10e1::1 ，字首設定為 64 位。每個路由器設定位置有差異，具體如何設定就不說了。（注意這邊設定 DNS 伺服器的時候，一定要設定為主路由器的網路地址，也就是 IPv6 的話是 2001:470:fxxx::1 ， IPv4 的話根據你的路由來看，為後文做鋪墊，用於解決 DNS 汙染問題的）

這樣子設定後如果不出意外，連線兩個路由器的裝置就都應該可以被自動分配到 IPv6 地址了。（目前應該都是預設安裝好了 DHCPv6 了）

解決 DNS 汙染的問題
----------------------------------------

一般來說有 2 種方法來解決，一種是設定預設使用 TCP 方式連線 DNS 伺服器查詢，一種是將常用的被汙染的 DNS 設定成為 hosts 檔案查詢。從長遠的便捷性來考慮的話，使用第一種比較好，不過我差了一下一個不錯的實現方案(pdnsd)已經不再維護，還有一種(unbound)評價說速度太慢，加上我也懶得再裝軟體配置，就選擇了第二種方案，使用 hosts 檔案 + 路由器上本身自帶的 dnsmasq 服務解決 IPv6 DNS 汙染問題。

很簡單，過程如下：

首先我是找到了一個關於 Google 的 ipv6 hosts 的專案，地址是： `https://github.com/lennylxx/ipv6-hosts <https://github.com/lennylxx/ipv6-hosts>`_ ，因為我端口出口在洛杉磯，所以它預設的解析地址本不好用，於是我臨時用 DigitalOcean 開了一臺 San Francisco 的 VPS 使用專案的指令碼重新生成了一遍 hosts 檔案在 `這裡 <https://c.ume.ink/s/kVTSe3f9WPQ5XC0>`_ ，然後把它與路由器原本的 /etc/hosts 檔案合併，並開啟路由器的設定介面，設定好 dnsmasq 的上游 DNS 伺服器其他保持原樣，最後設定另一臺路由器預設的 DNS 伺服器以及主路由器預設 DNS 伺服器均為主路由器即可。

完成！

有一個問題：我的 Windows 10 通過網線連線主路由器的時候，怎麼也無法分配到正確的 IPv6 地址，但是我的 Gentoo 可以非常輕鬆的獲取到。嘗試了很多次無果，我預設他們八字相沖吧，等 OpenWRT 版本更新後看看會不會有好轉。Windows 10 通過 WiFi 去連線另外一臺路由器就非常正常。總之現在已經可以正常使用了，我的 iPad 也可以正常通過 IPv6 訪問網路了。

