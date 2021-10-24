==============================================================
记录把 service worker 切换到由 Workbox 生成的过程 【流水帐】
==============================================================

:slug: switch-to-workbox
:date: 2021-10-24 17:39
:lang: zh_hans
:color: #E8710A
:tags: frontend, service-worker, workbox, javascript
:mykeywords: frontend,前端,service-worker,workbox,sw-precache
:description: 记录把 service worker 切换到 Workbox
:noindent: true
:summary:

.. contents::

我把网站的 service worker 从 sw-precache 迁移到了 Workbox ，记录一下过程。

sw-precache 是 Google 的一个实验性项目，也是 Workbox 的前身之一，之前一直用的它来生成网站的 service worker 文件，可即使对于我这个挺简单的站点，用它现在也有点不够用，比如之前我是缓存我的所有指定页面，以备离线使用，但是我现在我觉得不妥，只缓存访问页更好；再比如以前每次访问的时候都是先获取的离线内容，再尝试更新在线内容，我现在也觉得不好，应该根据内容的不同来判定先访问哪里的内容，而达成这些需要做很多的工作才能满足，就直接换了。

下面说说过程..

.. PELICAN_END_SUMMARY

对于未系统化了解过 JS 项目管理工具的我来说，看 Workbox 的简介我是懵的，什么支持通过 Javascript 模块来使用，但是 service worker 不支持模块，所以需要使用 bunlder 工具来统合成一个文件.. 在一开始，就被这个 bunlder 工具的选择和使用难到了。

介绍里列出了三种工具 webpack ， Rollup 以及 Parcel 。我先耐着性子基本浏览了一遍 Workbox 的介绍，全文没说推荐的工具。。于是我根据 tooling.report 上的通过率选择了 Parcel ，跟着其文档操作了一遍后发现。。 没把模块都整合进去啊，还是会需要导入外部的 js 文件，这就对 service worker 不适用了。后来又试了一下 Github 星多的 webpack .. 很满意，一下子就生成了我需要的文件。

在这个过程中，还了解到了 node.js 的项目管理文件 :file:`package.json` 里的一点基本内容，比如 :code:`devDependencies` 是用来放开发用工具的， :code:`dependencies` 则是用来放实际的项目依赖的，它好像会根据 Git 项目的环境来查找当前的项目根目录，自此，我就可以把这个项目环境当作一个独立的系统环境来对待了，然后就对其工具和依赖有了一个比较清晰的认知。

接下来就是一个比较重头的如何编写原始的 service worker 文件，我尝试复制了其 **Routing and Caching Strategies** 的示例直接使用，发现基本上满足了我的需求，这时候自己还需要额外添加的内容是离线访问未缓存页面时的 fallback 页，也根据示例直接添加了预缓存的并在缓存未获取时 fallback 到指定页的代码，也直接成功了。这时候我感叹，实在太方便了.. 我的要求好像全部达到了。

后来简单测试了一下后发现，就这样的代码是不会自动跳过新的 service worker 的 waiting 阶段的，虽然对于一些复制的 web 应用来说，它的 waiting 阶段是应该需要用户来选择是否跳过的，但对于我这个个人博客而言，不存在在访问时需要保留的内容，所以应设定为自动跳过。

参考自己以前写的 service worker 文件，把 :code:`self.skipWaiting()` 添加到 server worker 的 install 事件下后可用。考虑到需要删除之前缓存的本地数据库，同样把删除数据库的任务添加到了这个事件下。

这时候我在想，当阅读离线页面的时候，如果有一个简单的提示信息就更好了。因为 service worker 是无法获取 DOM 的，只能靠消息与其客户端（页面）进行通讯，于是我开始去找 Workbox 有没有提供类似的在抓缓存时用来和客户端通讯的功能。一开始没找到，后来发现了它可以自定义插件，而自定义插件的里面提供了一个 :code:`handlerDidComplete` 方法，介绍说它可以获取到缓存命中的状态，我经过实验后发现，给出的变量都抓不到返回的 Response 是从缓存拿到的还是网络拿到的（也可能是我没找到，不管）.. 后来我就又用了它另一个方法 :code:`fetchDidFail` （顾名思义就是从网络获取失败了后会触发的），两个一结合，前者用于提供 Resonse 的状态码（比如 200），后者用于告知客户端从网络获取失败了，这样一组合客户端就可以知道是不是从缓存获取的内容了。

但是在这个过程中，我又发现了一个问题。我的博客是静态的，不通过接收参数来获取到不同内容的，所以之前设定了获取缓存时会忽略掉任何参数，但 Workbox 会根据访问的完整 URL 来保存缓存，这样就导致了获取缓存可能获取到更旧的缓存，所以我得想办法在每次缓存保存完之后，删除我认为相同的更旧的缓存。这里就又有一个方法可以使用了， :code:`cacheDidUpdate` 同样是在自定义的插件里面，会在每次缓存被保存时触发，我在里面通过 Request 抓取了所有缓存，然后获取缓存头的 :file:`date` 消息来判断并删除更旧的缓存。

自此，切换 service worker 到 Workbox 实现完成。

*后来发现一个问题， Chrome 下测试没问题的离线页面信息提示在 Firefox 下无效.. 暂时不管了..*
