==================================================
详解 Yubikey 5 NFC 的工作原理（整理）
==================================================

:slug: yubikey_5_nfc_functions
:date: 2019-03-09 21:03
:modified: 2020-09-12 03:39
:lang: zh_hans
:notoriginal: true
:tags: yubikey, security, 2fa, otp, openpgp
:description: 最近新入了 Yubikey 5 NFC，就想把之前沒弄懂的功能和实现原理全部理清楚。本文主要做整理和归纳，说明 Yubikey 5 NFC 的各项功能，包括 U2F 的工作原理和密钥生成方式
:license: 本文所有内容整理自 FIDO, Yubico, Archlinux Wiki, Wikipedia，本站不声明版权。
:noindent: true
:summary:
:color: #161616

.. contents::

* 操作温度：   0 °C - 40 °C 
* 存储温度： -20 °C - 85 °C 

USB 接口
==========================================

USB 2.0 接口，当连接计算机时，它会把自己表现为除了其它单独 USB 接口外额外的一个 USB 综合设备。其 USB PID 和 iProduct 字符串会根据配置的 USB 接口类型改变，如下表。 Vendor ID 是 0x1050

+-----------------+--------+-----------------------+
|  USB Interface  | PID    | iProduct String       |
+=================+========+=======================+
| OTP             | 0x0401 | YubiKey OTP           |
+-----------------+--------+-----------------------+
| FIDO            | 0x0402 | YubiKey FIDO          |
+-----------------+--------+-----------------------+
| CCID            | 0x0404 | YubiKey CCID          |
+-----------------+--------+-----------------------+
| OTP, FIDO       | 0x0403 | YubiKey OTP+FIDO      |
+-----------------+--------+-----------------------+
| OTP, CCID       | 0x0405 | YubiKey OTP+CCID      |
+-----------------+--------+-----------------------+
| FIDO, CCID      | 0x0406 | YubiKey FIDO+CCID     |
+-----------------+--------+-----------------------+
| OTP, FIDO, CCID | 0x0407 | YubiKey OTP+FIDO+CCID |
+-----------------+--------+-----------------------+

但是我这里当 USB 接口为 OPT, FIDO, CCID 时， iProduct String 为 YubiKey 4 OPT+FIDO+CCID, 不知道是不是历史遗留问题。

使用 Yubikey Manager 可以配置功能的启用与关闭。

OTP 接口
-------------------------------------------------------------

OTP 接口把自己作为 USB 键盘呈现给操作系统，输出是来自虚拟键盘的一系列击键。

OTP 应用使用 OTP 接口，有 2 个可编程的槽，每个可以持有以下凭据中的一种：

* Yubico OTP
* HMAC-SHA1 Challenge Response
* Static Password
* OATH-HOTP **注意和 CCID 接口的区分**

FIDO 接口
-------------------------------------------------------------

FIDO 接口提供对 `FIDO2`_ 和 `U2F`_ 应用的访问，它把自己作为 HID 呈现。

CCID 接口
-------------------------------------------------------------

CCID 接口提供了对 `OATH(HOTP/TOTP)`_ ， `PIV`_ /智能卡和 `OpenPGP`_ 应用的通讯，他把自己作为 USB 智能卡读卡器呈现给操作系统，每个应用都会把自己作为连接对应读卡器的单独的智能卡来呈现。

YubiKey 5 系列可以持有最多 32 个 OATH 凭证，并同时支持 TOTP 和 HOTP，访问这个小程序需要使用到 Yubico Authenticator.

其余看对应说明。

NFC
==========================================

USB 接口以外的一种无线接口。详细的标准我不关注了。

NFC Data Exchange Format (NDEF) URI 使用了新格式，比如 OTP 值获取如下::

  https://my.yubico.com/yk/#<OTP>

对于需要触摸的请求会有 20s 的操作时间。一段时间不活动后，放置在台式 NFC 读取器上的 YubiKey 可能会断电以避免设备被意外访问。重新放置一下就可以激活。有些读取器会周期性供电来避免设备断电。


Secure static passwords
==========================================

一个基本的 Yubikey 功能，它可以生成一个 38 字符的静态密码。

.. code-block:: bash

  ykman otp static -h  # 查看使用说明

Yubico OTP
==========================================

Yubico OTP 是 44 个字符组成的、仅使用一次、安全的、128 位 AES 对称加密的公共 ID 和密码字符串，几乎不可能伪造。前 12 个字符是不变的代表着设备的公共 ID。剩下的 32 个字符则是每次生成的唯一的密码。密码中附加了一个计数器值，当验证密码时， Yubico Cloud 会对获取的计数器与当前服务器存储的针对这个 ID 的计数器做比较，只有在获取的计数器大于服务器保存的计数器时，才判断有效。所以过期的 OTP 是无效的。

因为这个是对称加密，且需要连接 Yubico Cloud 来做验证，个人认为安全性相对较弱，尽量不用。需要的时候再深入理解。

.. _`OATH(HOTP/TOTP)`:

OATH-HOTP/TOTP
==========================================

一个用于登录支持其服务的 6-8 位数字的一次性密码。

TOTP 是通过 :code:`HMAC(sharedSecret, timestamp)` 生成的，其中 timestamp 每 30 秒变化一次，而 sharedSecret 通常通过二维码提供或者已经预编写在了硬件令牌里（这里就是预编写在 Yubikey 中了）。但是因为 Yubikey 不带内置时钟，所以需要利用 `帮助应用`_ 来生成。

HOTP 工作原理和 TOTP 类似，只是把时间戳替换成了一个验证计数器，这样的好处是不需要额外的时钟。不过因为很容易和对应的服务器丢失计数器同步，所以服务在验证这种一次性密码的时候应该扩大计数器的范围多试几次。在按下 Yubikey 的按钮时， HOTP 代码会被发送，可以通过 `Yubikey 个性化工具`_ 来做配置（这里指代的应该是 OTP 接口的 HOTP）。

.. code-block:: bash

  ykman oath -h # 查看使用说明

Challenge and Response
==========================================

最适合离线验证，用于 Windows， Mac 和 Linux 的登录。这个最简单的应用是密码验证，其中挑战就是询问密码，而有效的回答就是正确的密码。

Yubikey 的实现原理是一个挑战码被客户端发给 Yubikey，然后 Yubikey 回传一个反馈码，支持两种模式：

Yubico OTP 模式
  在这个模式下，客户端会发送一个 6 字节的挑战码，然后 Yubikey 使用 Yubico OTP 算法来创建一个反馈码，创建过程会用到一些变量字段，所以就算是同一个挑战码，每次创建的也是不同的。

.. code-block:: bash

  ykman otp yubiotp -h # 查看使用说明

HMAC-SHA1 模式
  在这个模式下，客户端会发送一个 0 - 64 字节的挑战码，然后 Yubikey 使用 HMAC-SHA1 算法结合一个 20 字节的密钥来创建一个反馈码，创建过程不会用到其它变量字段，所以针对同一个挑战码，每次创建的都是相同的。

.. code-block:: bash

  ykman otp chalresp -h # 查看使用说明

.. _`PIV`:

Smart-Card(PIV-compliant)
==========================================

智能卡包含了一个代理数据交换的计算机芯片。 其功能基于行业标准的 :ruby:`个人身份与验证卡|Personal Identity and Verification Card` （PIV）接口，这个接口在 CCID 协议上实现。

PIV，也叫做 FIPS 201，是一个美国政府标准，它利用存储在智能卡上的一个私钥通过像 PKCS#11 这样的通用接口来启用 RSA 或 ECC 签名/加密操作。

PIV 主要用于非 web 应用，且在 Windows 中是内置支持的，在 OS X 和 Linux 的话可以通过 OpenSC 项目来使用。

关于 Yubikey PIV 实现的技术细节
-------------------------------------------------------------

* 默认的 PIN 码为 123456，默认的 PUK 码为 12345678

  * 用来保护终端用户的私钥操作，可以支持长达 8 个字母数字字符。当 PIN 输出错误 3 次后，它会被限制使用。当 PIN 被限制了或者丢失的时候，可以使用 PUK 码来重置。 PUK 码和 PIN 有相同的限制条件，如果两个都被限制了，那么只能使用特殊的命令来重置它们，这个命令会重置 PIN， PUK 和 管理密钥到默认的值，并删除所有已经存在的证书和密钥。

* 默认的 3DES 管理密钥(9B)为 010203040506070801020304050607080102030405060708

  * 24 字节，用于保护管理功能。当要做诸如生成/导入密钥和证书到 PIV 槽这种管理操作时，需要提供这个密钥。

  以上信息为 PIV 提供了两种不同的访问级别：一种是终端用户（卡持有者）级的，被 PIN 码所保护，用于日常 PIV 功能的使用；另一种是管理员级的，被一个管理密钥所保护，用于证书的配置。 **在使用 PIV 功能前一定要修改**

* 存在以下密钥槽：

  * 9A, 9C, 9D, 9E: RSA 1024, RSA 2048, 或 ECC secp256r1 密钥 (算法分别为 6, 7, 11) **Yubikey 5 还支持 ECC P-384**
  * 9B: 用于 PIV 管理的三重 DES 密钥（算法 3）

* 针对目前的 YubiKey NEO 和 YubiKey 4/5 设备而言，其存储对象的最大大小分别为 2025 和 3049 字节
* 目前所有功能在接触与非接触接口上都能支持（违反规范要求） **这边是哪个规范不清楚，可能是 PIV 规范，但我实在没精力去细看了**

PIV 证书槽
-------------------------------------------------------------

Yubikey NEO 有 4 个，而 Yubikey 4/5 有 24 个。每个槽都可以存一张 X.509 证书，随同其私钥一起。技术上来讲每一个槽都是类似的，但是它们的用途是不同的。

Slot 9a: PIV 验证
  这个证书及其私钥是用来验证卡和卡的持有者的。这个槽用于如系统登录这种事情。执行任意私钥操作都需要用户提供 PIN 码。一旦正确的 PIN 被提交了，那么后续其它的私钥操作可以不需要让用户同意。

Slot 9c: 数字签名
  这个证书及其私钥是用来对文档、电子邮件、文件和可执行文件进行数字签名的。执行任意私钥操作都需要用户提供 PIN 码。且每次签名操作都需要用户参与同意。

Slot 9d: 密钥管理
  这个证书及其私钥是用于机密性目的的加密的。这个槽用于加密电子邮件或文件。执行任意私钥操作都需要用户提供 PIN 码。一旦正确的 PIN 被提交了，那么后续其它的私钥操作可以不需要让用户同意。

Slot 9e: 卡验证
  这个证书及其私钥是用于支持其他物理访问应用程序，例如通过可支持 PIV 的门锁提供对建筑物的物理访问 。操作这个槽的私钥操作时，不需要终端用户的 PIN 码。

Slots 82-95: 退役的密钥管理
  这些槽适用于先前用过的密钥管理密钥，来使得可以对先前加密的文档或电子邮件进行解密。

Slot f9: 认证
  此插槽仅用于证明使用指令 f9 在设备上生成的其他密钥。复位时不会清除此插槽，但可以覆盖该插槽。

PIV :ruby:`认证|Attestation`
-------------------------------------------------------------

认证这个概念是用来说明某个非导入的非对称密钥在设备上被生成了。通常它会在创建证书前被使用。

认证是通过对需要被证明的密钥创建一个 X.509 证书来实现的，这只有在该密钥是在设备上被生成时才会完成。且这个证书只应该被用于验证密钥是在设备内生成的这 **一个** 目的。

使用
-------------------------------------------------------------

创建密钥对可以使用工具 YubiKey Manager, Archlinux 下安装 :code:`yubikey-manager` 包就可以了，如果需要 GUI 的话，可以安装 :code:`yubikey-manager-gui` 。

大致的使用方法就是，先在 PIV 证书槽创建私钥和证书，然后就可以通过像 PSCK#11 这样的接口来对其进行访问了，在 Linux 上需要安装 :code:`opensc` 库来使用。

使用 PIV 验证 SSH 可以参考 ArchWiki https://wiki.archlinux.org/index.php/YubiKey#Using_a_YubiKey_with_SSH ，注意的是 OpenSSH 的 PKCS#11 接口目前不支持 ECDSA：

* https://github.com/OpenSC/OpenSC/issues/803#issuecomment-227067408
* https://bugs.launchpad.net/ubuntu/+source/openssh/+bug/1665695
* https://bugzilla.redhat.com/show_bug.cgi?id=1354510

之前有人做了补丁（ https://bugzilla.mindrot.org/show_bug.cgi?id=2474 ）来支持。根据 OpenSSH 维护者 Damien Miller 的说法， 8.0 版本计划支持 ECDSA。

其它功能参见这里： https://developers.yubico.com/PIV/Guides/ 整理后觉得如果不是专门使用 PIV 的场景就不用 PIV 了。 一个关于 EC 的应用： https://www.smartcard-hsm.com/2014/08/22/using-smartcard-hsm-with-ecc-and-opensc.html

.. _`OpenPGP`:

OpenPGP
==========================================

.. PELICAN_BEGIN_SUMMARY

OpenPGP 是一个用于签名和加密的开放标准。它通过像 PKCS#11 这样的接口，使用存储在智能卡上的私钥来启用 RSA 或 ECC 签名/加密操作。这个应用可以为验证、签名和加密各存一个 PGP 密钥。和 PIV 触摸策略类似， openPGP 应用也可以设置需要接触金属触点来允许一个操作。

* Yubikey 5 NFC 仅支持 RSA 密钥，不支持 ECC 密钥
* PGP 不用于 web 验证

支持的算法有：

* RSA 1024
* RSA 2048
* RSA 3072
* RSA 4096

.. PELICAN_END_SUMMARY

RSA 3072 和 RSA 4096 需要 GnuPG 版本 2.0 及以上。

.. note::
  2020.9.12 更： YubiKey 5Ci 固件 5.2.3 版本以上 支持 ECC 了，但是 5 NFC 还是不支持。


一个别人整理的使用手册： https://github.com/drduh/YubiKey-Guide

文中有一个没有指出的在 :code:`admin` 命令下，使用 :code:`passwd` 做密码修改操作时，有一个 :code:`set the Reset Code` 选项，查阅如下所属资料后得知，其用于普通用户在忘记 PIN 且不知道 Admin PIN 时 对自己的 PIN 做重置时使用，一般在有管理员统一管理时有用，当卡本身属于自己时因为可以直接使用 Admin PIN 所以无需设置这个选项。

Functional Specification of the OpenPGP application on ISO Smart Card Operating Systems: https://gnupg.org/ftp/specs/OpenPGP-smart-card-application-3.3.1.pdf

.. _`U2F`:

FIDO U2F(Universal Second Factor)
==========================================

一个启用强双因素验证的开放验证标准。 `这里`_ 可以看到当前支持的网站。  `FIDO(Fast Identity Online)`_ 是一个联盟的名字，这个联盟由世界上各大财团组成，旨在解决世界上的密码问题。

FIDO U2F 让在线服务通过添加一个强第二因素到用户登录来增强其现有密码设施的安全性。

U2F 的优点（Yubico 网站指出的）
------------------------------------------------------------------------

强安全性
  使用公钥加密的强双因素验证。通过它可以对抗钓鱼、会话劫持、中间人和恶意软件的攻击。

使用简单
  因为很多平台都原生支持了，所以是开箱即用的，对任意数量的服务启用了即时身份验证。不需要编写代码也不需要安装驱动。

高隐私性
  用户可以控制并同时拥有多个线上身份，这些身份可以是和个人信息毫无关联的。 U2F 安全密钥为每个服务生成一对密钥，且服务本身不存储/共享私钥，所以 U2F 安全密钥可以支持任意数量的服务。 **针对 Yubikey，私钥每次都是通过设备上的主密钥生成的，所以可以满足任意数量的 web 服务，具体见下**

多选择的
  开放标准提供灵活性和产品选择。专为现有手机和计算机设计，适用于多种身份验证模式，以及不同的通信方式（USB和NFC）。

可互操作
  开放标准是由包括 Google 等 170 多家公司在内的领先的互联网和金融服务支持的。 U2F 允许每个服务商单独作为验证提供者，也可以让用户通过联合服务提供者来做验证。

经济适用
  用户可以在线选择一系列经济实惠的设备。 Yubico 通过 Yubico 开发人员计划提供免费的开源服务器软件，用于后端集成。

安全恢复
  建议用户是给每个服务提供者注册至少 2 个 U2F 设备的，就算该服务提供者给用户提供了备份码。

电子身份
  为需要更高级别身份保证的组织提供身份验证。通过服务提供商，您可以将您的U2F安全密钥绑定到您真正的政府颁发的身份。

工作原理
------------------------------------------------------------------------

以下是 U2F 的处理流程：

1. RP 返回记录的 handle, app_id 和 challenge 给客户端（比如浏览器）
2. 为了抵抗钓鱼网站和中间人攻击，客户端会附加上 orgin(URI) 和 TLS 信道 ID，连同 RP 返回的内容一起给 U2F 设备
3. U2F 设备根据 app_id 和 handle 查到对应的私钥，并对信息进行签名；同时对内置计数器加 1，然后把这些信息发送给客户端 （针对 Yubikey 的实现见下文）
4. 客户端收到 U2F 的返回信息后，连同之前未加密的 challenge 和自己拿到的 origin 以及 TLS 信道 ID 一起发给 RP
5. RP 根据对应的公钥来检查签名，同时验证明文信息

更详细的说明查看： https://developers.yubico.com/U2F/Protocol_details/Overview.html

.. ditaa::
  :alt: U2F workflow

                Device                                             Browser                                     Relying Party
                  |                                                   |                                             |
                  |                                                   |              username & password            |
                  |                                                   |-------------------------------------------->|
                  |                                                   |                                             |
                  |                                                   |                                 +-----------+------------+
                  |                                                   |                                 |     Verify Password    |
                  |                                                   |                                 +------------------------+
                  |                                                   |                                 |   Generate Challenge   |
                  |                                                   |                                 +------------------------+
                  |                                                   |                                 |     Lookup pub_key     |
                  |                                                   |                                 | associated with handle |
                  |                                                   |                                 +-----------+------------+
                  |                                                   |                                             |
                  |                                                   |    handle as 'h',app_id as 'a',challenge    |
                  |                                                   |<--------------------------------------------|
                  |  h,a; challenge,origin,tls_channel_id,etc as 'c'  |                                             |
                  |<--------------------------------------------------|                                             |
                  |                                                   |                                             |
    +-------------+-----------+                                       |                                             |
    |   Lookup the priv_key   |                                       |                                             |
    |  associated with handle |                                       |                                             |
    +-------------+-----------+                                       |                                             |
    |         counter++       |                                       |                                             |
    +-------------+-----------+                                       |                                             |
                  |                                                   |                                             |
                  |       counter, signature(a,c,counter) as 's'      |                                             |
                  |-------------------------------------------------->|                                             |
                  |                                                   |                                             |
                  |                                                   |             counter, c, s                   |
                  |                                                   |-------------------------------------------->|
                  |                                                   |                                             |
                  |                                                   |                     +-----------------------+-----------------------+
                  |                                                   |                     |             using pub_key to check s          |
                  |                                                   |                     |    Verify origin, tls_channel_id and counter  |
                  |                                                   |                     +-----------------------+-----------------------+
                  |                                                   |                                             |

密钥生成
------------------------------------------------------------------------

一般来说， U2F 每注册一个服务就应该生成一对新的密钥，但是这需要消耗很大的防篡改存储空间，价格昂贵。所以 Yubikey 采取了一种措施，能用低廉的成本就完成任意数量服务的注册。

对密码学不是很了解，说一下基本流程。

Yubikey 里面有一个随机数生成器(RNG)和一个在出场就配置好的只针对本设备的密钥(Device secret)。

当需要注册一个服务的时候，通过获取到的 APPID 结合 RNG 生成的随机数以及 Device secret 通过 HMAC-SHA256 单向函数生成所需的针对该服务的私钥，然后将生成的随机数和其 MAC 结合变成 handle，然后把通过私钥生成的公钥和 handle 发给服务商。

当需要验证的时候，也是需要重新通过 APPID 生成一下，此时会先验证 handle 是否未被修改，利用其 MAC，然后把提取的随机数和 Device secret 与 APPID 一起传给 HMAC 再生成一遍私钥，之后做相关操作。这里会对一个全局计数器进行操作，每次验证都会加 1，这也是在这个步骤中唯一会修改的状态。计数器是在所有凭据间共享的。

.. _`FIDO2`:

FIDO2
==========================================

支持扩展验证选项的的最新的开放验证标准。是由 W3C 提出的 Web Authentication 规范和相应 FIDO 联盟提出的 :ruby:`客户端到验证器协议|Client-to-Authenticator Protocols` (CTAP) 所组成的。

FIDO2 支持无密码、第二因素和多因素的用户体验模式，包括嵌入式（或绑定的）验证器（如生物识别或 PIN ）或外部的（或漫游的）验证器（如 FIDO 安全密钥、移动设备、可穿戴设备等）。

FIDO2 基于公钥密码学，提供了和 U2F 同等级别的安全性。它还允许存储 :ruby:`驻留凭据|resident credentials` 。因为驻留凭据可以保存用户名和其它数据，所以就支持了真正的无密码验证。 Yubikey 5 系列可以持有最多 25 个驻留密钥。如果使用了 RSA 密钥的话，那么 RSA 最多 3 个，其它需为 ECC。

驻留凭据可以是无锁的以提供强单因素验证，也可以被一个 PIN 保护以提供双因素验证。 PIN 可以长达 128 字符。 PIN 一旦设置就不能移除只能修改，除非重置整个 FIDO2 应用。

**重置 FIDO2 应用也会重置 U2F 密钥。使用 U2F 注册了 YubiKey 的网站都将无法使用，直到 YubiKey 重新注册该网站**

默认值
  PIN： 未设置的。

W3C WebAuthn
  定义了内置到浏览器和平台内的标准 web API，这个 API 对 FIDO 验证提供支持。

CTAP2
  允许在启用了 FIDO2 的浏览器和操作系统上通过 USB, NFC 或 BLE 来使用外部验证器做验证以提供无密码、第二因素或多因素验证体验。

CTAP1
  是 FIDO U2F 的新名字，和 CTAP2 类似，但 CTAP1 只对现有 FIDO U2F 设备提供第二因素验证，可以理解为向下的兼容协议。


一些链接
==========================================

* [Github Repo] Scripts to encrypt/decrypt files using OpenSSL: https://github.com/koljaschleich/file-encryption
* [PDF.slide] Using Cryptographic Hardware to Secure Applications: https://momjian.us/main/writings/crypto_hw_use.pdf
* [Github Repo] GPG asymmetric (YubiKey) password manager: https://github.com/drduh/Purse
* [Yubico] YubiKey 5 Series Technical Manual: https://support.yubico.com/support/solutions/articles/15000014219-yubikey-5-series-technical-manual
* [Github Wiki] US PIV of OpenSC: https://github.com/OpenSC/OpenSC/wiki/US-PIV
* [Yubico] Accidentally Triggering OTP Codes: https://support.yubico.com/support/solutions/articles/15000006440-accidentally-triggering-otp-codes-with-your-nano-yubikey



.. _`这里`: https://www.yubico.com/works-with-yubikey/catalog/#protocol=universal-2nd-factor-(u2f)&usecase=all&key=all
.. _`FIDO(Fast Identity Online)`: https://fidoalliance.org/
.. _`帮助应用`: https://developers.yubico.com/OATH/YubiKey_OATH_software.html
.. _`Yubikey 个性化工具`: https://developers.yubico.com/yubikey-personalization-gui/
