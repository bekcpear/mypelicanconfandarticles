==============================================================
GnuPG 2.3.2 与 yubikey-manager 的冲突
==============================================================

:slug: gnupg_2.3.2-conflicts-with-yubikey-manager
:date: 2021-09-30 21:35
:lang: zh_hans
:color: #0093DD
:tags: GnuPG,ykman,PC/SC,ccid
:mykeywords: gnupg,gpg,ykman,yubikey,PC/SC,pcsc,ccid
:description: gpg 2.3.2 与 yubikey-manager 冲突的说明
:noindent: true
:summary:

.. contents::

当升级 GnuPG 到 2.3.2 后，会发现其无法识别我的 yubikey，经过一系列检查后发现，是与 yubikey-manager 的依赖 pcsc-lite 冲突了，以下是详细说明。

解决方法
============================================

将以下配置写入 :file:`${GNUPGHOME}/scdaemon.conf` （默认位于： :file:`~/.gnupg/scdaemon.conf` ）

..code-block::

  disable-ccid

或者在配置 gnupg 时，添加 :code:`--disable-ccid-driver` 参数。总之就是要在运行 gpg-agent 时禁用 ccid 就行了（效果和 2.2 版本一样）。

当然，也可以结束 pcscd 进程，不过这样会导致 ykman 的一些功能无法使用（OTP，PIV 之类）。

原因
============================================

.. PELICAN_END_SUMMARY

当安装使用了 yubikey-manager 后（即有了 ykman 这个命令），由于其依赖 pcsc-lite ，后台会运行 pcscd 这个服务，其会接管 yubikey 的通讯，导致 gpg-agent 使用 ccid 驱动无法获取到需要的设备，从而出现报错::

  gpg: selecting card failed: No such device
  gpg: OpenPGP card not available: No such device

如果给 :file:`scdaemon.conf` 添加如下配置::

  debug-all
  debug-level guru
  log-file /tmp/scd.log
  debug-ccid-driver
  verbose
  verbose
  verbose

后，查看日志 :file:`/tmp/scd.log` 会发现其对应的问题是 :code:`usb_claim_interface failed: -6` ，查 `源码`_ 可知真实原因是设备繁忙。

而 2.2 的 GnuPG 在 CCID 驱动获取信息失效后会回退使用 PC/SC 驱动来获取信息。这两个版本的区别，目前不知道这是特意为之，还是 2.3.2 的 BUG。

.. note::

    这里我还有一个问题，使用 GnuPG 2.3.2 的时候，无论通过 CCID 还是 PC/SC 都无法正确获取 yubikey 版本号。 2.2.29 是可以正常获取的。

起因
============================================

至于为何需要升级到并不稳定的 2.3.2 版本，是因为 2.2 这个大版本不支持多 yubikey 的识别，2.3 开始支持了，且看到 `开发者说`_ 并没有 backport 的打算，没办法才只能升级。希望 2.3 赶紧稳定吧。


.. _`源码`: https://github.com/libusb/libusb/blob/5c89594f64ed5a14470d9965e558fd9aee1fd42c/libusb/libusb.h#L1067
.. _`开发者说`: https://dev.gnupg.org/T4620
