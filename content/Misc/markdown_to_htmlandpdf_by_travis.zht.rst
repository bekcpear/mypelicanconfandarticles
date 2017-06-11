======================================================================
通過travis自動轉換markdown格式為html/pdf格式
======================================================================

:slug: markdown_to_htmlandpdf_by_travis
:lang: zht
:date: 2016-06-10 18:33
:modified: 2017-06-09 13:55
:tags: pandoc, travis

.. contents::

[2017年6月9號標記：遷移到了新的部落格，這套方案就不再使用了]

本文是關於通過pandoc轉換markdown格式為html和pdf的，並由 travis-ci.org 自動編譯轉換生成到Github上。目的是因為我的主頁目前沒有富文字編輯器，使用markdown寫文章是一個不錯的選擇，轉換後再把html程式碼通過後臺釋出即可。因為都沒有接觸過類似的轉換，所以花了很多時間，感覺必須要整理一下的。


必要的幾個條件
============================================================

* 符合規則的 `markdown <https://daringfireball.net/projects/markdown/syntax>`_ 檔案
* `pandoc <http://pandoc.org/installing.html>`_ （提供基本轉換環境）
* texlive & texlive-xetex & texlive-xetex-extra（轉換為pdf）
* `中文字型 <https://wiki.ubuntu.com.cn/%E5%AD%97%E4%BD%93>`_
* 建立Makefile檔案以實現批量轉換
* travis-ci.org的幫助（提供了Ubuntu12.04.5LTS的虛擬化編譯平臺）

安裝基本的轉換工具
============================================================

針對Ubuntu12.04,5下安裝pandoc如果使用cabal處理依賴關係總是出現版本不符合的問題，不知道如何解決，反而直接下載 `deb包 <https://github.com/jgm/pandoc/releases/latest>`_ 來安裝卻非常簡單，適合travis-ci虛擬機器環境：

.. code-block:: shell-session

  wget https://github.com/jgm/pandoc/releases/download/1.17.1/pandoc-1.17.1-2-amd64.deb
  sudo dpkg -i pandoc-1.17.1-2-amd64.deb

本機電腦使用Gentoo安裝依賴關係處理非常好。

使pandoc支援中文pdf轉換
============================================================

在一知半解的情況下，我使用xelatex這個引擎為Pandoc提供pdf轉換中文支援，Ubuntu12.04.5LTS需要 :code:`texlive-xetex` :code:`texlive-latex-extra` 這兩個包，安裝這兩個包需要新增 :code:`texlive-backports/ppa` 這個庫。

.. code-block:: shell-session

  sudo apt-get install python-software-properties #這個在Travis下是不需要的
  sudo add-apt-repository ppa:texlive-backports/ppa
  sudo apt-get update
  sudo apt-get install texlive-xetex texlive-latex-extra

預設情況下，轉換中文時會出現不顯示中文字型的情況，那是因為pandoc下的XeLaTeX模版沒有預設設定中文，需要做如下的新增， `完整的模版 <https://github.com/Bekcpear/bekcpear.articlemake/blob/master/template.tex>`_ ：

:: 

  \usepackage{fontspec}         % 允許設定字型
  \usepackage{xeCJK}            % 分別設定中英文
  \setCJKmainfont{WenQuanYi Micro Hei}  % 設定中文字型，當然前提是有這個字型存在
  \setmainfont{DejaVu Sans}     % 設定英文字型 
  \setromanfont{DejaVu Sans}    % 字型
  \setmonofont{DejaVu Sans Mono}
  \linespread{1.2}\selectfont   % 行間距
  \XeTeXlinebreaklocale "zh"    % 針對中文自動換行
  \XeTeXlinebreakskip = 0pt plus 1pt % 字與字之間加入0-1pt，保證對齊
  \parindent 0em                % 段落縮排
  \setlength{\parskip}{20pt}    % 段落之間距離


`這個頁面 <https://en.wikibooks.org/wiki/LaTeX>`_ 有關於LaTeX的一些語法結構。

通過hypersetup可以設定轉換之後pdf的一些屬性，比如作者、標題、標籤等：

::

  \hypersetup{breaklinks=true,
              bookmarks=true,
              pdfauthor={$author-meta$},
              pdftitle={$title-meta$},
              pdfsubject={$subject-meta$},
              pdfkeywords={$keywords-meta$},
              colorlinks=true,
              urlcolor=$if(urlcolor)$$urlcolor$$else$blue$endif$,
              linkcolor=$if(linkcolor)$$linkcolor$$else$magenta$endif$,
              pdfborder={0 0 0}}

如何使用Makefile
============================================================

可以參考的一個說明是 `這個 <https://iccce.co/s/0njSzyO9OGxp3Mq>`_ ，用到了裡面所寫的靜態模式、（自動化）變數和偽目標。

::

  SOURCES := $(wildcard *.md)
  OBJECTS := $(patsubst %.md, %.html, $(wildcard *.md))
  OBJECTS_PDF := $(patsubst %.md, %.pdf, $(wildcard *.md))

  all: html pdf

  html: $(OBJECTS)
  pdf: $(OBJECTS_PDF)

  $(OBJECTS): %.html: %.md
    pandoc $< -o $@ && mv *.html git/

  $(OBJECTS_PDF): %.pdf: %.md
    pandoc --template=./template.tex --latex-engine=xelatex  $< -o $@ && mv *.pdf git/

配置Travis以實現自動化轉換
============================================================

目前即使配置到了自動換轉換，也還是一個很繁瑣的過程，至少還需要複製到個人主頁後臺再貼上的一個過程，先用著吧。

Travis可以在獲取了Github相應許可權後監視Github Repository動態，每當有commit時，便會克隆對應Repository到一個虛擬環境，根據預先設定好的.travis.yml檔案下的內容進行配置和指令碼執行。

如果在Github下生成一個支援公共資源的Token，並在Travis後臺設定對應的環境變數，就可以很方便地將轉換完成的html和pdf文件push到另外一個Repository下，不重複push到原先的Repository的原因是避免無限迴圈。

一個可用的.travis.yml：

.. code-block:: cfg

  language: ruby

  rvm:
      - 2.2
          
  cache:
    directories:
      - cache

  before_install:
      - sudo add-apt-repository ppa:texlive-backports/ppa -y
      - sudo apt-get update
  
  install:
      - wget https://github.com/jgm/pandoc/releases/download/1.17.1/pandoc-1.17.1-2-amd64.deb
      - sudo dpkg -i pandoc-1.17.1-2-amd64.deb
      - sudo apt-get install ttf-wqy-microhei texlive-xetex texlive-latex-extra
  
  script:
      - git config --global user.email "$GIT_EMAIL"
      - git config --global user.name "$GIT_NAME"
      - git clone --depth 1 https://$GIT_TOKEN@github.com/Bekcpear/bekcpear.github.io git
      - pwd
      - ls -a
      - make all
      - cd git
      - ls -a
      - git config --global push.default matching
      - git add -A .
      - git commit -m "update from travis" 
      - git push --quiet
  
  after_success:
      - echo 'Welcome to my home page: https://bekcpear.io'

參考
============================================================

* `farseerfc/farseerfc/.travis.yml <https://github.com/farseerfc/farseerfc/blob/master/.travis.yml>`_
* `如何在Linux下使用Markdown進行文件工作 <http://www.ituring.com.cn/article/10044>`_
* `LaTeX/Colors <https://en.wikibooks.org/wiki/LaTeX/Colors>`_
* `Markdown語法中文 <http://wowubuntu.com/markdown/>`_
* `關於一個xelatex的tightlist的報錯 <https://segmentfault.com/q/1010000002974818>`_
