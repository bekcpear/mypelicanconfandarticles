=============================================================================
Gentoo ebuild 文件内的 QA_PREBUILT 变量
=============================================================================

:slug: ebuild_qa_prebuilt_variable
:date: 2021-01-23 19:46
:lang: zh_hans
:color: #463c65
:tags: gentoo, portage, ebuild, QA
:mykeywords: gentoo,portage,ebuild,QA,strip,restrict
:noindent: true
:description: 这是一篇对 Gentoo ebuild 文件内 QA_* 变量进行简单剖析的文章，以助于理解如何设置这些变量。
:featured_image: /nocimages/gentoo.png
:summary:

.. contents::

起因是打了一个 Gentoo 上 QQ 音乐的包，然后最开始被提示了 QA 警告，于是一步步琢磨；后来参考了 :genpkg:`www-client/google-chrome` 的 ebuild 文件，并浅析了一下 ebuild 源码后，才逐渐理解了 portage 上的 QA_* 这些变量是如何运作的。所以写下以下内容以强化记忆。

.. PELICAN_END_SUMMARY

原始问题
==========================

先附上 `最原始的 ebuild 文件链接`_ ，当使用此 ebuild 安装 QQ 音乐时，会在 src_install 阶段完成后出现 QA 报警，如下：

::

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

  Usage Notes
    | Several QA variables are provided which allow an ebuild to manipulate some of the QA checks performed by portage. Use of these variables in ebuilds should be kept to an absolute minimum otherwise they defeat the purpose of the QA checks, and their use is subject to agreement of the QA team. They are primarily intended for use by ebuilds that install closed-source binary objects that cannot be altered.
    | Note that objects that violate these rules may fail on some architectures.

  .. _`QA_PREBUILT 值会自动添加到其它 QA_* 变量`:

  QA_PREBUILT
    This should contain a list of file paths, relative to the image directory, of files that are pre-built binaries. Paths listed here will be appended to each of the QA_* variables listed below. The paths may contain fnmatch-like patterns which will be internally translated to regular expressions for the QA_* variables that support regular expressions instead of fnmatch patterns. The translation mechanism simply replaces "*" with ".*".

这里没有非常明确说明是否是全部/彻底禁止 QA 检查（包括余项的说明也并不那么清楚），所以我就去查源码来自己解惑了。

**最后的验证结果是，彻底禁止了对应设置的 QA 检查。**

大部分的 QA 检查是在 src_install 阶段后执行的，由位于 :file:`doebuild.py` 文件中以下代码定义，

.. code-block:: python

  _post_phase_cmds = {

      "install" : [
          "install_qa_check",
          "install_symlink_html_docs",
          "install_hooks"],

对应的 :code:`install_qa_check` 函数在 :file:`misc-functions.sh` 文件中定义，其定义了会加载多个目录下设定好的检查规则，并执行，默认的检查规则位于 :file:`/usr/lib/portage/python3.8/install-qa-check.d` 目录下。

但是，还会存在有其它的 QA 检查，分布于 Portage 系统中，并直接被执行，比如针对 :file:`.desktop` 文件的检查，对应代码存在于 :file:`doebuild.py` 内，如下：

.. code-block:: python

  if desktop_file_validate and fname.endswith(".desktop") and \
      os.path.isfile(fpath) and \
      fpath_relative.startswith(xdg_dirs) and \
      not (qa_desktop_file and qa_desktop_file.match(fpath_relative.strip(os.sep)) is not None):

      desktop_validate = validate_desktop_entry(fpath)
      if desktop_validate:
          desktopfile_errors.extend(desktop_validate)

这里的 :code:`qa_desktop_file` 变量值是通过预处理的位于编译目录下的 :file:`build-info/QA_DESKTOP_FILE` 文件内容创建的一个正则表达式，来判断是否需要对该文件做 QA 检测。而这个文件，是根据软件的 :file:`.ebuild` 文件内对应的 QA_* 变量在 src_install 阶段创建的。具体创建过程查阅 :file:`phase-functions.sh` 文件内的 :code:`__dyn_install()` 函数。

**到这里，回头来看对于 strip 的限制**

strip 的动作是在 :file:`estrip.sh` 脚本下定义的，该脚本的最开始有判断如下：

.. code-block:: bash

  banner=false
  SKIP_STRIP=false
  if ${RESTRICT_strip} || ${FEATURES_nostrip} ; then
    SKIP_STRIP=true
    banner=true
    ${FEATURES_installsources} || exit 0
  fi

所以当最开始，我仅限制了做 strip 的动作，但是却没有限制做对应的检查时会出现一个问题，即在 :code:`installsources` 功能开启后，脚本是不会退出的，会继续执行其内的 QA 检查项目。只有设置了 QA_PRESTRIPPED 变量后，才能去掉对应文件的检查报告。

另外，这边有注意一点关于上述的 `QA_PREBUILT 值会自动添加到其它 QA_* 变量`_ 的问题，并不是所有变量都会添加 QA_PREBUILT 的值，目前（20210123）我看到的能被添加的变量只有 fnmatch 风格匹配的：

* QA_EXECSTACK
* QA_TEXTRELS
* QA_WX_LOAD

以及，替换为正则表达式匹配的：

* QA_DT_NEEDED
* QA_FLAGS_IGNORED
* QA_PRESTRIPPED
* QA_SONAME

暂完。

.. _`最原始的 ebuild 文件链接`: https://github.com/bekcpear/ryans-repos/blob/7c42f0eff1f129af0ec0cecc1dc0b72e16d6c279/media-sound/qqmusic-bin/qqmusic-bin-1.0.5.ebuild
.. _`开发手册上的解释`: https://devmanual.gentoo.org/eclass-reference/ebuild/index.html#lbAG
