=========================================================================
Chrome 下 touch 事件 inline 元素监听不生效
=========================================================================

:slug: chrome_touch_event_bug
:date: 2020-09-15 10:48
:color: #0066cc
:tags: web, javascript, chrome
:description: 
:noindent: true
:summary:

.. contents::

昨天对博客首页进行了重新设计，使用原生 Javascript 对文章标题添加 Touch 监听事件时，因为一个疑似 BUG 导致了一系列奇葩的问题。

.. PELICAN_END_SUMMARY

代码
================================================

举例如下这个 HTML:

.. code-block:: html

  <!DOCTYPE html>
  <html lang="zh-Hans">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <style>
      body {
        height: 2000px;
        background: #666;
        padding-top: 100px;
      }
      a {
        /*display: inline-block;*/
        background: #ccc;
      }
      div {
        color: #fdfdfd;
        width: 100%;
      }
    </style>
  </head>
  <body>
    <h2>
      <a>test touch event</a>
    </h2>
    <div></div>
    <script>
      var link = document.querySelector('a');
      var divE = document.querySelector('div');
      link.addEventListener('touchstart', function(event){
        divE.innerText = 'touchstart \n';
      });    
      link.addEventListener('touchmove', function(event){
        divE.innerText += 'touchmove \n';
      });
      /*
      link.addEventListener('touchend', function(event){
        divE.innerText += 'touchend \n';
      });
      */
    </script>
  </body>
  </html>

Chrome 的迷惑行为
================================================

.. PELICAN_BEGIN_SUMMARY

以下描述发生在 Blink 引擎浏览器内，也就是一般使用的 Chrome, Chromium 浏览器及以其为基础进行开发的其它浏览器；其它浏览器如 Safari, FireFox, iOS 上的 Chrome (webkit 引擎)则不会因为以下指出的不同而差异化表现。

* 当 a 元素是默认的 inline 样式，且页面仅有 :code:`touchstart` 或者 :code:`touchmove` 监听事件，这针对 a 元素的两个事件都不会触发；
* 当继续添加 :code:`touchend` 监听事件后， :code:`touchstart` 监听事件开始触发，但 :code:`touchmove` 事件依旧不触发；
* 再次添加 :code:`pointerdown` 监听事件（应该还有其它事件也能帮助触发）， :code:`touchmove` 监听事件触发。

当把 a 元素样式改成 inline-block 或者 block 后，则一切正常。

.. PELICAN_END_SUMMARY

在线演示在这里: 
  
* `a 元素未设置 display 属性`_
* `a 元素设置 display 属性为 inline-block`_

说明
========================

因为这个问题，翻遍了好多资料，愣是没有答案，最后发现居然是个潜藏的 BUG？

先记录，随后有空继续查下资料。目前翻阅过的内容大致有以下这些：

* https://developer.mozilla.org/en-US/docs/Web/API/Document/touchmove_event
* https://stackoverflow.com/questions/50792027/touchmove-event-not-firing-on-google-chrome-for-android
* https://stackoverflow.com/questions/17725667/touchmove-event-not-always-triggered-on-chrome-for-android
* https://stackoverflow.com/questions/54493182/touchmove-events-stopped-working-in-chrome-72-and-latest-webkit
* https://blog.wilsonpage.co.uk/touch-events-in-chrome-android/
* https://stackoverflow.com/questions/21761514/android-browsers-not-handling-touchmove-events-correctly
* https://developers.google.com/web/updates/2017/01/scrolling-intervention
* https://docs.google.com/document/d/1sfUup3nsJG3zJTf0YR0s2C5vgFTYEmfEqZs01VVj8tE/mobilebasic#h.2hod15pdgn0e
* https://stackoverflow.com/questions/26478267/touch-move-getting-stuck-ignored-attempt-to-cancel-a-touchmove
* https://developers.google.com/web/updates/2014/05/A-More-Compatible-Smoother-Touch
* https://developers.google.com/web/fundamentals/design-and-ux/input/touch
* https://www.reddit.com/r/webdev/comments/4x3b33/js_touch_why_is_my_touchmove_event_not_firing/
* https://bugs.chromium.org/p/chromium/issues/detail?id=260732
* https://developers.google.com/web/updates/2017/01/scrolling-intervention
* https://makandracards.com/makandra/51956-event-order-when-clicking-on-touch-devices

但是没一个真的有用的，仅是知道了 Chrome 对于 touch 事件默认是消极应对的，即不会触发阻断常规动作的行为，但是并不会导致事件监听不生效；对于 :code:`touchmove` 事件，第一个应该是同步触发的，可以用于阻断默认的移动，但一般不这么做，且默认情况下不允许这么做，之后的 :code:`touchmove` 事件则是异步触发的。


.. _`a 元素未设置 display 属性`: /demos/chrome_touch_event_bug_demo.html
.. _`a 元素设置 display 属性为 inline-block`: /demos/chrome_touch_event_bug_demo_block.html
