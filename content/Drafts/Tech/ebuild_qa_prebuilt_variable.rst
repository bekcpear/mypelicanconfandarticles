=============================================================================
Gentoo ebuild 文件内的 QA_PREBUILT 变量
=============================================================================

:slug: ebuild_qa_prebuilt_variable
:date: 2021-01-07 17:42
:lang: zh_hans
:color: #463c65
:tags: gentoo, portage, ebuild, QA
:mykeywords: gentoo,portage,ebuild,QA,strip,restrict
:description: 这是一篇对 Gentoo ebuild 文件内 QA_* 变量进行简单剖析的文章，以助于理解如何设置这些变量。
:status: draft
:summary:

.. contents::

起因是打了一个 Gentoo 上 QQ 音乐的包，然后最开始被提示了 QA 警告，于是一步步琢磨；后来参考了 :gepkg:`www-client/google-chrome` 的 ebuild 文件，并浅析了一下 ebuild 源码后，才逐渐理解了 portage 上的 QA 系统是如何检测包质量的。所以写下以下内容以强化记忆。

.. PELICAN_END_SUMMARY

原始问题
==========================

先附上 `最原始的 ebuild 文件链接`_ ，当使用此 ebuild 安装 QQ 音乐时，会在 src_install 阶段完成后报 QA 报警，如下：

.. code-block::

  * QA Notice: Pre-stripped files found:
  * /opt/qqmusic-bin/qqmusic
  * /opt/qqmusic-bin/libGLESv2.so
  * /opt/qqmusic-bin/libEGL.so
  * /opt/qqmusic-bin/libffmpeg.so
  * /opt/qqmusic-bin/libvk_swiftshader.so
  * /opt/qqmusic-bin/crashpad_handler
  * /opt/qqmusic-bin/swiftshader/libGLESv2.so
  * /opt/qqmusic-bin/swiftshader/libEGL.so
  strip: x86_64-pc-linux-gnu-strip --strip-unneeded -N __gentoo_check_ldflags__ -R .comment -R .GCC.command.line -R .note.gnu.gold-version
    /opt/qqmusic-bin/chrome-sandbox

原因就如提示的一样，于是我对此 ebuild 添加了 :code:`strip` 的限制，就没有报警了；但后来看到 google-chrome 的 ebuild 文件里有一个 QA_PREBUILT 的变量，就开始好奇其作用。

如何理解
==========================

我先去查询了对应的 `开发手册上的解释`_ ，如下：

  **QA_PREBUILT**
  This should contain a list of file paths, relative to the image directory, of files that are pre-built binaries. Paths listed here will be appended to each of the QA_* variables listed below. The paths may contain fnmatch-like patterns which will be internally translated to regular expressions for the QA_* variables that support regular expressions instead of fnmatch patterns. The translation mechanism simply replaces "*" with ".*".


.. _`最原始的 ebuild 文件链接`: https://github.com/bekcpear/ryans-repos/blob/7c42f0eff1f129af0ec0cecc1dc0b72e16d6c279/media-sound/qqmusic-bin/qqmusic-bin-1.0.5.ebuild
.. _`开发手册上的解释`: https://devmanual.gentoo.org/eclass-reference/ebuild/index.html#lbAG
