==================================================
我的笔记
==================================================

:slug: my_note
:date: 2021-05-16 01:20
:modified: 2021-05-16 01:20
:lang: zh_hans
:color: #1C1C1C
:tags: note
:mykeywords: note
:description: 我的笔记，很杂乱
:noindent: true
:status: draft
:summary:

.. contents::

我的笔记，很杂乱，不适用于阅读。

.. PELICAN_END_SUMMARY


::

  git rebase [-i | --interactive] [<options>] [--exec <cmd>] [--onto <newbase> | --keep-base] [<upstream> [<branch>]]
  git rebase [-i | --interactive] [<options>] [--exec <cmd>] [--onto <newbase>] --root [<branch>]
  git rebase (--continue | --skip | --abort | --quit | --edit-todo | --show-current-patch)

当上游有了高于当前提交的更新时，为了避免日志里面出现 merge upstream 这种日志时，可以基于当前上游的提交， rebase 本地的提交，使得日志更清晰。

<branch> --> used to automatic switch before rebase

<upstream> --> used to specify the base point?? default to `branch.<name>.remote/merge`, and add `--fork-point` option by default

--root --> ???? ==> 为当前分支的所有提交 rebase，如果这里用 --onto 的话，那么与 onto 到的分支相同的提交内容会被忽略。等


这一段太迷糊了：
  The current branch is reset to <upstream>, or <newbase> if the --onto option was supplied. This has the exact
  same effect as git reset --hard <upstream> (or <newbase>). ORIG_HEAD is set to point at the tip of the branch
  before the reset.
怎么尝试 这个 --onto 都没有效果啊，-->> 看起来无效的原因是，这里解释的是中间步骤，即， reset 到这个指定的点后，再继续后面的操作。

那么大致的流程就是，

1. 先确定当前的分支（有 <branch> 指定则切过去，否则就是当前分支）
2. 然后确定基准的分支，即上游分支，或者当前分支的最早的空提交
3. 然后以这个基准分支，来算差异提交
4. 把这些差异提交放到一个临时的空间下
5. 把当前分支 reset --hard 到上述基准分支（这里可以利用 --onto 选项，改变 reset 到的分支或者提交）
6. 依次把临时空间下的提交，一个接一个提交到当前分支下，这里会忽略相同内容的补丁
7. 如果发现提交冲突，那么会提示，需要人工介入处理，修复好后 git add <file> 后 git --continue 或者就干脆 git --skip 略过这些个修改
   （在 rebase 过程中，可以通过 git --abort 来中断 rebase 然后恢复到 rebase 前的状态）

还可以通过这样的命令 `git rebase --onto topicA~5 topicA~3 topicA` 把

E---F---G---H---I---J  topicA

rebase 成

E---H'---I'---J'  topicA

这样


---------------------

DRI DRM Mesa Vulkan X-Server wayland DDX DIX KMS FRAMEBUFFER 关系

Compositor????


::

  (Application)
  ====================================
      X-Server Wayland
  ------------------------------------
      Mesa(Vulkan,openGL)
  ------------------------------------
      DDX DIX
  ====================================
  (Kernel)  DRM KMS
  ====================================
  (Hardware) Framebuffer


------------------------

gcc/g++

禁用编译器扩展：
  You can disable compiler extensions by adding the -pedantic-errors flag to the compile command line.

提高警告等级：
  Add the following flags to your command line: -Wall -Weffc++ -Wextra -Wsign-conversion

把警告当作错误：
  Add the following flag to your command line: -Werror

指定版本的标准号：
  For GCC/G++, you can pass compiler flags -std=c++11, -std=c++14, -std=c++17, or -std=c++2a to enable C++11/14/17/2a support respectively.

C++ 里的变量初始化，更倾向于使用 `int a{ 5 }` 这样的列表初始化的形式
与复制初始化 `int a = 5` 和直接初始化 `int a( 5 )` 不同，当列表初始化的初始化值类型与声明类型不同时，会报错，比如::

  int a = 4.5  //a=4
  int a( 4.5 ) //a=4
  int a{ 4.5 } //error

推荐使用列表初始化。

在非特殊情况下，最好是在声明变量时便对其进行初始化。

一个额外的可用于检测输入字符的 C++ 库： https://pdcurses.org/


