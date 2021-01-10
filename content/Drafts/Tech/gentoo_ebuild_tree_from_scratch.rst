===========================================================
从零构建及维护 Gentoo Linux EBUILD 树
===========================================================

:slug: gentoo_ebuild_tree_from_scratch
:date: 2020-12-18 17:30
:lang: zh_hans
:color: #4D4371
:tags: gentoo, ebuild, portage
:mykeywords: gentoo,linux,ebuild,portage,fromscratch,从零开始,同步,安全性
:description: 这是一篇关于从零构建及维护 Gentoo Linux ebuild 树系统以用于同步 portage 仓库及其它的文章
:noindent: true
:status: draft
:summary:

.. contents::

关于如何创建， Gentoo 官方 wiki 有完整的 `创建教程`_ ，本文不会重复表述。这篇文章的重点会放在描述相对其它同步方式的优缺点及安全性，脚本的使用以更便捷的同步，以及自己的一些理解上。

.. PELICAN_END_SUMMARY

相对优缺点
=====================================

Gentoo Linux 的 portage 仓库目前最常用的日常同步方式有三种：

1. 以 rsync 方式同步完整的 ebuild 树
2. 以 git 方式同步完整的 ebuild 树
3. 以 git 方式分别同步需要的 git 仓库，然后自己创建 cache 以维护 ebuild 树

*安装 Gentoo 的时候，为了可以快速下载一个完整 portage 仓库，一般都使用 webrsync 方式下载一个大的 tar 包后解压，这里不比较这个方式，因为其同步延迟很高，不会用于日常同步。*




.. _`创建教程`: https://wiki.gentoo.org/wiki/Gentoo_ebuild_tree_from_scratch
