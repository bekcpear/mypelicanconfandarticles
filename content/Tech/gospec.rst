==================================================
Go 编程语言规范【译】
==================================================

:slug: golang_spec
:date: 2019-02-23 03:47
:modified: 2022-03-12 14:22
:lang: zh_hans
:tags: doc, golang, 翻译
:mykeywords: golang,go,语言,规范,翻译,中文版,中文
:notoriginal: true
:license: 本文由本人独立翻译自 The Go Programming Language Specification (https://go.dev/ref/spec)，原文采用 Creative Commons Attribution 3.0 协议，文档内代码采用 BSD 协议 (https://go.dev/LICENSE)。 本文采用 Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International 许可协议，文档内代码继用相同协议，如果你需要发布本文（或衍生品），也需要注明本文原始链接 (https://bitbili.net/golang_spec.html) 及译者 cwittlut (原 bekcpear)。
:description: 最新版 Go 编程语言规范， The Go Programming Language Specification 的中文译文，译者 cwittlut (原 bekcpear)。
:summary:
:color: #007d9c
:noindent: true

.. contents::

* **对应英文原版 为 2022 年 03 月 10 日 版本：** https://go.dev/ref/spec ,
  :github:`golang/go@fe75fe3c7ae99713ed4e452ea8a4fcb589517dd9:doc/go_spec.html`
* **本文完整翻译了官方英文版，且后续会尽全力同步更新**

.. important::

  本文适用于支持泛型的 Go 1.18 及以上版本；

  对于之前的文档，请移步：
  `Go 1.17 编程语言规范 【译】`_

.. PELICAN_END_SUMMARY

* **本文唯一原始链接为** https://bitbili.net/golang_spec.html
* **源码存放在我的 Github 上：**
  :github:`bekcpear/mypelicanconfandarticles@master:/content/Tech/gospec.rst`

- *翻译中针对可能有歧义/不明确/翻译后不易于理解的单词将直接使用原词汇*
- *为了行文工整，代码块内可能使用英文表述*
- *因为学习语言需要，所以翻译*
- *有些翻译可能比较迷糊，我会在进一步学习后完善它们*
- *文中实参仅代表 argument；参数仅代表 parameter，有时候也会译为形参*
- *目前翻译还是可能存在错误，如发现请及时联系我或在下方留言*

介绍
========================================

.. PELICAN_BEGIN_SUMMARY

这是一篇 Go 编程语言的参考手册。访问 `go.dev`_ 以获取更多信息及其它文档。

Go 是一个在设计时便考虑到系统编程的通用语言。它是强类型的、带垃圾回收的且明确支持了并发编程。程序是由包来构建的，包的特性允许对其依赖进行高效管理。

语言语法紧凑且易于解释，便于如集成开发环境（IDE）这样子的自动化工具分析。

.. PELICAN_END_SUMMARY

标记法
========================================

标记法语法指定使用扩展巴科斯-瑙尔范式（EBNF）::

  Production  = production_name, "=", [ Expression ], "." .
  Expression  = Alternative, { "|", Alternative } .
  Alternative = Term, { Term } .
  Term        = production_name | token, [ "…", token ] | Group | Option | Repetition .
  Group       = "(", Expression, ")" .
  Option      = "[", Expression, "]" .
  Repetition  = "{", Expression, "}" .

:ruby:`产生式|Productions` 是由 :ruby:`术语|terms` 和如下操作符所构建的表达式（操作符排列按优先级递增的顺序）::

  |   多选一
  ()  分组
  []  零或一
  {}  零或多

小写字母的产生式名是用来标记一个词汇记号（组）的。 :ruby:`非终结符|Non-terminals` 是以驼峰命名法命名的。词汇记号（ :ruby:`终结符|terminals` ）都是使用双引号 "" 或者反引号 \`\` 包裹起来的。

:code:`a … b` 这样子的格式表示从 :code:`a` 连续到 :code:`b` 的字符集。水平省略号 :code:`…` 也会用在其它一些地方非正式地表示枚举或者不再进一步说明的代码片段。 字符 :code:`…` （与三个单独字符 :code:`...` 不同）并不是 Go 语言里的 token。

.. role:: html-role(raw)
  :format: html

.. note::
  译注： :ruby:`扩展巴科斯-瑙尔范式|extended Backus-Naur form` 是一种 :ruby:`元语法|metasyntax` 符号标记法，可以用于表示 :ruby:`上下文无关文法|Context-free grammar` 。

  针对本文简单说明，其产生式规则由非终结符和终结符所构成，左侧是一个非终结符，右侧则是该非终结符所代表的终结符和非终结符。终结符包括字母数字字符、标点符号和空格字符，其不可再分；非终结符最终指代某种序列组合的多个终结符。

  本文用到的上述未说明的范式符号说明：
  :code:`=` 定义；
  :code:`,` 级联；
  :code:`.` 表示表达式终结；
  :code:`" .. "` 表示除双引号外的终结符；
  :code:`\` .. \`` 表示除反引号外的终结符；
  :code:`? .. ?` 表示特殊序列，用于解释 EBNF 标准以外的文本。

  又注：根据维基百科 `extended Backus-Naur form`_ 上说明来看，原文的 EBNF 格式并不规范，所以我对原文表达式进行最小程度修改。更详细的 EBNF 说明可以下载 `ISO/IEC 14977:1996 PDF 压缩档`_ 查看。

  段落名若为中文且在语法标记块中使用英文书写的，均会在段落名上一并附上英文。

源代码表示
========================================

源代码是以 `UTF-8`_ 编码的 Unicode 文本。该文本并不是规范化的，所以一个单一的带重音符（附加符）的码位和由重音符（附加符）和字母所组成的相同字符不同，该相同字符结构被看成两个码位。为了简便，本文档使用非正规的术语——字符——指代源文本中的 Unicode 码位。

.. note::
  译注： 这里的 **规范化** 的含义是指，文字处理软件为了对 Unicode 字符串做比较、搜寻和排序操作而不得不考虑其等价性才做的正规化处理，参考维基百科 `Unicode 等價性`_ 。

每一个码位都是不同的，比如大写和小写的字母就是不同的字符。

实现限制：为了保证与其它工具的兼容性，编译器可能会不允许源文本中存在 NUL 字符（U+0000）。

实现限制：为了保证与其它工具的兼容性，如果一个 UTF-8 编码的字节顺序标记（U+FEFF）为源文本的第一个 Unicode 码位，编译器可能会忽略它。字节顺序标记也可能会被不允许出现在源中的任何其它位置。

字符
------------------------------------------------------------

如下术语用于表示特定的 Unicode 字符类::

  newline        = ? Unicode 码位 U+000A ? .
  unicode_char   = ? newline 以外的任意 Unicode 码位 ? .
  unicode_letter = ? 被分类为「字母」的 Unicode 码位 ? .
  unicode_digit  = ? 被分类为「数字/十进制数」的 Unicode 码位 ? .

在 `The Unicode Standard 8.0`_ 中， 4.5 节 "General Category" 定义了一套字符类别。 Go 语言把类别 Lu, Ll, Lt, Lm 或 Lo 中的字符看作 Unicode 字母，把数字类别 Nd 中的字符看作 Unicode 数字。

.. note::
  译注： Lu 为大写字母， Ll 为小写字母， Lt 为标题字母， Lm 为修饰字母， Lo 为其它字母， Nd 为十进制数字，可以在 `Compart`_ 上查到对应分类包含哪些字符。

  **但是在这里我有一个疑惑，里面明明很多字母和数字是不能用在标识符中的，为什么这里统统包含了进来，并且下文也没有额外的说明？**

  暂时不去深究，就先以通常认知来对待

字母和数字
------------------------------------------------------------

下划线字符 _ (U+005F) 被认为是一个字母。

::

  letter        = unicode_letter | "_" .
  decimal_digit = "0" … "9" .
  binary_digit  = "0" | "1" .
  octal_digit   = "0" … "7" .
  hex_digit     = "0" … "9" | "A" … "F" | "a" … "f" .

词法元素
========================================

注释
------------------------------------------------------------

注释作为程序的文档，有两种格式：

1. 行内注释从字符序列 :code:`//` 开始并在一行末尾结束。
2. 通用注释从字符序列 :code:`/*` 开始并在遇到的第一个字符序列 :code:`*/` 时结束。

注释不能开始于 `rune`_ 或 `字符串`_ 字面值或另一个注释的内部。不包含新行的通用注释就像一个空格。任何其它的注释就像一空白行。

Tokens
------------------------------------------------------------

Tokens 组成了 Go 语言的词汇表。有四个分类： *标识符* 、 *关键字* 、 *运算符和标点* 以及 *字面值* 。 *空白* 是由空格（U+0020）、水平制表（U+0009）、回车（U+000D）和新行（U+000A）所组成的，空白一般会被忽略，除非它分隔了组合在一起会形成单一 token 的 tokens. 并且，新行或者文件结尾可能会触发 `分号`_ 的插入。当把输入的内容区分为 tokens 时，每一个 token 都是可组成有效 token 的最长字符序列。

分号
------------------------------------------------------------

正式的语法使用分号 :code:`;` 作为一定数量的产生式的终结符。 Go 程序可以依据如下两条规则来省略大部分这样子的分号：

1. 输入内容被分为 tokens 时，当每一行最后一个 token 为以下 token 时，一个分号会自动插入到其后面：

   * `标识符`_
   * `整数`_ 、 `浮点数`_ 、 `虚数`_ 、 `rune`_ 或者 `字符串`_ 字面值
   * `关键字`_ :code:`break` , :code:`continue` , :code:`fallthrough` 或 :code:`return` 之一
   * `运算符和标点`_ 中的 :code:`++` , :code:`--` , :code:`)` , :code:`]` 或 :code:`}` 之一

2. 为了使复杂的语句可以占据在单一一行上，分号也可以在关闭的 :code:`)` 或者 :code:`}` 前被省略。

为了反应出惯用的使用习惯，本文档中的代码示例将参照这些规则来省略掉分号。

.. _`标识符`:

:ruby:`标识符|Identifiers`
------------------------------------------------------------

标识符用于命名程序中的实体——比如变量和类型。它是一个或者多个字母和数字的序列组合。标识符的第一个字符必须是一个字母。

::

  identifier = letter, { letter | unicode_digit } .

.. code-block:: go

  a
  _x9
  ThisVariableIsExported
  αβ

有一些标识符已经被 `预先声明`_ 了。

关键字
------------------------------------------------------------

如下关键字是保留的，不可以用作标识符。

::

  break        default      func         interface    select
  case         defer        go           map          struct
  chan         else         goto         package      switch
  const        fallthrough  if           range        type
  continue     for          import       return       var

运算符和标点
------------------------------------------------------------

如下的字符序列用于代表 `运算符`_ （包括了 `赋值运算符`_ ）和标点::

  +    &     +=    &=     &&    ==    !=    (    )
  -    |     -=    |=     ||    <     <=    [    ]
  *    ^     *=    ^=     <-    >     >=    {    }
  /    <<    /=    <<=    ++    =     :=    ,    ;
  %    >>    %=    >>=    --    !     ...   .    :
       &^          &^=          ~

.. _`整数`:

:ruby:`整数字面值|Integer literals`
------------------------------------------------------------

整数字面值是用来代表整数 `常量`_ 的数字序列。可用一个可选前缀来设置非十进制数： :code:`0b` 或 :code:`0B` 代表二进制， :code:`0`, :code:`0o`, :code:`0O` 代表八进制， :code:`0x` 或 :code:`0X` 代表十六进制。单独的 :code:`0` 被视作十进制零。在十六进制数字面值中，字母 a 到 f 以及 A 到 F 代表数字值 10 到 15 。

为了可读性，下划线字符 :code:`_` 可以出现在基本前缀之后或者连续的数字之间；这样的下划线不改变字面值的值。

::

  int_lit        = decimal_lit | binary_lit | octal_lit | hex_lit .
  decimal_lit    = "0" | ( "1" … "9" ), [ [ "_" ], decimal_digits ] .
  binary_lit     = "0", ( "b" | "B" ), [ "_" ], binary_digits .
  octal_lit      = "0", [ "o" | "O" ], [ "_" ], octal_digits .
  hex_lit        = "0", ( "x" | "X" ), [ "_" ], hex_digits .

  decimal_digits = decimal_digit, { [ "_" ], decimal_digit } .
  binary_digits  = binary_digit, { [ "_" ], binary_digit } .
  octal_digits   = octal_digit, { [ "_" ], octal_digit } .
  hex_digits     = hex_digit, { [ "_" ], hex_digit } .

.. code-block:: go

  42
  4_2
  0600
  0_600
  0o600
  0O600       // 第二个字符是大写字母 'O'
  0xBadFace
  0xBad_Face
  0x_67_7a_2f_cc_40_c6
  170141183460469231731687303715884105727
  170_141183_460469_231731_687303_715884_105727

  _42         // 这是一个标识符，而不是一个整数字面值
  42_         // 无效: _ 必须分隔连续数字
  4__2        // 无效: 一次只能有一个 _
  0_xBadFace  // 无效: _ 必须分隔连续数字

.. _`浮点数`:

.. _`浮点数字面值`:

:ruby:`浮点数字面值|Floating-point literals`
------------------------------------------------------------

浮点数字面值是浮点数 `常量`_ 的十进制或十六进制表示。

十进制的浮点数字面值由一个整数部分（十进制数字），一个小数点，一个小数部分（十进制数字）和一个指数部分（ :code:`e` 或 :code:`E` 后紧跟着带或者不带符号且为十进制的数字）。整数部分和小数部分其中之一可以省略；小数点和指数部分其中之一可以省略。指数值 exp 以 :math:`10^exp` 来缩放 :ruby:`有效数字|mantissa` （整数和小数部分）。

.. note::
  译注： "An exponent value exp scales the mantissa (integer and fractional part) by :math:`10^exp` ."
  这里的 "mantissa" 存在争议，目前 IEEE 使用的是 "significand" 一词，维基百科 `Talk:Significand`_ 整理了相关讨论。

十六进制浮点数字面值由一个 0x 或 0X 前缀，一个整数部分（十六进制数字），一个小数点，一个小数部分（十六进制数字）和一个指数部分（ :code:`p` 或 :code:`P` 后紧跟着带或者不带符号且为十六进制的数字）。整数部分和小数部分其中之一可以省略；小数点也可以省略，但是指数部分是必须的。（这个语法匹配 IEEE 754-2008 §5.12.3 章所说的。）指数值 exp 以 :math:`2^exp` 来缩放有效数字（整数和小数部分）。

为了可读性，下划线字符 :code:`_` 可以出现在基本前缀之后或是连续的数字之间；这样的下划线不会改变字面值的值。

::

  float_lit         = decimal_float_lit | hex_float_lit .

  decimal_float_lit = decimal_digits, ".", [ decimal_digits ], [ decimal_exponent ] |
                      decimal_digits, decimal_exponent |
                      ".", decimal_digits, [ decimal_exponent ] .
  decimal_exponent  = ( "e" | "E" ), [ "+" | "-" ], decimal_digits .

  hex_float_lit     = "0", ( "x" | "X" ), hex_mantissa, hex_exponent .
  hex_mantissa      = [ "_" ], hex_digits, ".", [ hex_digits ] |
                      [ "_" ], hex_digits |
                      ".", hex_digits .
  hex_exponent      = ( "p" | "P" ), [ "+" | "-" ], decimal_digits .

.. code-block:: go

  0.
  72.40
  072.40       // == 72.40
  2.71828
  1.e+0
  6.67428e-11
  1E6
  .25
  .12345E+5
  1_5.         // == 15.0
  0.15e+0_2    // == 15.0

  0x1p-2       // == 0.25
  0x2.p10      // == 2048.0
  0x1.Fp+0     // == 1.9375
  0X.8p-0      // == 0.5
  0X_1FFFP-16  // == 0.1249847412109375
  0x15e-2      // == 0x15e - 2 （整数减法）

  0x.p1        // 无效的： 有效数字无数字
  1p-2         // 无效的： p 指数需要十六进制有效数字
  0x1.5e-2     // 无效的： hexadecimal mantissa requires p exponent
  1_.5         // 无效的： _ 必须分隔连续的数字
  1._5         // 无效的： _ 必须分隔连续的数字
  1.5_e1       // 无效的： _ 必须分隔连续的数字
  1.5e_1       // 无效的： _ 必须分隔连续的数字
  1.5e1_       // 无效的： _ 必须分隔连续的数字

.. _`虚数`:

:ruby:`虚数字面值|Imaginary literals`
------------------------------------------------------------

虚数字面值表示复数 `常量`_ 的虚部。它由 `整数`_ 或者 `浮点数`_ 字面值紧跟着一个小写的字母 :code:`i` 组成。这个虚数字面值的值为对应整数或者浮点数字面值的值乘以虚数单位 *i* 。

::

  imaginary_lit = (decimal_digits | int_lit | float_lit), "i" .

考虑到向后兼容，完全由十进制数字（可能存在下划线）组成的虚数字面值的整数部分被作为十进制整数，即使其以 0 开头也不例外。

.. code-block:: go

  0i
  0123i         // == 123i 为了向后兼容
  0o123i        // == 0o123 * 1i == 83i
  0xabci        // == 0xabc * 1i == 2748i
  0.i
  2.71828i
  1.e+0i
  6.67428e-11i
  1E6i
  .25i
  .12345E+5i
  0x1p-2i       // == 0x1p-2 * 1i == 0.25i

.. _`rune`:

:ruby:`Rune 字面值|Rune literals`
------------------------------------------------------------

Rune 字面值代表了一个 rune `常量`_ ，一个确定了 Unicode 码位的整数值。 Rune 字面值是由一个或者多个字符以单引号包裹来表示的，就像 :code:`'x'` 或 :code:`'\\n'` 。在引号内，除了新行和未被转义的单引号外的任何字符都可能出现。被单引的字符表示的是该字符的 Unicode 值，不过以反斜杠开头的多字符序列会以不同的格式来编码 Unicode 值。

这是在引号内代表单一字符的最简单的形式；因为 Go 源文件是使用 UTF-8 编码的 Unicode 字符，多个 UTF-8 编码的字节可以表示为一个单一整数值。比如： :code:`'a'` 用一个字节代表了字面值 :code:`a` ， Unicode U+0061，值 :code:`0x61` ；但 :code:`'ä'` 用了两个字节（ :code:`0xc3 0xa4` ）代表了字面值 :code:`a 分音符` ， Unicode U+00E4，值 :code:`0xe4` 。

几个反斜杠转义允许任意值被编码为 ASCII 文本。有四种方法将整数值表达为数值常量： :code:`\\x` 紧跟着两个十六进制数； :code:`\\u` 紧跟着四个十六进制数； :code:`\\U` 紧跟着八个十六进制数；一个单独的反斜杠 :code:`\\` 紧跟着三个八进制数。每一种情况下的字面值的值都是对应基础上该数所表示的值。

虽然这些表示的最终都是一个整数，但它们有不同的有效范围。八进制转义必须表示 0 到 255 之间的值。十六进制转义满足条件的要求会因为构造不同而不同。 :code:`\\u` 和 :code:`\\U` 代表了 Unicode 码位，所以在这里面有一些值是非法的，尤其是那些超过 :code:`0x10FFFF` 的和代理了一半的（译注：查阅「 UTF-16 代理对」进行深入阅读）。

在反斜杠后，某些单字符的转义代表了特殊的值::

  \a   U+0007 警报或蜂鸣声
  \b   U+0008 退格
  \f   U+000C 换页
  \n   U+000A 换行或新行
  \r   U+000D 回车
  \t   U+0009 水平制表
  \v   U+000B 垂直制表
  \\   U+005C 反斜杠
  \'   U+0027 单引号（只在 rune 字面值中转义才有效）
  \"   U+0022 双引号（只在字符串字面值中转义才有效）

所有其它以反斜杠开头的序列在 rune 字面值中都是非法的。

::

  rune_lit         = "'", ( unicode_value | byte_value ), "'" .
  unicode_value    = unicode_char | little_u_value | big_u_value | escaped_char .
  byte_value       = octal_byte_value | hex_byte_value .
  octal_byte_value = `\`, octal_digit, octal_digit, octal_digit .
  hex_byte_value   = `\`, "x", hex_digit, hex_digit .
  little_u_value   = `\`, "u", hex_digit, hex_digit, hex_digit, hex_digit .
  big_u_value      = `\`, "U", hex_digit, hex_digit, hex_digit, hex_digit,
                               hex_digit, hex_digit, hex_digit, hex_digit, .
  escaped_char     = `\`, ( "a" | "b" | "f" | "n" | "r" | "t" | "v" | `\` | "'" | `"` ) .

.. code-block:: go

  'a'
  'ä'
  '本'
  '\t'
  '\000'
  '\007'
  '\377'
  '\x07'
  '\xff'
  '\u12e4'
  '\U00101234'
  '\''         // 包含了一个单引号字符的 rune 字面值
  'aa'         // 非法：字符太多
  '\xa'        // 非法：十六进制数字太少
  '\0'         // 非法：八进制数字太少
  '\uDFFF'     // 非法：只代理了一半
  '\U00110000' // 非法：无效的 Unicode 码位

.. _`字符串`:

:ruby:`字符串字面值|String literals`
------------------------------------------------------------

字符串字面值代表了通过串联字符序列而获得的字符串 `常量`_ 。它有两种形式： :ruby:`原始|raw` 字符串字面值和 :ruby:`解释型|interpreted` 字符串字面值。

原始字符串字面值是在反引号之间的字符序列，就像 :code:`\`foo\`` 。
除了反引号外的任何字符都可以出现在该引号内。
原始字符串字面值的值是由在引号内未被解释过的（隐式 UTF-8 编码的）字符所组成的字符串；
尤其是，反斜杠在这里没有特殊意义，且字符串可以包含新行（LF）。
原始字符串字面值中的回车字符（ :code:`'\\r'` ）会被从原始字符串值中所丢弃。

.. note::
  译注： 经测试，手动输入的 :code:`'\\r'` 字符是可以正常显示为 :code:`'\\r'`
  的（毕竟反斜杠在这里无意义），那么理解下来，丢弃的是键盘键入的回车（CR，比如 Windows 上）。

解释型字符串字面值是在双引号之间的字符序列，就像 :code:`"bar"` 。除了新行和未被转义的双引号之外的所有字符都可以出现在该引号内。引号之间的文本组成了字符串字面值的值，反斜杠转义以及限制都和 `rune`_ 字面值一样（不同的是，在解释型字符串字面值中， :code:`\\'` 是非法的， :code:`\\"` 是合法的）。三个数字的八进制数（ :code:`\\nnn` ）和两个数字的十六进制数（ :code:`\\xnn` ）的转义代表着所生成字符串的独立字节；所有其它的转义代表了单独字符的 UTF-8 编码（可能是多字节的）。因此字符串字面值内的 :code:`\\377` 和 :code:`\\xFF` 代表着值为 :code:`0xFF=255` 的单一字节，而 :code:`ÿ`, :code:`\\u00FF`, :code:`\\U000000FF` 和 :code:`\\xc3\\xbf` 代表着字符 U+00FF 以 UTF-8 编码的双字节 :code:`0xc3 0xbf` 。

::

  string_lit             = raw_string_lit | interpreted_string_lit .
  raw_string_lit         = "`", { unicode_char | newline }, "`" .
  interpreted_string_lit = `"`, { unicode_value | byte_value }, `"` .

.. code-block:: go

  `abc`                // 同 "abc"
  `\n
  \n`                  // 同 "\\n\n\\n"
  "\n"
  "\""                 // 同 `"`
  "Hello, world!\n"
  "日本語"
  "\u65e5本\U00008a9e"
  "\xff\u00FF"
  "\uD800"             // 非法: 代理了一半
  "\U00110000"         // 非法: 无效的 Unicode 码位

以下这些例子都代表着相同的字符串：

.. code-block:: go

  "日本語"                                 // UTF-8 输入文本
  `日本語`                                 // 以原始字面值输入的 UTF-8 文本
  "\u65e5\u672c\u8a9e"                    // 明确的 Unicode 码位
  "\U000065e5\U0000672c\U00008a9e"        // 明确的 Unicode 码位
  "\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e"  // 明确的 UTF-8 字节

当源代码以两个码位来代表一个字符，比如包含一个重音符和一个字母的组合形式，如果是在 rune 字面值中的话会使得结果出错（因为其并不是一个单一码位），而如果是在字符串字面值中的话则会显示为两个码位。

.. _`默认类型`:

.. _`非类型化的字符串`:

常量
========================================

常量有 *布尔值常量* 、 *rune 常量* 、 *整数常量* 、 *浮点数常量* 、 *复数常量* 和 *字符串常量* 。 Rune、整数、浮点数和复数常量统称为数值常量。

一个常量的值是由如下所表示的： `rune`_ 、 `整数`_ 、 `浮点数`_ 、 `虚数`_ 或 `字符串`_ 字面值；表示常量的标识符； `常量表达式`_ ；结果为常量的 `变量转换`_ ；或者一些内置函数所生成的值，这些内置函数比如应用于 `某些值`_ 的 :code:`unsafe.Sizeof` ，应用于 `一些表达式`_ 的 :code:`cap` 或 :code:`len` ，应用于复数常量的 :code:`real` 和 :code:`imag` 以及应用于数值常量的 :code:`complex` 。布尔值是由预先声明的常量 :code:`true` 和 :code:`false` 所代表的。预先声明的标识符 `iota`_ 表示一个整数常量。

通常，复数常量是 `常量表达式`_ 的一种形式，会在该节讨论。

数值常量代表任意精度的确切值，而且不会溢出。因此，没有常量表示 IEEE-754 负零，无穷，以及非数字值。

.. note::
  译注：上面后半句应该是指的数值常量，可能没有表示清楚，因为字符串常量肯定就是非数字值。

常量可以是 `类型化的`_ 也可以是非类型化的。字面值常量， :code:`true` , :code:`false` , :code:`iota` 以及一些仅包含非类型化的恒定操作数的 `常量表达式`_ 是非类型化的。

常量可以通过 `常量声明`_ 或 `变量转换`_ 被显示地赋予一个类型，也可以在 `变量声明`_ 或 `赋值`_ 中，或作为一个操作数在 `表达式`_ 中使用时隐式地被赋予一个类型。如果常量的值不能按照所对应的类型来表示的话，就会出错。
如果类型是一个类型形参，那么常量会被转化为该类型形参的一个非常量值。

.. note::

   译注，
   【2018 年 5 月版的内容】
   比如， :code:`3.0` 可以作为任何整数类型或任何浮点数类型，而 :code:`2147483648.0`
   （相当于 :code:`1<<31` ）可以作为 :code:`float32` , :code:`float64` 或 :code:`uint32`
   类型，但不能是 :code:`int32` 或 :code:`string` 。

一个非类型化的常量有一个 *默认类型* ，当在上下文中需要请求该常量为一个类型化的值时，这个 *默认类型* 便指向该常量隐式转换后的类型，比如像 :code:`i := 0` 这样子的 `短变量声明`_ 就没有显示的类型。非类型化的常量的默认类型分别是 :code:`bool` , :code:`rune` , :code:`int` , :code:`float64` , :code:`complex128` 或 :code:`string` ，取决于它是否是一个布尔值、 rune、整数、浮点数、复数或字符串常量。

实现限制：虽然数值常量在这个语言中可以是任意精度的，但编译器可能会使用精度受限的内部表示法来实现它。也就是说，每一种实现必须：

* 使用最少 256 位来表示整数。
* 使用最少 256 位来表示浮点数常量（包括复数常量的对应部分）的小数部分，使用最少 16 位表示其带符号的二进制指数部分。
* 当无法表示一个整数常量的精度时，需要给出错误。
* 当因为溢出而无法表示一个浮点数或复数常量时，需要给出错误。
* 当因为精度限制而无法表示一个浮点数或复数常量时，约到最接近的可表示的常量。

这些要求也适用于字面值常量，以及 `常量表达式`_ 的求值结果。

变量
========================================

变量是用来放置 *值* 的存储位置。可允许的值的集是由变量 `类型`_ 所确定的。

`变量声明`_ 和对于函数参数及其结果而言的 `函数声明`_ 或 `函数字面值`_ 的签名都为命名的变量保留存储空间。调用内置函数 :code:`new` 或获取 `复合字面值`_ 的地址会在运行时为变量分配存储空间。这样子的一个匿名变量是通过（可能隐式的） `指针间接`_ 引用到的。

*结构化的* `数组`_ 、 `分片`_ 和 `结构体`_ 类型变量存在可以独立 `寻址`_ 的元素和字段。每一个这样子的元素就像一个变量。

变量的 *静态类型* （或者就叫 *类型* ）是其声明时确定好的类型，或由 :code:`new`
调用或复合字面值所提供的类型，或结构化变量的元素类型。接口类型的变量还有一个独特的 *动态*
类型，该类型是在运行时所分配给变量的值的（非接口）类型（除非那个值是预声明的标识符 :code:`nil`
，它是没有类型的）。动态类型可能会在执行过程中变化，但存储在接口变量中的值始终 `可分配`_ 为接口变量的静态类型。

.. code-block:: go

  var x interface{}  // x 是 nil，它有一个静态类型 interface{}
  var v *T           // v 的值为 nil，静态类型为 *T
  x = 42             // x 的值为 42，动态类型为 int
  x = v              // x 的值为 (*T)(nil)，动态类型为 *T

变量的值是通过引用 `表达式`_ 中的变量来检索的；它总是那个最后 `赋`_ 给变量的值。如果一个变量还没有被分配到值，那么它的值是其对应类型的 `零值`_ 。

.. _`类型化的`:

.. _`所确定的`:

.. _`命名类型`:

.. _`命名的类型`:

.. _`类型字面值`:

.. _`未命名的类型`:

类型
========================================

类型确定了一个值集（连同特定于这些值的操作和方法）。
类型可以由 *类型名* 表示（如果它有的话），如果该类型是泛型，那么其后必须紧跟一个 `类型实参`_ 。
类型也可以由已知类型组成的 *类型字面值* 指定。

::

  Type      = TypeName | TypeLit | "(", Type, ")" .
  Type      = TypeName, [ TypeArgs ] | TypeLit | "(", Type, ")" .
  TypeName  = identifier | QualifiedIdent .
  TypeArgs  = "[", TypeList, [ "," ], "]" .
  TypeList  = Type, { ",", Type } .
  TypeLit   = ArrayType | StructType | PointerType | FunctionType | InterfaceType |
              SliceType | MapType | ChannelType .

语言本身 `预先声明`_ 了一些特定的类型名。其它的命名类型则使用 `类型声明`_ 或者 `类型形参列表`_ 引入。 *复合类型* ——数组、结构体、指针、函数、接口、分片、映射和信道类型——可以由类型字面值构成。

预先声明的类型、定义好的类型以及类型形参都被称为 *命名类型* 。如果在别名声明中给出的类型是命名类型，那么该别名表示命名类型。

.. _`布尔`:

布尔类型
------------------------------------------------------------

*布尔类型* 代表以预先声明的常量 :code:`true` 和 :code:`false` 所表示的布尔真值的集合。预先声明的布尔类型为 :code:`bool` ，这是一个 `定义类型`_ 。

.. _`无符号整数`:

.. _`浮点数类型`:

.. _`整数类型`:

.. _`复数类型`:

.. _`复数`:

数字类型
------------------------------------------------------------

*整数* 、 *浮点数* 或 *复数* 类型分别代表整数、浮点数或复数值的集合。
它们被统称为 *数字类型* 。
预先声明的架构无关的数字类型有::

  uint8       无符号的  8 位整数集合（0 到 255）
  uint16      无符号的 16 位整数集合（0 到 65535）
  uint32      无符号的 32 位整数集合（0 到 4294967295）
  uint64      无符号的 64 位整数集合（0 到 18446744073709551615）

  int8        带符号的  8 位整数集合（-128 到 127）
  int16       带符号的 16 位整数集合（-32768 到 32767）
  int32       带符号的 32 位整数集合（-2147483648 到 2147483647）
  int64       带符号的 64 位整数集合（-9223372036854775808 到 9223372036854775807）

  float32     所有 IEEE-754 标准的 32 位浮点数数字集合
  float64     所有 IEEE-754 标准的 64 位浮点数数字集合

  complex64   由 float32 类型的实数和虚数部分所组成的所有复数的集合
  complex128  由 float64 类型的实数和虚数部分所组成的所有复数的集合

  byte        unit8 的别名
  rune        int32 的别名

一个 n 位整数的值是 n 位宽的，是使用 `补码`_ 来表示的。

.. note::
  译注：也就是 uint8 就是 8 位宽， int8 也是 8 位宽， int16 就是 16 位宽，以此类推；关于原码、反码和补码，这里有一篇比较： `知乎-原码、反码、补码的产生、应用以及优缺点有哪些？`_

以下是根据实现不同而有特定大小的预先声明的整数类型::

  uint     可以是 32 或 64 位
  int      和 uint 大小相同
  uintptr  一个大到足够用来存储一个指针值的未解释的比特位的无符号整数

为了避免移植性问题，除了 :code:`byte` （ :code:`unit8` 的别名）和 :code:`rune` （ :code:`int32` 的别名）外的所有数字类型都是截然不同的 `定义类型`_ 。当不同的数字类型混合在一个表达式或赋值里时，是需要显示的转换的。比如， :code:`int32` 和 :code:`int` 并不是相同的类型，就算在一个特定的架构上它们可能有相同的大小，也是如此。

字符串类型
------------------------------------------------------------

*字符串类型* 代表了字符串值的集合。一个字符串值是字节的序列（可能为空）。字节的个数被称为该字符串的长度，并且不能为负。字符串是不可变的：一旦创建好了是不可能去修改其内容的。预先声明的字符串类型是 :code:`string` ；它是一个 `定义类型`_ 。

字符串 :code:`s` 的长度可以使用内置函数 `len`_ 来发现。如果字符串是一个常量，那么长度是一个编译时常量。一个字符串的字节可以通过从 :code:`0` `索引`_ 到 :code:`len(s) - 1` 的整数来访问。获取这样子的一个元素的地址是非法的；如果 :code:`s[i]` 是一个字符串的第 :code:`i` 个字节，那么 :code:`&s[i]` 是无效的。

.. _`数组`:

.. _`数组类型`:

:ruby:`数组类型|Array types`
------------------------------------------------------------

数组是单一类型元素的有序序列，该单一类型称为元素类型。元素的个数被称为数组长度，并且不能为负值。

::

  ArrayType   = "[", ArrayLength, "]", ElementType .
  ArrayLength = Expression .
  ElementType = Type .

长度是数组类型的一部分；它必须为一个可以被 :code:`int` 类型的值所代表的非负 `常量`_ 。数组的长度 :code:`a` 可以使用内置函数 `len`_ 来发现。元素可以被从 :code:`0` `索引`_ 到 :code:`len(a) - 1` 的整数所寻址到。数组类型总是一维的，但可以被组合以形成多维类型。

.. code-block:: go

  [32]byte
  [2*N] struct { x, y int32 }
  [1000]*float64
  [3][5]int
  [2][2][2]float64  // 同 [2]([2]([2]float64))

.. _`分片`:

.. _`分片类型`:

.. _`元素类型`:

:ruby:`分片类型|Slice types`
------------------------------------------------------------

分片是针对一个底层数组的连续段的描述符，它提供了对该数组内有序序列元素的访问。分片类型表示其元素类型的数组的所有分片的集合。元素的数量被称为分片长度，且不能为负。未初始化的分片的值为 :code:`nil` 。

.. note::

  译注， 在这里 Go Specification 的描述为：

    The value of an uninitialized slice is nil.

  而 :ruby:`《Go 语言圣经》|The GO Programming Language` 里说：

    The zero-value mechanism ensures that a variable always holds a well-defined value of its type; in Go there is no such thing as an uninitialized variable."

  于是我对如下两段代码：

  .. code-block:: go

    // file: test0.go
    package main

    func main() {
      var a []int
      print(a)
    }

    // file: test1.go
    package main

    func main() {
      var a []int = nil
      print(a)
    }

  使用如下命令：

  .. code-block:: bash

    go build -o test ./test.go
    objdump -d -Mamd64 test > test.s

  分别生成对应的汇编文件后对比，发现两个文件内容除文件名外其它一致，均对变量 a 所对应的栈地址写零了；因此这里的描述实际上修正为， **“未被显式初始化过的分片会被隐式地初始化为其零值 nil”** 更恰当，下同。

::

  SliceType = "[", "]", ElementType .

分片 :code:`s` 的长度可以被内置函数 `len`_ 来发现；和数组不同的是，这个长度可能会在执行过程中改变。元素可以被从 :code:`0` `索引`_ 到 :code:`len(s) - 1` 的整数所寻址到。一个给定元素的分片索引可能比其底层数组的相同元素的索引要小。

分片一旦初始化便始终关联到存放其元素的底层数组。因此分片会与其数组和相同数组的其它分片共享存储区；相比之下，不同的数组总是代表不同的存储区域。

分片底层的数组可以延伸超过分片的末端。 *容量* 便是对这个范围的测量：它是分片长度和数组内除了该分片以外的长度的和；不大于其容量长度的分片可以从原始分片 `再分片`_ 新的来创建。分片 :code:`a` 的容量可以使用内置函数 `cap(a)`_ 来找到。

对于给定元素类型 :code:`T` 的新的初始化好的分片值可以使用的内置函数 `make`_ 来制作，
这个内置函数需要获取分片类型、指定的长度和可选的容量作为参数。使用 :code:`make` 创建的分片总是分配一个新的隐藏的数组给返回的分片值去引用。也就是，执行

::

  make([]T, length, capacity)

就像分配个数组然后 `再分片`_ 它一样来产生相同的分片，所以如下两个表达式是相等的::

  make([]int, 50, 100)
  new([100]int)[0:50]

如同数组一样，分片总是一维的但可以通过组合来构造高维的对象。数组间组合时，被构造的内部数组总是拥有相同的长度；但分片与分片（或数组与分片）组合时，内部的长度可能是动态变化的。此外，内部分片必须单独初始化。

.. _`结构体`:

.. _`字段名`:

.. _`结构体类型`:

.. _`结构体的标签`:

:ruby:`结构体类型|Struct types`
------------------------------------------------------------

结构体是命名元素的一个序列，这些元素被称为字段，每一个都有一个名字和一个类型。字段名可以被显式指定（IdentifierList）也可以被隐式指定（EmbeddedField）。在结构体中，非 `空白`_ 字段名必须是 `唯一的`_ 。

.. _`嵌入字段`:

::

  StructType    = "struct", "{", { FieldDecl, ";" }, "}" .
  FieldDecl     = (IdentifierList Type | EmbeddedField), [ Tag ] .
  EmbeddedField = [ "*" ], TypeName .
  Tag           = string_lit .

.. code-block:: go

  // 一个空的结构体
  struct {}

  // 一个有六个字段的结构体
  struct {
    x, y int
    u float32
    _ float32  // padding
    A *[]int
    F func()
  }

一个声明了类型但没有显式的字段名的字段就是 *嵌入字段* 。嵌入字段必须指定为一个类型名 :code:`T` 或者为一个到非接口类型的指针名 :code:`*T` ， 并且 :code:`T` 不是一个指针类型。这个非限定的类型名就被当作字段名。

.. code-block:: go

  // 四个类型分别为 T1, *T2, P.T3, *P.T4 的嵌入字段所组成的结构体
  struct {
    T1        // 字段名为 T1
    *T2       // 字段名为 T2
    P.T3      // 字段名为 T3
    *P.T4     // 字段名为 T4
    x, y int  // 字段名为 x 和 y
  }

以下声明是非法的，因为在一个结构体类型中，字段名必须是唯一的：

.. code-block:: go

  struct {
    T     // 与嵌入字段 *T 和 *P.T 冲突
    *T    // 与嵌入字段  T 和 *P.T 冲突
    *P.T  // 与嵌入字段  T 和   *T 冲突
  }

在结构体 :code:`x` 中，一个嵌入字段的字段或 `方法`_ :code:`f` 被称作 *promoted* ，前提是 :code:`x.f` 是一个表示那个字段或方法 :code:`f` 的合法 `选择器`_ 。

除了不能在结构体的 `复合字面值`_ 中作为字段名外， promoted 字段和结构体的普通字段一样。

给定一个结构体类型 :code:`S` 和一个 `定义类型`_ :code:`T` ， promoted 方法包含在这个结构体的方法集中的情况分为：

* 如果 :code:`S` 包含一个嵌入字段 :code:`T` ，那么 :code:`S` 和 :code:`*S` 的 `方法集`_ 都包括了接收器为 :code:`T` 的 promoted 方法。 :code:`*S` 的方法集还包括了接收器为 :code:`*T` 的 promoted 方法。
* 如果 :code:`S` 包含了一个嵌入字段 :code:`*T` ，那么 :code:`S` 和 :code:`*S` 的 `方法集`_ 都包括了接收器为 :code:`T` 或 :code:`*T` 的 promoted 方法。

字段声明可以紧跟着一个可选的字符串字面值 *标签* ，在对应的字段声明中，它将成为针对所有这个字段的属性。空的标签字符串等于没有标签。标签可以通过 `反射接口`_ 被可视化，并且可以参与到结构体的 `类型一致性`_ 中，但其它情况下都是被忽略的。

.. code-block:: go

  struct {
    x, y float64 ""  // 空的标签字面值和没有标签一样
    name string  "any string is permitted as a tag"
    _    [4]byte "ceci n'est pas un champ de structure"
  }

  // 对应时间戳协议缓冲区的结构体
  // 其标签字符串定义了协议缓冲区的字段号
  // 它们遵循了由 reflect 包所概述的转换规则
  struct {
    microsec  uint64 `protobuf:"1"`
    serverIP6 uint64 `protobuf:"2"`
  }

.. _`指针`:

.. _`指向`:

.. _`指针类型`:

:ruby:`指针类型|Pointer types`
------------------------------------------------------------

指针类型表示指向一给定类型的 `变量`_ 的所有指针的集合，这个给定类型称为该指针的 *基础类型* 。未初始化的指针的值为 :code:`nil` 。

::

  PointerType = "*", BaseType .
  BaseType    = Type .

.. code-block:: go

  *Point
  *[4]int

.. _`签名`:

.. _`variadic`:

.. _`结果参数`:

.. _`函数形参列表`:

.. _`命名的结果参数`:

:ruby:`函数类型|Function types`
------------------------------------------------------------

函数类型表示具有相同参数和结果类型的所有函数的集合。函数类型的未初始化的变量的值为 :code:`nil` 。

::

  FunctionType   = "func", Signature .
  Signature      = Parameters, [ Result ] .
  Result         = Parameters | Type .
  Parameters     = "(", [ ParameterList, [ "," ] ], ")" .
  ParameterList  = ParameterDecl, { ",", ParameterDecl } .
  ParameterDecl  = [ IdentifierList ], [ "..." ], Type .

在参数或结果的列表中，名字（IdentifierList）要么全部存在，要么全部不存在。如果存在，每个名字代表特定类型的一个条目（参数或者结果），签名中的名字是非 `空白`_ 的，且必须是 `唯一的`_ 。如果不存在，每个类型代表该类型的一个条目。参数和结果列表总是括起来的，除非只有一个未命名的结果（可以写为不使用括号括起来的类型）。

函数签名中最后的进入参数可以是以 :code:`...` 为前缀的类型。带这样一个参数的函数被称为 *variadic* （可变），它可以携带针对该形参的零或多个实参来调用。

.. code-block:: go

  func()
  func(x int) int
  func(a, _ int, z float32) bool
  func(a, b int, z float32) (bool)
  func(prefix string, values ...int)
  func(a, b int, z float64, opt ...interface{}) (success bool)
  func(int, int, float64) (float64, *[]int)
  func(n int) func(p *T)

.. _`实现的接口`:

.. _`接口类型`:

.. _`接口`:

.. _`类型元素（TypeElem）`:

.. _`类型集`:

.. _`方法名`:

.. _`能实现`:

:ruby:`接口类型|Interface types`
------------------------------------------------------------

一个接口类型定义了一个 *类型集* 。
一个接口类型的变量可以储存该接口的类型集中任意类型的值。
这样的一个类型被称为 `实现了这个接口`_ 。
接口类型的未初始化的变量的值为 :code:`nil` 。

::

  InterfaceType  = "interface", "{", { InterfaceElem, ";" }, "}" .
  InterfaceElem  = MethodElem | TypeElem .
  MethodElem     = MethodName, Signature .
  MethodName     = identifier .
  TypeElem       = TypeTerm, { "|", TypeTerm } .
  TypeTerm       = Type | UnderlyingType .
  UnderlyingType = "~", Type .

接口类型是由一个 *接口元素* 列表所指定的。接口元素可以是一个 *方法* 也可以是一个 *类型元素* ，其中类型元素是一个或多个 *类型术语* 的并集。类型术语可以是一个单一类型也可以是一个单一潜在类型。

基本接口
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

在最基本的格式下，接口指定了一个（可能为空的）方法列表。
由这样的接口所定义的类型集是实现了所有这些方法的类型的集合，其对应的 `方法集`_
完全由这个接口所指定的方法组成。那些类型集可以完全由一列方法定义的接口被称为
*基本接口* 。

.. code-block:: go

  // 一个简单的 File 接口。
  interface {
    Read([]byte) (int, error)
    Write([]byte) (int, error)
    Close() error
  }

显示地指定的方法名必须是 `唯一的`_ 且非 `空白`_ 的。

.. code-block:: go

  interface {
    String() string
    String() string  // 非法: String 不是唯一的
    _(x int)         // 非法: 方法不能是空白名
  }

多个类型可以实现一个相同的接口。比如，如果两个类型 :code:`S1` 和 :code:`S2` 有方法集

.. code-block:: go

  func (p T) Read(p []byte) (n int, err error)
  func (p T) Write(p []byte) (n int, err error)
  func (p T) Close() error

（其中 :code:`T` 代表 :code:`S1` 或 :code:`S2` ）那么 :code:`File` 接口就被 :code:`S1` 和 :code:`S2` 实现了，不管 :code:`S1` 和 :code:`S2` 是否有其它的（或共享的）方法。

接口类型集中的每一个类型都实现了这个接口。一个给定的类型可能会实现完全不同的接口。例如，所有类型都实现 *空接口* ，它代表所有类型的集合：

.. code-block:: go

  interface{}

为了方便，用预先声明的类型 :code:`any` 作为空接口的一个别名。

类似的，来看这个出现在 `类型声明`_ 中定义了一个叫做 :code:`Locker` 接口的接口规格：

.. code-block:: go

  type Locker interface {
    Lock()
    Unlock()
  }

如果 :code:`S1` 和 :code:`S2` 也实现了

.. code-block:: go

  func (p T) Lock() { … }
  func (p T) Unlock() { … }

和 :code:`File` 接口一样，它们也实现了 :code:`Locker` 接口。

嵌入接口
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

以稍微常规点的格式来说，接口 :code:`T` 可以使用（可能是限定的）接口类型名 :code:`E` 作为其接口元素。
这被叫作在 :code:`T` 中的 *嵌入* 接口 :code:`E` 。 :code:`T` 的类型集是 :code:`T`
显示声明的方法的类型集与 :code:`T` 嵌入接口的类型集的交集。换句话说，
:code:`T` 的类型集是实现了所有 :code:`T` 与 :code:`E` 显示声明的方法的类型的集合。

.. code-block:: go

  type Reader interface {
    Read(p []byte) (n int, err error)
    Close() error
  }

  type Writer interface {
    Write(p []byte) (n int, err error)
    Close() error
  }

  // ReadWriter 的方法是 Read, Write, Close
  type ReadWriter interface {
    Reader  // 在 ReadWriter 的方法集中包含 Reader 的方法
    Writer  // 在 ReadWriter 的方法集中包含 Writer 的方法
  }

当嵌入接口时， `同名`_ 方法必须拥有 `一致的`_ 签名。

.. code-block:: go

  type ReadCloser interface {
    Reader   // 在 ReadCloser 的方法集中包含 Reader 的方法
    Close()  // 非法： Reader.Close 的签名和 Close 的不同
  }

泛型接口
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

以最通用的格式来说，接口元素也可以是一个任意的类型术语 :code:`T` ，或者一个指定潜在类型为
:code:`T` 的格式为 :code:`~T` 的术语，或者术语
:html-role:`<code class="code">t<sub>1</sub>|t<sub>2</sub>|…|t<sub>n</sub></code>`
的并集。这些元素与方法规格一起启用了一个接口的类型集的精确定义，如下：

* 空接口的类型集是所有非接口类型的集合
* 非空接口的类型集是其接口元素类型集的交集
* 方法规格的类型集是方法集中包含该方法的类型的集合
* 非接口类型术语的类型集就是组成该类型的集合
* 格式为 :code:`~T` 的术语的类型集是潜在类型为 :code:`T` 的类型的集合
* 术语 :html-role:`<code class="code">t<sub>1</sub>|t<sub>2</sub>|…|t<sub>n</sub></code>` *并集*
  的类型集是这些术语的类型集的并集

通过构建，接口的类型集永远不会包含接口类型。

.. code-block:: go

  // 仅代表类型 int 的接口。
  interface {
    int
  }

  // 代表具有潜在类型 int 的所有类型的接口
  interface {
    ~int
  }

  // 代表具有潜在类型 int 且实现了 String 方法的所有类型的接口
  interface {
    ~int
    String() string
  }

  // 代表一个空类型集的接口；没有类型能同时是 int 和 string
  interface {
    int
    string
  }

在格式为 :code:`~T` 的术语中， :code:`T` 的潜在类型必须是它自身且 :code:`T` 不能是一个接口。

.. code-block:: go

  type MyInt int

  interface {
    ~[]byte  // []byte 的潜在类型是它自己
    ~MyInt   // 非法： MyInt 的潜在类型不是 MyInt
    ~error   // 非法： error 是一个接口
  }

:ruby:`并集元素|Union elements` 表示其所有类型集的并集：

.. code-block:: go

  // Float 接口代表了所有浮点数类型
  // （包括所有潜在类型为 float32 或 float64 的命名类型）。
  type Float interface {
    ~float32 | ~float64
  }

在并集中，术语不能是一个 `类型形参`_
，且所有非接口术语的类型集必须是成对不相交的（类型集成对的交集必须为空）。给定一个类型形参 :code:`P` ：

.. code-block:: go

  interface {
    P                // 非法： P 是一个类型形参
    int | P          // 非法： P 是一个类型形参
    ~int | MyInt     // 非法： ~int 的类型集和 MyInt 不是不相交的（ ~int 包括了 MyInt ）
    float32 | Float  // 重叠的类型集但 Float 是一个接口
  }

实现限制：一个（术语数量大于 1 的）并集不能包含 `预先声明的标识符`_ :code:`comparable`
或指定了方法的接口，或者嵌入的 :code:`comparable` 或指定了方法的接口。

非 `基本接口`_ 只可以作为类型约束来使用，或作为其它作为约束来使用的接口的元素。
这些接口不能作为值或变量的类型，也不能作为其它非接口类型的组件。

.. note::

  译注，这里的基本接口包含了上述的基本接口以及仅嵌入了基本接口的嵌入接口。
  来源见 `the commit msg of 30501bb`_

.. code-block:: go

  var x Float                     // 非法： Float 不是一个基本接口

  var x interface{} = Float(nil)  // 非法

  type Floatish struct {
    f Float                       // 非法
  }

一个接口类型 :code:`T` 不能嵌入任何递归地包含或嵌入 :code:`T` 的类型元素。

.. code-block:: go

  // 非法: Bad 不能嵌入它自己
  type Bad interface {
    Bad
  }

  // 非法: Bad1 不能通过 Bad2 来嵌入它自己
  type Bad1 interface {
    Bad2
  }
  type Bad2 interface {
    Bad1
  }

  // 非法： Bad3 不能嵌入包含 Bad3 的并集
  type Bad3 interface {
    ~int | ~string | Bad3
  }

.. _`实现了`:

.. _`实现了这个接口`:

实现接口
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

如果

* :code:`T` 不是一个接口但是 :code:`I` 的类型集的元素；或者
* :code:`T` 是一个接口且 :code:`T` 的类型集是 :code:`I` 的类型集的子集，

那么类型 :code:`T` 就实现了接口 :code:`I` 。

如果 :code:`T` 实现了一个接口，那么类型 :code:`T` 的值就实现了这个接口。

.. _`映射`:

.. _`映射类型`:

:ruby:`映射类型|Map types`
------------------------------------------------------------

映射是由一种类型的元素所组成的无序组，这个类型被称为元素类型，
其元素被一组另一种类型的唯一 *键* 索引，这个类型被称为键类型。
一个未初始化的映射的值为 :code:`nil` 。

::

  MapType     = "map", "[", KeyType, "]", ElementType .
  KeyType     = Type .

键类型的操作数必须有完全定义的 `比较运算符`_ :code:`==` 和 :code:`!=` ；因此键类型不能为一个函数、映射或分片。如果键类型是一个接口类型，那么比较运算符必须针对其动态键值做完全定义；失败会导致一个 `run-time panic`_ 。

.. code-block:: go

  map[string]int
  map[*T]struct{ x, y float64 }
  map[string]interface{}

映射元素的数目被称为其长度。对于一个映射 :code:`m` ，长度可以使用内置函数 `len`_ 来找到并且可能会在执行过程中改变。元素可以在执行过程中使用 `赋值`_ 来进行添加，可以使用 `索引表达式`_ 来获取；可以使用内置函数 `delete`_ 来移除。

一个新的、空的映射值的创建使用的是内置函数 `make`_ ，其获取映射类型和一个可选的容量提示作为实参：

.. code-block:: go

  make(map[string]int)
  make(map[string]int, 100)

初始化的容量不会限制其大小：映射会增长以适合其存储项目的数量，除了 :code:`nil` 映射。 :code:`nil` 映射相当于空映射，但是 :code:`nil` 映射不能添加元素。

.. _`信道`:

.. _`信道类型`:

:ruby:`信道类型|Channel types`
------------------------------------------------------------

信道针对 `并行执行函数`_ 提供了一个 `发送`_ 和 `接收`_ 指定类型的值的机制。未初始化的信道的值为 :code:`nil` 。

::

  ChannelType = ( "chan" | "chan", "<-" | "<-", "chan" ), ElementType .

可选的 :code:`<-` 运算符指定了信道的 *方向* 、 *发送* 或 *接收* 。如果方向被指定了，那么这个信道是 *定向的* ，否则就是 *双向的* 。通过 `赋值`_ 或显示的 `转换`_ ，信道可以被限制为仅能发送或仅能接收。

.. code-block:: go

  chan T          // 可用于发送或接收类型为 T 的值
  chan<- float64  // 仅用于发送 float64 类型
  <-chan int      // 仅用于接收 int 类型

:code:`<-` 与最左的 :code:`chan` 关联的一些可能性：

.. code-block:: go

  chan<- chan int    // 和 chan<- (chan int) 一样
  chan<- <-chan int  // 和 chan<- (<-chan int) 一样
  <-chan <-chan int  // 和 <-chan (<-chan int) 一样
  chan (<-chan int)

一个新的，初始化的信道值的创建可以使用内置的函数 `make`_ ，它获取信道类型和可选的 *容量* 作为实参：

.. code-block:: go

  make(chan int, 100)

容量（元素的数量）确定了信道中缓冲区的大小。如果容量为零或没有写，那么信道就是无缓冲的，这种情况下，只有在接收端和发送端都准备好的情况下，通信才会成功。不然信道就是有缓冲的，这种情况下只要不阻塞，通信便会成功；阻塞是指缓冲区满了（对于发送端而言）或者缓冲区空了（对于接收端而言）。 一个 :code:`nil` 的信道是不能用于通信的。

信道可以使用内置函数 `close`_ 来关闭。 `接收运算符`_ 的多值分配形式报告了在信道关闭前接收到的值是否已经被发送了。

单个信道可以被不需要进一步同步的任意数量的 goroutines 用在 `发送语句`_ ， `接收运算符`_ 和对内置函数 `cap`_ 及 `len`_ 的调用上。信道是一个先进先出的队列。举例，如果一个 goroutine 在信道上发送了值，第二个 goroutine 接收了这些值，那么这些值是按照发送的顺序被接收的。


类型和值的属性
========================================

潜在类型
------------------------------------------------------------

每个类型 :code:`T` 都有一个 *潜在类型* ：
如果 :code:`T` 是预先声明的布尔值、数值或者字符串类型之一，或一个类型字面值，那对应的潜在类型就是
:code:`T` 自己。否则，其潜在类型就是 :code:`T` 声明时指定的那个类型的潜在类型。
对于类型形参而言，则是其 `类型约束`_ 的潜在类型，其总是一个接口。

.. code-block:: go

  type (
    A1 = string
    A2 = A1
  )

  type (
    B1 string
    B2 B1
    B3 []B1
    B4 B3
  )

  func f[P any](x P) { … }

:code:`string` , :code:`A1` , :code:`A2` , :code:`B1` 和 :code:`B2` 的潜在类型是 :code:`string` 。
:code:`[]B1` , :code:`B3` 和 :code:`B4` 的潜在类型是 :code:`[]B1` 。
:code:`P` 的潜在类型为 :code:`interface{}` 。

核心类型
------------------------------------------------------------

每个非接口类型 :code:`T` 都有一个 *核心类型* ，它和 :code:`T` 的 `潜在类型`_ 是相同的。

如果以下条件之一满足，那么接口 :code:`T` 就就有核心类型：

1. 存在一个单一类型 :code:`U` ，这个类型是 :code:`T` 的 `类型集`_ 中所有类型的 `潜在类型`_ ；或者
2. :code:`T` 的类型集仅包含带一致元素类型 :code:`E` 的 `信道类型`_ ，且所有定向信道有相同的方向。

所有其它接口都没有核心类型。

根据满足条件，接口的核心类型要么是：

1. 类型 :code:`U` ；要么是
2. 类型 :code:`chan E` （如果 :code:`T` 仅包含双向信道），
   或者类型 :code:`chan<- E` 或 :code:`<-chan E` （取决于现存定向信道的方向）

根据定义，核心类型永远不会是 `定义类型`_ 、 `类型形参`_ 或 `接口类型`_ 。

带核心类型的接口的例子：

.. code-block:: go

  type Celsius float32
  type Kelvin  float32

  interface{ int }                          // int
  interface{ Celsius|Kelvin }               // float32
  interface{ ~chan int }                    // chan int
  interface{ ~chan int|~chan<- int }        // chan<- int
  interface{ ~[]*data; String() string }    // []*data

不带核心类型的接口的例子：

.. code-block:: go

  interface{}                               // 无单一潜在类型
  interface{ Celsius|float64 }              // 无单一潜在类型
  interface{ chan int | chan<- string }     // 信道有不同的元素类型
  interface{ <-chan int | chan<- int }      // 定向信道有不同的方向

.. 于 https://github.com/golang/go/commit/46f352de2dc80657664431ebb04f89a2fad579c5 中被删除

  特定类型
  ------------------------------------------------------------

  *[The definition of specific types is not quite correct yet.]*

  一个包含了 `类型元素（TypeElem）`_ 的接口规格定义了一个（可能为空的） *特定类型*
  的集合。粗略地说，这些类型 :code:`T` 以 :code:`T` 、 :code:`~T` 或此类术语的并集形式出现在接口定义中。

  更准确地来说，对于一个给定的接口，如果这个接口表现的类型的集合 𝑅
  非空且有限，那么特定类型的集合对应这个集合 𝑅 。否则，如果 𝑅 是空的或者无限的，那么这个接口
  *没有特定类型* 。

  对于一个给定的接口、类型元素 或类型术语，其表现的类型的集合 𝑅 定义如下：

  * 对于非类型化的元素的接口， 𝑅 是所有类型的（无限）集。
  * 对于类型化的元素的接口， 𝑅 是其类型元素所表现类型的交集。
  * 对与非接口类型术语 :code:`T` 或 :code:`~T` 格式的术语， 𝑅 是由类型 :code:`T` 所组成的集。
  * 对于术语 :html-role:`<code class="code">t<sub>1</sub>|t<sub>2</sub>|…|t<sub>n</sub></code>`
    的 *并集* ， 𝑅 是这些术语所表现类型的并集。

  即使一个接口的 `类型集`_ 为空，它依旧可能有特定类型。

  带特定类型的接口的例子：

  .. code-block:: go

    interface{}                    // 无特定类型
    interface{ int }               // int
    interface{ ~string }           // string
    interface{ int|~string }       // int, string
    interface{ Celsius|Kelvin }    // Celsius, Kelvin
    interface{ float64|any }       // 无特定类型 （并集是所有类型）
    interface{ int; m() }          // int （但类型集是空的，因为 int 没有方法 m）
    interface{ ~int; m() }         // int （但类型值是无限的，因为很多整数类型都有一个方法 m ）
    interface{ int; any }          // int
    interface{ int; string }       // 无特定类型 （交集是空的）

.. _`不同的`:

.. _`一致的`:

.. _`一致`:

类型一致性
------------------------------------------------------------

两个类型，要么是 *一致的* 要么是 *不同的* 。

`命名类型`_ 和其它类型总是不同的。除此以外，如果两个类型所对应的 `潜在类型`_ 字面值是结构一致的——也就是说它们拥有相同的字面值结构并且对应的组成部分拥有一致的类型——那么它们便是一致的。详细来说：

* 如果两个数组类型有一致的元素类型和相同的数组长度，那么它们便是一致的。
* 如果两个分片类型有一致的元素类型，那么它们便是一致的。
* 如果两个结构体有相同的字段序列，并且对应的字段有相同的名字、一致的类型和一致的标签，那么它们便是一致的。（不同包的 `非暴露的`_ 字段名总是不同的）
* 如果两个指针类型有一致的基础类型，那么它们便是一致的。
* 如果两个函数类型有相同的参数数量和结果值，并且对应的参数和结果类型是一致的，并且两者要么都是 variadic 要么都不是，那么它们便是一致的。（参数和结果名不是必须匹配的）
* 如果两个接口类型定义了相同的类型集，那么它们便是一致的。
* 如果两个映射类型有一致的键类型和值类型，那么它们便是一致的。
* 如果两个信道类型有一致的值类型和相同的方向，那么它们便是一致的。
* 如果两个 `实例化`_ 过的类型的定义类型和所有的类型实参都是一致的，那么它们便是一致的。

给出声明

.. code-block:: go

  type (
    A0 = []string
    A1 = A0
    A2 = struct{ a, b int }
    A3 = int
    A4 = func(A3, float64) *A0
    A5 = func(x int, _ float64) *[]string

    B0 A0
    B1 []string
    B2 struct{ a, b int }
    B3 struct{ a, c int }
    B4 func(int, float64) *B0
    B5 func(x int, y float64) *A1
    C0 = B0
    D0[P1, P2 any] struct{ x P1; y P2 }
    E0 = D0[int, string]
  )


这些类型是一致的

::

  A0, A1, 和 []string
  A2 和 struct{ a, b int }
  A3 和 int
  A4, func(int, float64) *[]string, 和 A5

  B0 和 C0
  D0[int, string] 和 E0
  []int 和 []int
  struct{ a, b *T5 } 和 struct{ a, b *T5 }
  func(x int, y float64) *[]string, func(int, float64) (result *[]string), 和 A5

:code:`B0` 和 :code:`B1` 是不同的，因为它们是被不同的 `类型定义`_ 所创建的新类型； :code:`func(int, float64) *B0` 和 :code:`func(x int, y float64) *[]string` 是不同的，因为 :code:`B0` 和 :code:`[]string` 是不同的； :code:`P1` 和 :code:`P2` 不同是因为它们是不同的类型形。 :code:`D0[int, string]` 和 :code:`struct{ x int; y string }` 不同是因为前者是一个 `实例化`_ 过的定义类型而后者是一个类型字面值（但它们仍然是 `可分配的`_ ）。

.. _`可分配`:

.. _`可分配的`:

可分配性
------------------------------------------------------------

在如下这些情况中，类型为 :code:`V` 的值 :code:`x` *可以分配* 给一个类型为
:code:`T` 的 `变量`_ （「 :code:`x` 可以分配给 :code:`T` 」）：

* :code:`V` 和 :code:`T` 一致。
* :code:`V` 和 :code:`T` 有一致的 `潜在类型`_ 并且二者至少有一个不是 `命名类型`_ 。
* :code:`V` 和 :code:`T` 是带一致元素类型的信道类型， :code:`V`
  是一个双向信道，且 :code:`V` 和 :code:`T` 中至少有一个不是命名类型。
* :code:`T` 是一个接口类型，但不是一个类型形参，且 :code:`x` `实现了`_ :code:`T` 。
* :code:`x` 是一个预先声明的标识符 :code:`nil` 而 :code:`T` 是一个指针、函数、分片、映射、信道或接口类型，但不是一个类型形参。
* :code:`x` 是一个非类型化的可以被类型 :code:`T` 的一个值所代表的 `常量`_ 。

此外，如果 :code:`x` 的类型 :code:`V` 或 :code:`T` 是类型形参，那么如果满足如下条件之一，
:code:`x` 就可以分配给类型 :code:`T` 的变量：

* :code:`x` 是一个预先声明的标识符 :code:`nil` ， :code:`T` 是一个类型形参，那么
  :code:`x` 可以分配给 :code:`T` 类型集中的每一个类型。
* :code:`V` 不是一个 `命名类型`_ ， :code:`T` 是一个类型形参，那么
  :code:`x` 可以分配给 :code:`T` 类型集中的每一个类型。
* :code:`V` 是一个类型形参且 :code:`T` 不是一个命名类型，那么 :code:`V`
  类型集中每一个类型的值都可以分配给 :code:`T` 。

.. _`所表示`:

.. _`表示的`:

.. _`所表示的`:

可表示性
------------------------------------------------------------

只要以下条件有一个成立，那么 `常量`_ :code:`x` 就可以被类型为 :code:`T` （这个 :code:`T` 不能是一个 `类型形参`_ ）的值所表示：

* :code:`x` 在由 :code:`T` `所确定的`_ 值集中
* :code:`T` 是一个 `浮点数类型`_ 并且 :code:`x` 可以被不溢出地约到 :code:`T`
  的精度。约数用的是 IEEE 754 round-to-even 规则，但是 IEEE 负零会被进一步简化到一个无符号的零。
  （注：这种常量值不会出现 IEEE 负零、 NaN 或者无穷。）
* :code:`T` 是一个复数类型并且 :code:`x` 的 `组成`_ :code:`real(x)` 和 :code:`imag(x)` 是可以被 :code:`T` 的组成类型（ :code:`float32` 或者 :code:`float64` ）所表示的。

如果 :code:`T` 是一个类型形参，那么如果 :code:`x` 可以被 :code:`T`
类型集中的每一个类型的值所表示，那么 :code:`x` 就可以被 :code:`T` 的值所表示。

::

  x                   T           x 可以被 T 表示的原因是

  'a'                 byte        97 在 byte 值集中
  97                  rune        rune 是 int32 的别名且 97 在 32 位整数值集中
  "foo"               string      "foo" 在 string 值集中
  1024                int16       1024 在 16 位整数值集中
  42.0                byte        42 在无符号 8 位整数值集中
  1e10                uint64      10000000000 在无符号 64 位整数值集中
  2.718281828459045   float32     2.718281828459045 约到 2.7182817 后在 float32 值集中
  -1e-1000            float64     -1e-1000 约到 IEEE -0.0 后再被进一步简化到 0.0
  0i                  int         0 是一个整数值
  (42 + 0i)           float32     42.0 （带虚部零）在 float32 值集中

::

  x                   T           x 不能被 T 表示的原因是

  0                   bool        0 不在 boolean 值集中
  'a'                 string      'a' 是 rune，它不在 string 值集中
  1024                byte        1024 不在无符号 8 位整数值集中
  -1                  uint16      -1 不在无符号 16 位整数值集中
  1.1                 int         1.1 不是一个整数值
  42i                 float32     (0 + 42i) 不在 float32 值集中
  1e1000              float64     1e1000 约数后溢出了 IEEE +Inf

.. _`实现`:

方法集
------------------------------------------------------------

类型的 *方法集* 确定了该类型的 `操作数`_ 所可以 `调用`_
的方法。每一个类型都有一个（可能为空的）方法集与之关联：

* `定义类型`_ :code:`T` 的方法集是由接收器类型 :code:`T` 所声明的所有 `方法`_ 组成的。
* 指向定义类型 :code:`T` 的指针（ :code:`T` 既不能是指针也不能是接口）
  的方法集是由接收器类型 :code:`*T` 或 :code:`T` 所声明的所有方法组成的。
* `接口类型`_ 的方法集是该接口的 `类型集`_
  中每个类型的方法集的交集（最终的方法集往往是该接口中所声明的方法的集合）。

应用于包含嵌入字段的结构体（及其指针）的更多规则，会在 `结构体类型`_
一节描述。任何其它类型都有一个空的方法集。

在方法集中，每个方法都必须有一个 `唯一的`_ 非 `空白`_ 的 `方法名`_ 。


.. _`块`:

.. _`包块`:

.. _`宇宙块`:

.. _`语句列表`:

:ruby:`块|Blocks`
========================================

*块* 是在一对花括号内的声明和语句序列，这个序列可能是空的。

::

  Block = "{", StatementList, "}" .
  StatementList = { Statement, ";" } .

源代码中除了显式的块外，还有隐式的块：

1. 包围所有 Go 原始文本的 *宇宙块* 。
2. 每个 `包`_ 有一个包含针对该包的所有 Go 原始文本的 *包块* 。
3. 每个文件有一个包含在该文件中所有 Go 原始文本的 *文件块* 。
4. 每个 `"if"`_ , `"for"`_ 和 `"switch"`_ 语句都被认为是在其自己的隐式块中。
5. 每个在 `"switch"`_ 或 `"select"`_ 语句中的子句都作为一个隐式的块。

块是嵌套的并影响着 `作用域`_ 。

.. _`声明`:

.. _`声明的`:

.. _`作用域`:

声明和作用域
========================================

*声明* 绑定了非 `空白`_ 的标识符到
`常量`_ 、
`类型`_ 、
`类型形参`_ 、
`变量`_ 、
`函数`_ 、
`标签`_ 或 `包`_ 。
程序中的每个标识符都必须要声明。同一个块中不能定义一个标识符两次，并且没有标识符可以同时在文件块和包块中定义。

`空白标识符`_ 可以像其它标识符一样在声明中使用，但它不会引出一个绑定，因此不被声明。在包块中，标识符 :code:`init` 只能用于 `init 函数`_ 声明，且和空白标识符一样，它不会引出一个新的绑定。

::

  Declaration   = ConstDecl | TypeDecl | VarDecl .
  TopLevelDecl  = Declaration | FunctionDecl | MethodDecl .

声明的标识符的 *作用域* 是该标识符表示特定常量、类型、变量、函数、标记或包时所处的原始文本的范围。

Go 使用 `块`_ 来定作用域：

1. `预先声明的标识符`_ 的作用域为宇宙块。
2. 表示一个常量、类型、变量或函数（但不是方法）的在最上层（在任何函数外）定义的标识符的作用域为包块。
3. 导入的包的包名的作用域为包含导入声明在内的文件的文件块。
4. 表示一个方法接收器、函数参数或结果变量的标识符的作用域为函数主体。
5. 表示一个函数的或被方法接收器所声明的
   类型形参的标识符的作用域是这个函数体及函数的所有形参列表。
6. 表示一个类型的类型形参的标识符的作用域起于这个类型的名字，终于类型规格（TypeSpec）。
7. 在函数内定义的常量或变量标识符的作用域起始于 ConstSpec 或 VarSpec（对短变量来说为 ShortVarDecl）的尾端，结束于包含着它的最内的块。
8. 在函数内定义的类型标识符的作用域起于 TypeSpec 的标识符，终于包含着它的最内的块。

在块中声明的标识符可以在其内的块中重新声明。当内部声明的标识符在作用域内时，它表示内部声明所声明的实体。

`包子句`_ 不是一个声明；包名不会在任何作用域中出现。它的目的是确定一个文件属于相同的 `包`_ 和针对导入声明指定默认的包名。

标签作用域
------------------------------------------------------------

标签是由 `标签语句`_ 所声明的，它用在 `"break"`_ 、 `"continue"`_ 和 `"goto"`_ 语句中。定义一个不去用的标签是非法的。与其它标识符相对比，标签不按块分作用域，也不和那些不是标签的标识符冲突。标记的作用域是声明时所在的函数的主体，不过要排除所有嵌套函数的主体。

.. _`空白`:

空白标识符
------------------------------------------------------------

*空白标识符* 由下划线字符 :code:`_` 所代表。它充当一个匿名的占位符替代通常的（非空白的）标识符，并且作为 `操作数`_ 在 `声明`_ 和 `赋值`_ 中有特殊的意义。

.. _`nil`:

.. _`预先声明`:

.. _`预先声明的`:

.. _`预先声明的标识符`:

预声明的标识符
------------------------------------------------------------

以下的标识符是在 `宇宙块`_ 中被隐式地定义的::

  Types:
    any bool byte comparable
    complex64 complex128 error float32 float64
    int int8 int16 int32 int64 rune string
    uint uint8 uint16 uint32 uint64 uintptr

  Constants:
    true false iota

  Zero value:
    nil

  Functions:
    append cap close complex copy delete imag len
    make new panic print println real recover

.. _`暴露`:

.. _`非暴露的`:

暴露的标识符
------------------------------------------------------------

标识符可以被 *暴露* 用来允许从另一个包访问到它。一个标识符将会被暴露如果同时满足：

1. 标识符的首字母为 Unicode 大写字母（Unicode 类 "Lu"）；以及
2. 标识符是在 `包块`_ 中声明的或者它是一个 `字段名`_ 或 `方法名`_ 。

所有其它的标识符是不暴露的。

.. _`唯一的`:

.. _`一个`:

.. _`同名`:

标识符的唯一性
------------------------------------------------------------

给定一组标识符，如果一个标识符与在该集合中的所有其它都 *不同* ，那么其便被称为是 *唯一的* 。如果两个标识符拼写不同，或它们处于不同的 `包`_ 并且没有被暴露，那么它们便是不同的。否则，它们便是相同的。

.. _`标识符列表`:

.. _`隐式重复`:

常量声明
------------------------------------------------------------

常量声明绑定了一个标识符的列表（常量的名字）到 `常量表达式`_ 列表的值。标识符的数量必须等于表达式的数量，并且左侧第 n 个标识符绑定到了右侧第 n 个表达式的值。

.. _`ConstSpec`:

::

  ConstDecl      = "const", ( ConstSpec | "(", { ConstSpec, ";" }, ")", ) .
  ConstSpec      = IdentifierList, [ [ Type ], "=", ExpressionList ] .

  IdentifierList = identifier { ",", identifier } .
  ExpressionList = Expression { ",", Expression } .

如果类型提供了，那么所有常量需采用该指定类型，并且表达式必须 `可分配`_
到该类型，且该类型不能是一个类型形参。
如果类型省略了，常量为对应表达式的独立的类型。如果表达式的值为非类型化的 `常量`_
，那么声明的常量保持为非类型化的，常量标识符表示着该常量的值。
比如，如果一个表达式为浮点数字面值，那么即使字面值的小数部分为零，常量标识符依旧表示一个浮点数常量。

.. code-block:: go

  const Pi float64 = 3.14159265358979323846
  const zero = 0.0        // 非类型化的浮点数常量
  const (
    size int64 = 1024
    eof        = -1       // 非类型化的整数常量
  )
  const a, b, c = 3, 4, "foo"  // a = 3, b = 4, c = "foo", 非类型化的整数和字符串常量
  const u, v float32 = 0, 3    // u = 0.0, v = 3.0

在括起来的 :code:`const` 声明列表中，除了第一个常量声明外，其它的表达式列可以省略。这样的一个空列表相当于第一个前面的非空表达式列表及其类型（如果有的话）的文本替换。省略表达式的列表就因此相当于重复之前的列表。标识符的数量必须等于之前列表的表达式的数量。这个机制结合 `iota`_ 常量生成器允许了连续值的轻量声明：

.. code-block:: go

  const (
    Sunday = iota
    Monday
    Tuesday
    Wednesday
    Thursday
    Friday
    Partyday
    numberOfDays  // 这个常量是不暴露的
  )

Iota
------------------------------------------------------------

在一个 `常量声明`_ 中，预先声明的标识符 :code:`iota` 代表连续的非类型化的整数 `常量`_ 。它的值从零开始，是在常量声明中各自的 `ConstSpec`_ 的索引。其可以用于构造一组相关的常量：

.. code-block:: go

  const (
    c0 = iota  // c0 == 0
    c1 = iota  // c1 == 1
    c2 = iota  // c2 == 2
  )

  const (
    a = 1 << iota  // a == 1  (iota == 0)
    b = 1 << iota  // b == 2  (iota == 1)
    c = 3          // c == 3  (iota == 2，没有使用)
    d = 1 << iota  // d == 8  (iota == 3)
  )

  const (
    u         = iota * 42  // u == 0     （非类型化的整数常量）
    v float64 = iota * 42  // v == 42.0  （float64 常量）
    w         = iota * 42  // w == 84    （非类型化的整数常量）
  )

  const x = iota  // x == 0
  const y = iota  // y == 0

定义上，在同一个 `ConstSpec`_ 中使用的多个 :code:`iota` 都拥有相同的值：

.. code-block:: go

  const (
    bit0, mask0 = 1 << iota, 1<<iota - 1  // bit0 == 1, mask0 == 0  (iota == 0)
    bit1, mask1                           // bit1 == 2, mask1 == 1  (iota == 1)
    _, _                                  //                        (iota == 2，没有使用)
    bit3, mask3                           // bit3 == 8, mask3 == 7  (iota == 3)
  )

最后一个例子利用了上一个非空表达式列表的 `隐式重复`_ 。

.. _`参数化类型`:

.. _`类型声明`:

.. _`泛型`:

.. _`TypeSpec`:

:ruby:`类型声明|Type declarations`
------------------------------------------------------------

一个类型声明绑定了一个标识符（也就是 *类型名* ）到一个 `类型`_ 。类型声明有两种形式：别名声明和类型定义。

::

  TypeDecl     = "type", ( TypeSpec | "(", { TypeSpec, ";" }, ")" ) .
  TypeSpec     = AliasDecl | TypeDef .

:ruby:`别名声明|Alias declarations`
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

别名声明绑定了一个标识符到一个给定的类型。

::

  AliasDecl = identifier, "=", Type .

在标识符的 `作用域`_ 内，它充当了该类型的 *别名* 。

.. code-block:: go

  type (
    nodeList = []*Node  // nodeList 和 []*Node 的类型一致
    Polar    = polar    // Polar 和 polar 表示的类型一致
  )

.. _`定义的`:

.. _`定义类型`:

.. _`类型定义`:

:ruby:`类型定义|Type definitions`
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

类型定义创建一个新的，不同的类型，其具有与给定类型相同的 `潜在类型`_ 和操作，并将标识符和 *类型名* 绑定到它。

::

  TypeDef = identifier, [ TypeParameters ], Type .

新类型被称为 *定义类型* 。它和其它任何的类型（包括那个给定类型）都是 `不同的`_ 。

.. code-block:: go

  type (
    Point struct{ x, y float64 }  // Point 和 struct{x, y float64} 是不同的类型
    polar Point                   // polar 和 Point 表示不同的类型
  )

  type TreeNode struct {
    left, right *TreeNode
    value any
  }

  type Block interface {
    BlockSize() int
    Encrypt(src, dst []byte)
    Decrypt(src, dst []byte)
  }

定义类型可能具有与之关联的 `方法`_ 。它不会继承任何绑定到给定类型的方法，但接口类型或者复合类型元素的 `方法集`_ 是保持不变的：

.. code-block:: go

  // Mutex 是带两个方法——Lock 和 Unlock——的数据类型。
  type Mutex struct         { /* 互斥对象字段 */ }
  func (m *Mutex) Lock()    { /* Lock 实现 */ }
  func (m *Mutex) Unlock()  { /* Unlock 实现 */ }

  // NewMutex 和 Mutex 有相同的构成，但是其方法集是空的。
  type NewMutex Mutex

  // PtrMutex 的潜在类型 *Mutex 的方法集是保持不变的，
  // 但 PtrMutex 的方法集是空的。
  type PtrMutex *Mutex

  // *PrintableMutex 的方法集包含了绑定到它的嵌入字段 Mutex 的方法 Lock 和 Unlock 。
  type PrintableMutex struct {
    Mutex
  }

  // MyBlock 是一个和 Block 有着相同方法集的接口类型。
  type MyBlock Block

类型声明可以用于定义不同的布尔、数值或字符串类型，并关联方法给它：

.. code-block:: go

  type TimeZone int

  const (
    EST TimeZone = -(5 + iota)
    CST
    MST
    PST
  )

  func (tz TimeZone) String() string {
    return fmt.Sprintf("GMT%+dh", tz)
  }

如果类型定义指定了 `类型形参`_ ，那么这个类型名代表一个 *泛型* 。
泛型在它们使用时必须被 `实例化`_ 。

.. code-block:: go

  type List[T any] struct {
    next  *List[T]
    value T
  }

在一个类型定义中，给定的类型不能是一个类型形参。

.. code-block:: go

  type T[P any] P    // 非法： P 是一个类型形参

  func f[T any]() {
    type L T         // 非法： T 是被封闭函数所声明的一个类型形参
  }

泛型也可能有与之关联的 `方法`_ 。
在这种情况下，方法接收器声明的类型形参数量必须与当前泛型定义中的数量相等。

.. code-block:: go

  // 方法 Len 会返回连接列表 l 中元素的数量。
  func (l *List[T]) Len() int  { … }

.. _`类型形参列表`:

.. _`类型形参`:

.. _`约束`:

:ruby:`类型形参声明|Type parameter declarations`
------------------------------------------------------------

类型形参列表在一个泛型函数中或类型定义中声明了 *类型形参* 。类型形参列表看起来就像一个寻常的
`函数形参列表`_ ，除了类型形参名都必须已经存在且这个列表是闭合在方括号中而不是花括号。

::

  TypeParameters  = "[", TypeParamList, [ "," ], "]" .
  TypeParamList   = TypeParamDecl, { ",", TypeParamDecl } .
  TypeParamDecl   = IdentifierList, TypeConstraint .

列表中所有非空白的名字都必须是唯一的。
每个名字都声明了一个类型形参，每个类型形参都是一个新的且不同的 `命名类型`_
，用来作为声明中（至今的）未知类型的占位符。

.. code-block:: go

  [P any]
  [S interface{ ~[]byte|string }]
  [S ~[]E, E any]
  [P Constraint[int]]
  [_ any]

就像每个寻常的函数形参都有一个形参类型一样，每个类型形参也有一个对应的被称为其 `类型约束`_ 的（元）类型。

当泛型的类型形参列表声明了一个带类型约束 :code:`C` 的单一类型形参 :code:`P` 时
（这样的 :code:`P C` 形成了有效的表达式：

.. code-block:: go

  type T[P *C] …
  type T[P (C)] …
  type T[P *C|Q] …

），那么会发生 :ruby:`解析歧义|parsing ambiguity` 。

在这种罕见的情况下，类型形参声明很难与表达式进行区分，
导致该类型声明被解析为一个数组类型声明。
为了解决这种歧义，可以将该约束嵌入到一个 `接口`_ 中，或在尾部添上逗号：

.. code-block:: go

  type T[P interface{*C}] …
  type T[P *C,] …

类型形参也可以被与泛型相关联的 `方法声明`_ 的接收器规格所声明。

.. This section needs to explain if and what kind of cycles are permitted
   using type parameters in a type parameter list.

.. _`类型约束`:

:ruby:`类型约束|Type constraints`
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

类型约束是一个 `接口`_ ，这个接口为对应的类型形参定义了一组允许的类型实参，并控制着被该类型形参的值所支持的操作。

::

  TypeConstraint = TypeElem .

如果约束是一个 :code:`interface{E}` 形式的接口字面值，其中 :code:`E`
是一个嵌入类型元素（非方法），那么为了方便在类型参数列表里的封闭的
:code:`interface{ … }` 可以被省略：

.. code-block:: go

  [T []P]                      // = [T interface{[]P}]
  [T ~int]                     // = [T interface{~int}]
  [T int|string]               // = [T interface{int|string}]
  type Constraint ~int         // 非法： ~int 不在一个类型参数列表里

.. We should be able to simplify the rules for comparable or delegate some of them
   elsewhere since we have a section that clearly defines how interfaces implement
   other interfaces based on their type sets. But this should get us going for now.

`预先声明的`_ `接口类型`_ :code:`comparable` 表示所有
`可比较的`_ 的非接口类型的集合。确切来说，如果：

* :code:`T` 不是一个接口类型且 :code:`T` 支持 :code:`==` 或 :code:`!=` 操作；或者
* :code:`T` 是一个接口类型但 :code:`T` `类型集`_ 内的每一个类型都实现了 :code:`comparable` ，

那么类型 :code:`T` 就实现了 :code:`comparable` 。

尽管非类型形参的接口可以 `被比较`_ （可能会导致一个 run-time panic），但它们并没有实现 :code:`comparable` 。

.. code-block:: go

  int                          // 实现了 comparable
  []byte                       // 未实现 comparable （分片不能被比较）
  interface{}                  // 未实现 comparable （见上文）
  interface{ ~int | ~string }  // 仅对类型形参而言： 实现了 comparable
  interface{ comparable }      // 仅对类型形参而言： 实现了 comparable
  interface{ ~int | ~[]byte }  // 仅对类型形参而言： 未实现 comparable （不是所有在类型集中的类型都可以被比较）

:code:`comparable` 这个接口以及那些（直接或间接）嵌入了 :code:`comparable` 的接口仅用作类型约束。它们不能作为值或者变量的类型，或其它及非接口类型的组件。


.. _`变量声明`:

.. _`初始化表达式`:

:ruby:`变量声明|Variable declarations`
------------------------------------------------------------

一个变量声明创建一个或多个变量，给它们绑定对应的标识符，并且给每个分一个类型和一个初始化的值。

::

  VarDecl     = "var", ( VarSpec | "(", { VarSpec, ";" }, ")", ) .
  VarSpec     = IdentifierList, ( Type, [ "=", ExpressionList ] | "=", ExpressionList ) .

.. code-block:: go

  var i int
  var U, V, W float64
  var k = 0
  var x, y float32 = -1, -2
  var (
    i int
    u, v, s = 2.0, 3.0, "bar"
  )
  var re, im = complexSqrt(-1)
  var _, found = entries[name]  // 映射查找；只关心 "found"

如果给出了表达式列表，那么变量会根据 `赋值`_ 规则由表达式来初始化。否则，每个变量都被初始化为其 `零值`_ 。

如果类型提供了，那么每个变量都会指定为那个类型。否则，每个变量的类型会被给定为赋值中对应的初始化值的类型。如果那个值是非类型化的常量，它会先隐式地 `转换`_ 为它的 `默认类型`_ ；如果它是一个非类型化的布尔值，那么它会先隐式地转换为类型 :code:`bool` 。预先声明的值 :code:`nil` 不能用于初始化没有明确类型的变量。

.. code-block:: go

  var d = math.Sin(0.5)  // d 是 float64
  var i = 42             // i 是 int
  var t, ok = x.(T)      // t 是 T, ok 是 bool
  var n = nil            // 非法

实现限制：当在 `函数实体`_ 中定义的变量没有被使用时，编译器可以认定它为非法的。

短变量声明
------------------------------------------------------------

*短变量声明* 使用如下语法::

  ShortVarDecl = IdentifierList, ":=", ExpressionList .

这是如下这种带初始化表达式而不带类型的 `变量声明`_ 的速记法::

  "var", IdentifierList, "=", ExpressionList .

.. code-block:: go

  i, j := 0, 10
  f := func() int { return 7 }
  ch := make(chan int)
  r, w, _ := os.Pipe(fd)  // os.Pipe() 返回一个连接着的文件对和一个 error （如果有的话）
  _, y, _ := coord(p)  // coord() 返回三个值; 只关心 y 座标

和普通的变量声明不同，短变量声明可以 *重复声明* 一个变量，这个变量是在同一个块（或者参数列表——如果该块是一个函数实体的话）内之前已经声明过的，且变量类型不能改变，但是重复声明语句最少要存在一个新的非 `空白`_ 变量。因此，重复声明仅能出现在多变量短声明中。重复声明不会引进新的变量；它仅赋一个新的值到原变量。

.. code-block:: go

  field1, offset := nextField(str, 0)
  field2, offset := nextField(str, offset)  // 重复声明了 offset
  a, a := 1, 2                              // 非法: a 声明了两次，或者如果 a 已经在其它地方声明的了话那么就没有新的变量了

短变量声明只能出现在函数内。在一些针对诸如 `"if"`_ 、 `"for"`_ 或 `"switch"`_ 这样的初始化器的上下文中，也可以用于声明本地临时变量。

.. _`函数`:

.. _`函数体`:

.. _`函数声明`:

.. _`函数实体`:

.. _`泛型函数`:

:ruby:`函数声明|Function declarations`
------------------------------------------------------------

.. Given the importance of functions, this section has always
   been woefully underdeveloped. Would be nice to expand this
   a bit.

函数声明绑定一个标识符（也就是 *函数名* ）到一个函数。

::

  FunctionDecl = "func", FunctionName, [ TypeParameters ], Signature, [ FunctionBody ] .
  FunctionName = identifier .
  FunctionBody = Block .

如果函数的 `签名`_ 声明了结果参数，那么函数体语句列表必须以 `终止语句`_ 结尾。

.. code-block:: go

  func IndexRune(s string, r rune) int {
    for i, c := range s {
      if c == r {
        return i
      }
    }
    // 无效: 缺少返回语句
  }

如果函数声明指定了 `类型形参`_ ，那么这个函数名表示一个
*泛型函数* 。在被调用或作为值使用前，泛型函数必须被 `实例化`_ 。

.. code-block:: go

  func min[T ~int|~float64](x, y T) T {
    if x < y {
      return x
    }
    return y
  }

不带类型形参的函数声明可以省略其实体。这样的声明为在 Go 外部实现（比如汇编程序）的函数提供了签名。

.. code-block:: go

  func flushICache(begin, end uintptr)  // 由外部实现

.. _`方法`:

.. _`接收器`:

.. _`方法声明`:

:ruby:`方法声明|Method declarations`
------------------------------------------------------------

方法是带 *接收器* 的 `函数`_ 。一个方法声明绑定了一个标识符（也就是 *方法名* ）为一个方法，并与接收器的 *基础类型* 关联。

::

  MethodDecl   = "func", Receiver, MethodName, Signature, [ FunctionBody ] .
  Receiver     = Parameters .

接收器是使用在方法名之前额外的参数段来指定的。这个参数段必须声明一个单一非 variadic
形参作为接收器。其类型必须是一个 `定义类型`_ :code:`T`
或到定义类型 :code:`T` 的指针，后面可能跟着一列由方括号包裹的类型形参名 :code:`[P1, P2, …]` 。
:code:`T` 被称为接收器的 *基本类型* 。
接收器的基本类型不能是一个指针或者接口类型，并且它必须在和方法相同的包中被声明。
这个方法就被称为 *绑定到了* 这个基本类型，且方法名只有通过类型 :code:`T`
或 :code:`*T` 的 `选择器`_ 才可见。

.. note::
  译注：方法的基础类型不能是接口，这边不要混淆，接口是一组方法签名的集合，也就是可以定义一个固定类型为一个接口类型，这个固定类型实现了对应接口类型所声明的方法。

一个非 `空白`_ 接收器标识符在方法签名中必须是 `唯一的`_ 。如果接收器的值在方法实体内没有被引用，那么其标识符在声明时是可以省略的。一般来说这也同样适用于函数和方法的参数。

对一个基础类型来说，绑定到它的非空白的方法名必须是唯一的。如果基础类型为 `结构体类型`_ 。那么非空白的方法和字段名必须是不同的。

给定一个定义类型 :code:`Point` ，其声明

.. code-block:: go

  func (p *Point) Length() float64 {
    return math.Sqrt(p.x * p.x + p.y * p.y)
  }

  func (p *Point) Scale(factor float64) {
    p.x *= factor
    p.y *= factor
  }

绑定了方法 :code:`Length` 和 :code:`Scale` ，接收器类型为 :code:`*Point` ，对应基础类型 :code:`Point` 。

如果接收器的基本类型是一个 `泛型`_ ，那么 :ruby:`接收器规格|the receiver specification`
必须声明对应的类型形参以供该方法使用。这使得接收器类型形参对该方法可用。

从语句构成上看，类型形参声明像接收器基本类型的 `实例化`_ ：
类型实参必须为标识符（这个标识符表示被声明的类型形参），接收器基本类型的每个类型形参各一个。
类型形参名无需匹配接收器基本类型定义中对应的形参名，
但所有在接收器形参段和方法签名中的非空白的形参名都必须是唯一的。
接收器类型形参的约束是被接收器基本类型定义所隐含的：对应的类型形参有对应的约束。

.. code-block:: go

  type Pair[A, B any] struct {
         a A
         b B
  }

  func (p Pair[A, B]) Swap() Pair[B, A]  { … }  // 接收器声明了 A, B
  func (p Pair[First, _]) First() First  { … }  // 接收器声明了 First ，对应 Pair 中的 A


表达式
========================================

表达式将运算符和函数应用于操作数来规定值的计算。

.. _`操作数`:

:ruby:`操作数|Operands`
------------------------------------------------------------

操作数表示表达式中基本的值。一个操作数可能是一个字面值；可能是一个（可能为 `限定的`_ ）表示 `常量`_ 、 `变量`_ 或 `函数`_ 的非 `空白`_ 标识符或者一个圆括号括起来的表达式。

::

  Operand     = Literal | OperandName, [ TypeArgs ] | "(" Expression ")" .
  Literal     = BasicLit | CompositeLit | FunctionLit .
  BasicLit    = int_lit | float_lit | imaginary_lit | rune_lit | string_lit .
  OperandName = identifier | QualifiedIdent .

表示 `泛型函数`_ 的操作数名可能会紧跟一个 `类型实参`_ 列表；
产生的操作数是一个 `实例化过的`_ 函数。

`空白标识符`_ 只有在 `赋值`_ 的左侧时才能作为一个操作数。

实现限制：当操作数类型是带空 `类型集`_ 的 `类型形参`_ 时，编译器不必报告错误。
带这样类型形参的函数无法被 `实例化`_ ；任何尝试都会导致在实例化处报错。

.. _`限定的`:

.. _`限定标识符`:

:ruby:`限定标识符|Qualified identifiers`
------------------------------------------------------------

*限定标识符* 是由包名前缀所限定的标识符。包名和标识符都不能为 `空白`_ 。

::

  QualifiedIdent = PackageName, ".", identifier .

限定标识符可以在不同的包内访问一个标识符，该标识符对应的包必须已经被 `导入`_ 。标识符则必须已经在那个包被 `暴露`_ 并在 `包块`_ 中被声明。

.. code-block:: go

  math.Sin  // 表示在包 math 中的 Sin 函数

.. _`复合字面值`:

:ruby:`复合字面值|Composite literals`
------------------------------------------------------------

复合字面值在每次被求值时创建一个新的复合值。
复合字面值由字面值类型和紧跟着的花括号绑定的元素列表所组成。每个元素可以选择前缀一个对应的键。

::

  CompositeLit  = LiteralType, LiteralValue .
  LiteralType   = StructType | ArrayType | "[", "...", "]", ElementType |
                  SliceType | MapType | TypeName .
  LiteralValue  = "{", [ ElementList, [ "," ] ], "}" .
  ElementList   = KeyedElement, { ",", KeyedElement } .
  KeyedElement  = [ Key, ":" ], Element .
  Key           = FieldName | Expression | LiteralValue .
  FieldName     = identifier .
  Element       = Expression | LiteralValue .

LiteralType 的 `核心类型`_ :code:`T` 必须是结构体、数组、分片或者映射类型
（文法强制执行此约束，当类型是 TypeName 时除外）。元素和键的类型必须 `可分配`_
给类型 :code:`T` 所对应的字段、元素和键类型；这里没有额外的转换。
该键被解释为结构体字面值的字段名，数组和分片字面值的索引，映射字面值的键。
对于映射字面值而言，每个元素都要有一个键。给多个元素指定相同的字段名或者不变的键值会出错。
对于非常量映射键，可以查阅 `求值顺序`_ 。

对结构体字面值来说，应用如下规则：

* 键必须是在结构体类型中声明的字段。
* 不包含任何键的元素列表必须对每个结构体字段（字段声明的顺序）列出一个元素。
* 只要一个元素有键，那么每个元素都必须要有键。
* 包含键的元素列表不需要针对每个结构体字段有一个元素。省略的字段会获得一个零值。
* 字面值可以省略元素列表；这样子的字面值相当于其类型的零值。
* 针对属于不同包的结构体的非暴露字段来指定一个元素是错误的。

给定一个声明

.. code-block:: go

  type Point3D struct { x, y, z float64 }
  type Line struct { p, q Point3D }

你可以写

.. code-block:: go

  origin := Point3D{}                            // Point3D 为零值
  line := Line{origin, Point3D{y: -4, z: 12.3}}  // line.q.x 为零值

对数组和分片字面值来说，应用如下规则：

* 数组中的每个元素有一个关联的标记其位置的整数索引。
* 带键的元素使用该键作为其索引。这个键必须是可被类型 :code:`int` 所表示的一个非负常量；
  且如果其被类型化了的话，则必须是 `整数类型`_ 。
* 不带键的元素使用之前元素的索引加一。如果第一个元素没有键，则其索引为零。

一个复合变量的 `寻址`_ 生成了一个到由字面值值初始化的唯一 `变量`_ 的指针。

.. code-block:: go

  var pointer *Point3D = &Point3D{y: 1000}

注意的是，分片和映射类型的零值不同于同类型的初始化过但为空的值。所以，获取空的分片或映射复合字面值的地址与使用 `new`_ 来分配一个新的分片或映射的效果不同。

.. code-block:: go

  p1 := &[]int{}    // p1 指向一个初始化过的值为 []int{} 长度为 0 的空分片
  p2 := new([]int)  // p2 指向一个值为 nil 长度为 0 的未初始化过的分片

数组字面值的长度是字面值类型所指定的长度。在字面值中，如果少于其长度的元素被提供了，那么缺漏的元素会被设置为数组元素类型的零值。提供其索引值超出了数组索引范围的元素是错误的。符号 :code:`...` 指定一个数组长度等于其最大元素索引加一。

.. code-block:: go

  buffer := [10]string{}             // len(buffer) == 10
  intSet := [6]int{1, 2, 3, 5}       // len(intSet) == 6
  days := [...]string{"Sat", "Sun"}  // len(days) == 2

分片字面值描述了整个底层数组字面值。因此一个分片字面值的长度和容量为其最大元素索引加一。分片字面值的格式为

.. code-block:: go

  []T{x1, x2, … xn}

以及针对应用到数组的分片操作的速记为

.. code-block:: go

  tmp := [n]T{x1, x2, … xn}
  tmp[0 : n]

在数组、分片或者映射类型 :code:`T` 的复合字面值中，如果元素或映射的键本身为复合字面值，当其字面值类型和 :code:`T` 的元素或键类型一致时，该字面值类型可以省略。类似的，如果元素或键本身为复合字面值的地址，当元素或键的类型为 :code:`*T` 时，该元素或键可以省略 :code:`&T` 。

.. code-block:: go

  [...]Point{{1.5, -3.5}, {0, 0}}     // 同 [...]Point{Point{1.5, -3.5}, Point{0, 0}}
  [][]int{{1, 2, 3}, {4, 5}}          // 同 [][]int{[]int{1, 2, 3}, []int{4, 5}}
  [][]Point{{{0, 1}, {1, 2}}}         // 同 [][]Point{[]Point{Point{0, 1}, Point{1, 2}}}
  map[string]Point{"orig": {0, 0}}    // 同 map[string]Point{"orig": Point{0, 0}}
  map[Point]string{{0, 0}: "orig"}    // 同 map[Point]string{Point{0, 0}: "orig"}

  type PPoint *Point
  [2]*Point{{1.5, -3.5}, {}}          // 同 [2]*Point{&Point{1.5, -3.5}, &Point{}}
  [2]PPoint{{1.5, -3.5}, {}}          // 同 [2]PPoint{PPoint(&Point{1.5, -3.5}), PPoint(&Point{})}

当一个使用 LiteralType 的 TypeName 形式的复合字面值表现为一个在 `关键字`_ 和 "if" 、 "for" 或 "switch" 语句块的左花括号之间的操作数，并且该复合字面值不被圆括号、方括号或花括号所包围时，会出现一个解析歧义。在这样子一个罕见的情况下，复合字面值的左花括号错误地被解析为语句块的引入。为了解决这样子的歧义，这个复合字段必须在圆括号内。

.. code-block:: go

  if x == (T{a,b,c}[i]) { … }
  if (x == T{a,b,c}[i]) { … }

有效的数组、分片和映射字面值的例子：

.. code-block:: go

  // 质数列表
  primes := []int{2, 3, 5, 7, 9, 2147483647}

  // 当 ch 为元音时 vowels[ch] 为真
  vowels := [128]bool{'a': true, 'e': true, 'i': true, 'o': true, 'u': true, 'y': true}

  // 数组 [10]float32{-1, 0, 0, 0, -0.1, -0.1, 0, 0, 0, -1}
  filter := [10]float32{-1, 4: -0.1, -0.1, 9: -1}

  // 十二平均律以 Hz 为单位的频率（A4 = 440Hz）
  noteFrequency := map[string]float32{
    "C0": 16.35, "D0": 18.35, "E0": 20.60, "F0": 21.83,
    "G0": 24.50, "A0": 27.50, "B0": 30.87,
  }

.. _`函数字面值`:

:ruby:`函数字面值|Function literals`
------------------------------------------------------------

函数字面值代表一个匿名 `函数`_ 。函数字面值不能声明类型形参。

::

  FunctionLit = "func", Signature, FunctionBody .

.. code-block:: go

  func(a, b int, z float64) bool { return a*b < int(z) }

函数字面值可以被赋给一个变量或者直接调用。

.. code-block:: go

  f := func(x, y int) int { return x + y }
  func(ch chan int) { ch <- ACK }(replyChan)

  // 译注： (replayChan) https://stackoverflow.com/questions/16008604/why-add-after-closure-body-in-golang

函数字面值是 *闭包* ：它们可以引用外层函数定义的变量。然后这些变量就在外层函数和函数字面值间共享了，并且只要能被访问就可以一直存活。

.. _`主表达式`:

:ruby:`主表达式|Primary expressions`
------------------------------------------------------------

主表达式是一元表达式和二元表达式的操作数。

::

  PrimaryExpr =
    Operand |
    Conversion |
    MethodExpr |
    PrimaryExpr, Selector |
    PrimaryExpr, Index |
    PrimaryExpr, Slice |
    PrimaryExpr, TypeAssertion |
    PrimaryExpr, Arguments .

  Selector       = ".", identifier .
  Index          = "[", Expression, "]" .
  Slice          = "[", [ Expression ], ":", [ Expression ], "]" |
                   "[", [ Expression ], ":", Expression, ":", Expression, "]" .
  TypeAssertion  = ".", "(", Type, ")" .
  Arguments      = "(", [ ( ExpressionList | Type, [ ",", ExpressionList ] ), [ "..." ], [ "," ] ], ")" .

.. code-block:: go

  x
  2
  (s + ".txt")
  f(3.1415, true)
  Point{1, 2}
  m["foo"]
  s[i : j + 1]
  obj.color
  f.p[i].x()

选择器
------------------------------------------------------------

针对一个不为 `包名`_ 的 `主表达式`_ :code:`x` ， *选择器表达式*

.. code-block:: go

  x.f

表示了值 :code:`x` （或者有时候为 :code:`*x` ；见下文）的字段或方法 :code:`f` 。标识符 :code:`f` 被称为（字段或方法） *选择器* ，它一定不能为 `空白标识符`_ 。选择器表达式的类型为 :code:`f` 的类型。如果 :code:`x` 是一个包名，看 `限定标识符`_ 一节。

选择器 :code:`f` 可以表示一个类型 :code:`T` 的一个字段或方法 :code:`f` ，或者可以指嵌套在 :code:`T` 中的 `嵌入字段`_ 的字段或方法 :code:`f` 。遍历以达到 :code:`f` 所经历的嵌入字段数被称为 :code:`f` 在 :code:`T` 中的 *深度* 。在 :code:`T` 中声明的字段或者方法 :code:`f` 的深度为零。在 :code:`T` 中的嵌入字段 :code:`A` 中声明的字段或者方法 :code:`f` 的深度为 :code:`A` 中 :code:`f` 的深度加一。

以下规则应用于选择器：

1. 对于为类型 :code:`T` 或 :code:`*T` 的值 :code:`x` （
   :code:`T` 既不是指针类型也不是接口类型）， :code:`x.f` 表示在 :code:`T`
   中最浅深度的字段或者方法 :code:`f` 。如果不是恰好 `一个`_ :code:`f`
   在最浅深度的话，那么这个选择器表达式就是非法的。
2. 对于为接口类型 :code:`I` 的值 :code:`x` ， :code:`x.f` 表示动态值 :code:`x`
   的名为 :code:`f` 的实际的方法。如果在 :code:`I` 的 `方法集`_ 中没有名为 :code:`f`
   的方法，那么这个选择器表达式就是非法的。
3. 作为例外，如果 :code:`x` 的类型为一个 `定义的`_ 指针类型并且 :code:`(*x).f`
   是一个有效的表示一个字段（但不是方法）的选择器表达式，那么 :code:`x.f` 是 :code:`(*x).f` 的速记。
4. 在所有其它情况中， :code:`x.f` 是非法的。
5. 如果 :code:`x` 是指针类型并且值为 :code:`nil` 并且 :code:`x.f` 表示一个结构体字段，那么，给
   :code:`x.y` 赋值或求值会导致一个 `run-time panic`_ 。
6. 如果 :code:`x` 是接口类型并且值为 :code:`nil` ，那么 `调用`_ 或 `求值`_ 方法 :code:`x.y`
   会导致一个 `run-time panic`_ 。

.. note::
  **这边好好熟悉，规则 2 应该要结合方法声明/调用那节一起看**

举例，给定声明：

.. code-block:: go

  type T0 struct {
    x int
  }

  func (*T0) M0()

  type T1 struct {
    y int
  }

  func (T1) M1()

  type T2 struct {
    z int
    T1
    *T0
  }

  func (*T2) M2()

  type Q *T2

  var t T2     // 假定 t.T0 != nil
  var p *T2    // 假定 p != nil 并且 (*p).T0 != nil
  var q Q = p

你可以写：

.. code-block:: go

  t.z          // t.z
  t.y          // t.T1.y
  t.x          // (*t.T0).x

  p.z          // (*p).z
  p.y          // (*p).T1.y
  p.x          // (*(*p).T0).x

  q.x          // (*(*q).T0).x        (*q).x 是一个有效的字段选择器

  p.M0()       // ((*p).T0).M0()      M0 期望接收器 *T0
  p.M1()       // ((*p).T1).M1()      M1 期望接收器 T1
  p.M2()       // p.M2()              M2 期望接收器 *T2
  t.M2()       // (&t).M2()           M2 期望接收器 *T2，查看调用一节

但下述是无效的：

.. code-block:: go

  q.M0()       // (*q).M0 是有效的，但不是字段选择器

方法表达式
------------------------------------------------------------

如果 :code:`M` 在类型 :code:`T` 的 `方法集`_ 中，那么 :code:`T.M` 是一个函数，该函数可以携带和 :code:`M` 同样的实参像普通函数一样调用，不过会给其前缀一个额外的实参作为该方法的接收器。

::

  MethodExpr    = ReceiverType, ".", MethodName .
  ReceiverType  = Type .

考虑有两个方法的结构体类型 :code:`T` ，方法一是接收器为类型 :code:`T` 的 :code:`Mv` ，其二是接收器为类型 :code:`*T` 的 :code:`Mp` 。

.. code-block:: go

  type T struct {
    a int
  }
  func (tv  T) Mv(a int) int         { return 0 }  // 值接收器
  func (tp *T) Mp(f float32) float32 { return 1 }  // 指针接收器

  var t T

表达式

.. code-block:: go

  T.Mv

产生一个等同于 :code:`Mv` 但带一个明确的接收器作为其第一个实参的函数；它的签名为

.. code-block:: go

  func(tv T, a int) int

这个函数可以在带一个明确的接收器情况下被正常地调用，所以以下五种调用是等同的：

.. code-block:: go

  t.Mv(7)
  T.Mv(t, 7)
  (T).Mv(t, 7)
  f1 := T.Mv; f1(t, 7)
  f2 := (T).Mv; f2(t, 7)

类似的，表达式

.. code-block:: go

  (*T).Mp

产生一个签名为如下的代表 :code:`Mp` 的函数值

.. code-block:: go

  func(tp *T, f float32) float32

对于一个带值接收器的方法，可以推导出一个带明确指针接收器的函数，所以

.. code-block:: go

  (*T).Mv

产生一个签名为如下的代表 :code:`Mv` 的函数值

.. code-block:: go

  func(tv *T, a int) int

这样的一个函数通过接收器创建一个值间接地将其作为接收器传递给底层函数；这个方法在函数调用中不会覆盖那个地址被传递的值。

最后一种情况——值接收器的函数对指针接收器的方法——是非法的，因为指针接收器的方法不在该值类型的方法集中。

从方法推导出的函数值是用函数调用语法来调用的；接收器作为调用的第一个实参。也就是，给定 :code:`f := T.Mv` ， :code:`f` 是作为 :code:`f(t, 7)` 而非 :code:`t.f(7)` 被调用的。使用 `函数字面值`_ 或 `方法值`_ 来构建一个绑定了接收器的函数。

从一个接口类型的方法中得到一个函数值是合法的。所得到的函数使用该接口类型的显式的接收器（原文： The resulting function takes an explicit receiver of that interface type. ）。

.. _`求值`:

方法值
------------------------------------------------------------

如果表达式 :code:`x` 有静态类型 :code:`T` ，并且 :code:`M` 在类型 :code:`T` 的 `方法集`_ 中，那么 :code:`x.M` 被称为一个 *方法值* 。方法值 :code:`x.M` 是一个可以用与 :code:`x.M` 的方法调用的相同的实参来调用的函数值。表达式 :code:`x` 在该方法值的求值过程中被求值和保存；保存的副本被用在（可能会在后续被执行的）任意调用中作为接收器。

.. code-block:: go

  type S struct { *T }
  type T int
  func (t T) M() { print(t) }

  t := new(T)
  s := S{T: t}
  f := t.M                    // 接收器 *t 被求值并存储进 f
  g := s.M                    // 接收器 *(s.T) 被求值并存储进 g
  *t = 42                     // 不会影响在 f 和 g 内存储的接收器

类型 :code:`T` 可以为接口或者非接口类型。

就像上面 `方法表达式`_ 所讨论的，考虑一个带两个方法的结构体 :code:`T` ，方法一是接收器为类型 :code:`T` 的 :code:`Mv` ，其二是接收器为类型 :code:`*T` 的 :code:`Mp` 。

.. code-block:: go

  type T struct {
    a int
  }
  func (tv  T) Mv(a int) int         { return 0 }  // 值接收器
  func (tp *T) Mp(f float32) float32 { return 1 }  // 指针接收器

  var t T
  var pt *T
  func makeT() T

表达式

.. code-block:: go

  t.Mv

产生了一个类型如下的函数值

.. code-block:: go

  func(int) int

这两种调用是等同的：

.. code-block:: go

  t.Mv(7)
  f := t.Mv; f(7)

类似的，表达式

.. code-block:: go

  pt.Mp

产生了一个类型如下的函数值

.. code-block:: go

  func(float32) float32

就 `选择器`_ 来说，如果以值作为接收器的非接口方法使用了指针来引用，那么会自动解除到该指针的引用： :code:`pt.Mv` 等同于 :code:`(*pt).Mv` 。

就 `方法调用`_ 来说，如果以指针作为接收器的非接口方法使用了可寻址值来引用，那么会自动获取该值的地址来引用： :code:`t.Mp` 等同于 :code:`(&t).Mp` 。

.. code-block:: go

  f := t.Mv; f(7)   // 就像 t.Mv(7)
  f := pt.Mp; f(7)  // 就像 pt.Mp(7)
  f := pt.Mv; f(7)  // 就像 (*pt).Mv(7)
  f := t.Mp; f(7)   // 就像 (&t).Mp(7)
  f := makeT().Mp   // 无效的: makeT() 的结果是不可寻址的

虽然以上的例子使用了非接口类型，但是从接口类型的值来创建一个方法值同样是合法的。

.. code-block:: go

  var i interface { M(int) } = myVal
  f := i.M; f(7)  // 就像 i.M(7)

.. _`索引`:

索引表达式
------------------------------------------------------------

如下形式的主表达式

.. code-block:: go

  a[x]

表示了可被 :code:`x` 索引的数组、到数组的指针、分片、字符串或者被 :code:`x` 索引的映射 :code:`a` 的元素。值 :code:`x` 分别被称为 *索引* 或 *映射键* 。以下规则应用于：

如果 :code:`a` 既不是一个映射又不是一个类型形参：

* 索引 :code:`x` 必须是非类型化的常量或者其 `核心类型`_ 必须是 `整数类型`_ 。
* 常量索引必须为非负且可以被类型 :code:`int` `所表示的`_ 的一个值
* 非类型化的常量索引会被给定一个类型 :code:`int`
* 当 :code:`0 <= x < len(a)` 时，索引 :code:`x` *在范围内* ，否则它就 *超出了范围*

对于为 `数组类型`_ :code:`A` 的 :code:`a` ：

* `常量`_ 索引必须在范围内
* 如果在运行时 :code:`x` 超出了范围，那么会发生一个 `run-time panic`_
* :code:`a[x]` 是一个在索引 :code:`x` 处的数组元素，且 :code:`a[x]` 的类型是 :code:`A` 的元素类型

对于到数组类型的 `指针`_ :code:`a` ：

* :code:`a[x]` 是 :code:`(*a)[x]` 的速记

对于为 `分片类型`_ :code:`S` 的 :code:`a` ：

* 如果在运行时 :code:`x` 超出了范围，那么会发生一个 `run-time panic`_
* :code:`a[x]` 是在索引 :code:`x` 处的分片元素，且 :code:`a[x]` 的类型是 :code:`S` 的元素类型

对于 `字符串类型`_ :code:`a` ：

* 当字符串 :code:`a` 是常量时， `常量`_ 索引必须在范围内
* 如果在运行时 :code:`x` 超出了范围，那么会发生一个 `run-time panic`_
* :code:`a[x]` 是在索引 :code:`x` 处的非常量字节，并且 :code:`a[x]` 的类型为 :code:`byte`
* :code:`a[x]` 不能被赋值

对于为 `映射类型`_ :code:`M` 的 :code:`a` ：

* :code:`x` 的类型必须是 `可分配`_ 为 :code:`M` 的键类型的
* 如果映射带键为 :code:`x` 的条目，那么 :code:`a[x]` 是带键 :code:`x` 的映射值，并且 :code:`a[x]` 的类型为 :code:`M` 的值类型。
* 如果映射为 :code:`nil` 或者不存这样这样子的一个条目，那么 :code:`a[x]` 是针对 :code:`M` 的值类型的 `零值`_ 。

对于为 `类型形参`_ :code:`P` 的 :code:`a` ：

* 索引表达式 :code:`a[x]` 必须对 :code:`P` 类型集中所有类型的值有效。
* :code:`P` 类型集中所有类型的元素类型都必须是一致的。
  关于这点，string 类型的的元素类型是 :code:`byte` 。
* 如果 :code:`P` 类型集的类型中有映射，
  那么该类型集中的所有类型都必须是映射类型，且对应的键类型都必须是一致的。
* :code:`a[x]` 是在索引 :code:`x` 处的数组、分片或字符串元素，
  或带 :code:`P` 实例化时所用类型实参（所代表类型的）键 :code:`x` 的映射元素，
  且 :code:`a[x]` 的类型为（一致的）元素类型的类型。
* 如果 :code:`P` 类型集中的类型包含字符串类型，那么 :code:`a[x]` 可能无法被分配到。

否则 :code:`a[x]` 是非法的。

对类型为 :code:`map[K]v` 的映射 :code:`a` 使用特殊格式的 `赋值`_ 或初始化索引表达式

.. code-block:: go

  v, ok = a[x]
  v, ok := a[x]
  var v, ok = a[x]

会产生一个额外的非类型化的布尔值。当键 :code:`x` 存在于映射中时， :code:`ok` 的值为 :code:`true` ，否则为 :code:`false` 。

给 :code:`nil` 映射的元素赋值会导致一个 `run-time panic`_ 。

.. _`再分片`:

分片表达式
------------------------------------------------------------

分片表达式从一个字符串、数组、到数组的指针或者分片中构建一个子字符串或者一个分片。有两种变体：指定一个低位和高位边界的简单格式，以及同时在容量上有指定的完整格式。

简单的分片表达式
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

主表达式

.. code-block:: go

  a[low : high]

构造了一个子字符串或者分片。 :code:`a` 的 `核心类型`_ 必须字符串、数组、到数组的指针或者分片类型。
*索引* :code:`low` 和 :code:`high` 选择了操作数 :code:`a`
的哪些元素显示在结果种。结果有从零开始且长度等于 :code:`high - low` 的索引。
在分片了数组 :code:`a` 后

.. code-block:: go

  a := [5]int{1, 2, 3, 4, 5}
  s := a[1:4]

分片 :code:`s` 有类型 :code:`[]int` ，长度 3，容量 4，以及元素

.. code-block:: go

  s[0] == 2
  s[1] == 3
  s[2] == 4

为了方便，每一个索引都可能被省略。缺少的 :code:`low` 索引默认为零；缺少的 :code:`high` 索引默认为被分片的操作数的长度：

.. code-block:: go

  a[2:]  // 同 a[2 : len(a)]
  a[:3]  // 同 a[0 : 3]
  a[:]   // 同 a[0 : len(a)]

如果 :code:`a` 为到数组的指针，那么 :code:`a[low : high]` 为 :code:`(*a)[low : high]` 的速记。

对于数组或者字符串，如果 :code:`0 <= low <= high <= len(a)` ，那么索引是 *在范围内* 的，否则就 *超出了范围* 。对于分片，上索引边界是分片的容量 :code:`cap(a)` 而不是其长度。 `常量`_ 索引必须为非负且是可以被类型 :code:`int` `所表示的`_ ；对于数组和常量字符串而言，常量索引也必须在范围内。如果两个索引都是常量，那么它们必须满足 :code:`low <= high`。如果在运行时索引超出了范围，那么会发生 `run-time panic`_ 。

除了 `非类型化的字符串`_ 以外，如果被分片的操作数是一个字符串或者分片，那么分片操作的结果为一个和该操作数具有相同类型的非常量值。对于非类型化的字符串操作数而言，其结果是一个类型为 :code:`string` 的非常量值。如果被分片的操作数是一个数组，那么它必须是 `可被寻址的`_ ，并且分片操作的结果为和该数组具有相同元素类型的分片。

如果一个有效的分片表达式的被分片的操作数是一个 :code:`nil` 分片，那么结果是一个 :code:`nil` 分片。否则，结果会共享该操作数的底层数组。

.. code-block:: go

  var a [10]int
  s1 := a[3:7]   // s1 的底层数组是数组 a； &s1[2] == &a[5]
  s2 := s1[1:4]  // s2 的底层数组是 s1 的底层数组 a； &s2[1] == &a[5]
  s2[1] = 42     // s2[1] == s1[2] == a[5] == 42；它们指的都是相同的底层数组元素

完整的分片表达式
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

主表达式

.. code-block:: go

  a[low : high : max]

构建了一个有相同类型的分片，并且带有和简单的分片表达式 :code:`a[low : high]`
一样的长度和元素。此外，它通过设置分片的容量为 :code:`max - low`
来控制产生分片的容量。只有第一个索引是可以被省略的；默认为零。
:code:`a` 的 `核心类型`_ 必须是数组、到数组的指针或者分片类型（但不能是字符串类型）。
在分片了数组 :code:`a` 后

.. code-block:: go

  a := [5]int{1, 2, 3, 4, 5}
  t := a[1:3:5]

分片 :code:`t` 有类型 :code:`[]int` ，长度 2，容量 4，以及元素

.. code-block:: go

  t[0] == 2
  t[1] == 3

和简单的分片表达式一样，如果 :code:`a` 是一个到数组的指针，那么 :code:`a[low : high : max]` 是 :code:`(*a)[low : high : max]` 的速记。如果被分片的操作数是一个数组，那么它必须是 `可被寻址的`_ 。

如果 :code:`0 <= low <= high <= max <= cap(a)` ，那么索引是 *在范围内* 的，否则就 *超出了范围* 。 `常量`_ 索引必须是非负的且可以被类型 :code:`int` 所代表的值；对于数组，常量索引也必须在范围内。如果多个索引为常量，那么存在的常量必须在相对彼此的范围内。如果在运行时索引超出了范围，那么会出现一个 `run-time panic`_ 。

类型断言
------------------------------------------------------------

对于一个为 `接口类型`_ 但非 `类型形参`_ 的表达式 :code:`x` 以及一个类型 :code:`T` ，主表达式

.. code-block:: go

  x.(T)

断言 :code:`x` 不为 :code:`nil` 并且存储在 :code:`x` 中的值具有类型 :code:`T` 。记法 :code:`x.(T)` 被称为 *类型断言* 。

更准确地来说，如果 :code:`T` 不是一个接口类型，那么 :code:`x.(T)` 断言 :code:`x` 的动态类型和类型
:code:`T` `一致`_ 。在这种情况下， :code:`T` 必须 `实现`_ :code:`x`
的（接口）类型；否则类型断言是无效的，因为对于 :code:`x` 来说存储一个类型为 :code:`T`
的值是不可能的。如果 :code:`T` 是一个接口类型，那么 :code:`x.(T)` 断言 :code:`x`
的动态类型 `实现了`_ 接口 :code:`T` 。

如果类型断言成立，那么表达式的值为存储在 :code:`x` 中的值，并且其类型为 :code:`T` 。如果类型断言不成立，会发生一个 `run-time panic`_ 。换句话来说，即使 :code:`x` 的动态类型仅在运行时可知， :code:`x.(T)` 的类型也可以在一个正确的程序中被已知为 :code:`T` 。

.. code-block:: go

  var x interface{} = 7    // x 有动态类型 int 以及值 7
  i := x.(int)             // i 有类型 int 以及值 7

  type I interface { m() }

  func f(y I) {
    s := y.(string)        // 非法: string 没有实现 I (缺少方法 m)
    r := y.(io.Reader)     // r 有类型 io.Reader ，并且 y 的动态类型必须同时实现 I 和 io.Reader
    …
  }

用于 `赋值`_ 或如下特殊格式的初始化中的类型断言

.. code-block:: go

  v, ok = x.(T)
  v, ok := x.(T)
  var v, ok = x.(T)
  var v, ok interface{} = x.(T) // v 和 ok 的动态类型为 T 和 bool

产生一个额外的非类型化的布尔值。如果断言成功，那么 :code:`ok` 的值为 :code:`true` 。否则为 :code:`false` ，并且 :code:`v` 的值为类型 :code:`T` 的 `零值`_ 。这种情况下不会发生 run-time panic。

.. _`函数调用`:

.. _`方法调用`:

.. _`通常的情况来求值`:

调用
------------------------------------------------------------

给定一个带 `核心类型`_ 为函数类型 :code:`F` 的表达式 :code:`f` ，

.. code-block:: go

  f(a1, a1, … an)

带实参 :code:`a1, a2, … an` 调用了 :code:`f` 。除了一种特殊情况以外，实参必须是单一值的 `可分配`_ 给 :code:`F` 的参数类型的表达式，并且它们在函数调用之前就被求值好了。上述函数表达式的类型是 :code:`F` 的结果类型。方法调用是类似的，但是方法本身是被指定为一个在该方法的接收器的值之上的选择器。

.. code-block:: go

  math.Atan2(x, y)  // 函数调用
  var pt *Point
  pt.Scale(3.5)     // 带接收器 pt 的方法调用

如果 :code:`f` 表示一个泛型函数，那么在它可以被调用前或者作为一个函数值前，必须先被 `实例化`_ 。

在一个函数调用中，函数值和实参使用 `通常的顺序`_ 被求值。在它们求值好后，调用的参数以值传递给函数，然后被调用的函数开始执行。函数的返回参数在函数返回时以值返回给调用者。

调用一个 :code:`nil` 函数会发生 `run-time panic`_ 。

作为一个特殊情况，如果一个函数或方法 :code:`g` 的返回值数量上等于且可以分别被分配给另一个函数或方法 :code:`f` 的参数，那么调用 :code:`f(g(parameters_of_g))` 将会在按序绑定了 :code:`g` 的返回值到 :code:`f` 的参数后调用 :code:`f` 。 :code:`f` 这个调用必须排除 :code:`g` 调用以外的参数，并且 :code:`g` 必须要有最少一个返回值。如果 :code:`f` 有一个最终的 :code:`...` 参数，这个参数会被分配那些在普通参数赋值完之后的剩余的 :code:`g` 的返回值。

.. code-block:: go

  func Split(s string, pos int) (string, string) {
    return s[0:pos], s[pos:]
  }

  func Join(s, t string) string {
    return s + t
  }

  if Join(Split(value, len(value)/2)) != value {
    log.Panic("test fails")
  }

如果 :code:`x` 的（类型的）方法集包含了 :code:`m` ，并且实参列表可以被分配给 :code:`m` 的形参列表，那么方法调用 :code:`x.m()` 是有效的。如果 :code:`x` 是 `可被寻址的`_ 并且 :code:`&x` 的方法集包含了 :code:`m` ，那么 :code:`x.m()` 是 :code:`(&x).m()` 的速记：

.. code-block:: go

  var p Point
  p.Scale(3.5)

这里没有明确的方法类型，也没有方法字面值。

.. _`参数传递规则`:

传递实参给 :code:`...` 参数
------------------------------------------------------------

如果 :code:`f` 是带最终参数 :code:`p` （其类型为 :code:`...T` ）的 `variadic`_ ，那么在 :code:`f` 内， :code:`p` 的类型等同于类型 :code:`[]T` 。如果 :code:`f` 在调用时没有实参给 :code:`p` ，那么传递给 :code:`p` 的值为 :code:`nil` 。否则，传递的值是一个新的类型为 :code:`[]T` 的分片，这个分片带一个底层数组，这个底层数组的连续的元素作为实参，并且必须 `可分配`_ 给 :code:`T` 。因此该分配的长度和容量是绑定到 :code:`p` 的实参的数量，而且每次调用可能会不同。

给定函数和调用

.. code-block:: go

  func Greeting(prefix string, who ...string)
  Greeting("nobody")
  Greeting("hello:", "Joe", "Anna", "Eileen")

在 :code:`Greeting` 中， :code:`who` 的值第一次调用时为 :code:`nil` ，在第二次调用时为 :code:`[]string{"Joe", "Anna", "Eileen"}` 。

如果最终的实参可分配给一个分片类型 :code:`[]T` 且其后跟着 :code:`...` 的话，它就会在不改变值的情况下传递给一个 :code:`...T` 参数。在这种情况下，不会创建新的分片。

给定一个分片 :code:`s` 和调用

.. code-block:: go

  s := []string{"James", "Jasmine"}
  Greeting("goodbye", s...)

在 :code:`Greeting` 内， :code:`who` 有和 :code:`s` 有同一个值和同一个底层数组。

.. _`实例化过的`:

.. _`类型实参`:

.. _`实例化`:

:ruby:`实例化|Instantiations`
------------------------------------------------------------

泛型或泛型函数是通过用 *类型实参* 替代类型形参而 *被实例化* 的。
实例化会分两个步骤进行：

1. 每个类型实参替换掉在泛型声明中对应的类型形参。
   这个替换行为会在整个函数或类型声明中发生，包括类型形参列表自身及列表中的每个类型。
2. 替换完成后，每个类型实参必须 `能实现`_ 对应类型形参的 `约束`_ （若有必要则实例化它）。
   否则实例化会失败。

实例化一个类型会产生一个新的非泛型的 `命名类型`_ ；
实例化一个函数会产生一个新的非泛型的函数。

.. code-block:: go

  类型形参列表           类型实参　　      替换后

  [P any]              int             int 实现了 any
  [S ~[]E, E any]      []int, int      []int 实现了 ~[]int， int 实现了 any
  [P io.Writer]        string          非法： string 未实现 io.Writer

对于泛型函数，其类型实参可以被明确地提供，或者被部份或完全 `推断`_ 。
未被 `调用`_ 的泛型函数需要类型实参列表以用于实例化；
如果列表是不完整的，那么剩下所有的实参都必须是可被推断的。
调用的泛型函数可以提供一份（可能不完整的）类型实参列表；
也可以整个省略它，前提是被省略的类型实参是可以从普通的（非类型）函数实参中推断得出的。

.. code-block:: go

  func min[T ~int|~float64](x, y T) T { … }

  f := min                   // 非法： 在非调用情况下使用 min 时，它必须用类型实参实例化
  minInt := min[int]         // minInt 类型为 func(x, y int) int
  a := minInt(2, 3)          // a 有类型为 int 的值 2
  b := min[float64](2.0, 3)  // b 有类型为 float64 的值 2.0
  c := min(b, -1)            // c 有类型为 float64 的值 -1.0

一份部份提供的类型实参列表不能是空的；至少第一个实参需存在。
这个列表是完整实参列表的前缀，剩下的实参则留待推断。简单地说，类型实参可以 「从右往左」被省略。

.. code-block:: go

  func apply[S ~[]E, E any](s S, f(E) E) S { … }

  f0 := apply[]                  // 非法： 类型实参列表不能为空
  f1 := apply[[]int]             // S 的类型实参被明确提供了， E 的则被推断出
  f2 := apply[[]string, string]  // 两个类型实参都被明确提供了

  var bytes []byte
  r := apply(bytes, func(byte) byte { … })  // 两个类型实参都是从函数实参中被推断出

对于泛型（类型，非函数），则所有类型实参都要被明确的提供。

.. _`替换映射`:

.. _`推断`:

类型推断
------------------------------------------------------------

缺失的函数类型实参可以通过一系列步骤 *被推断出* ，如下所述。
每个步骤都会尝试使用已知的信息来推断额外的类型实参。
一旦所有类型实参都已知，类型推断就会停止。
类型推断完成后，仍会将所有类型形参替换为类型实参，并验证每个类型实参是否 `实现了`_ 相关约束；
推断的类型实参可能会无法实现其约束，这种情况下实例化会失败。

类型推断基于：

* `类型形参列表`_
* 使用已知类型实参进行初始化的替换映射 *M* （如果有）
* （可能为空的）普通函数实参列表（仅适用于函数调用）

然后继续执行以下步骤：

1. 将 `函数实参类型推断`_ 应用于所有 *类型化的* 普通函数实参
2. 应用 `约束类型推断`_
3. 使用每个非类型化的函数实参的默认类型将函数实参类型推断应用于所有 *非类型化的* 函数实参
4. 应用约束类型推断

如果没有普通或非类型化的函数实参，那么对应的步骤是跳过的。
如果前一个步骤没有推断任何新的类型实参，那么约束类型推断是跳过的，
但在有缺失的类型实参时，这个步骤会至少运行一次。

替换映射 *M* 是贯穿所有步骤的，且每个步骤可能会添加条目到 *M* 。
一旦 *M* 针对每个类型形参都有一个类型实参，或推断步骤失败时，该过程就会停止。
如果一个推断过程失败了，或者在最后的步骤之后 *M* 依旧缺失类型实参，那么推断失败。

.. _`联合`:

:ruby:`类型联合|Type unification`
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

类型推断是基于 *类型联合* 的。
一个单一的联合步骤应用于一个 `替换映射`_ 和两个类型，这两个类型中的一个或两个可能是或包含有类型形参。
替换映射会追踪已知的（明确提供的或者已经被推断出的）类型实参：这个映射对每个类型形参 :code:`P`
及对应的已知类型实参 :code:`A` 包含有一个条目 :code:`P` :html-role:`&RightArrow;` :code:`A` 。
联合过程中，已知的类型实参会在比较时取代其对应类型形参的位置。
联合过程是一个寻找可以使两个类型等同的替换映射条目的过程。

对于联合过程而言，如果当前类型形参列表中的两个不包含任何类型形参的类型其本身是一致的，
或者它们是信道类型且在忽略信道方向下是一致的，或者它们的潜在类型是等同的，那么它们就是 *等同的* 。

联合过程是通过比较类型对的结构来进行的：
忽视类型形参后的结构必须是一致的，且除类型形参以外的类型必须是等同的。
一个类型中的类型形参能匹配其它类型中任何完整的子类型；
每次成功的匹配都能使一个条目被添加到替换映射中。
如果结构不一致，或者除类型形参外的类型不等同，那么联合失败。

.. TODO(gri) Somewhere we need to describe the process of adding an entry to the
   substitution map: if the entry is already present, the type argument
   values are themselves unified.

比如，如果 :code:`T1` 和 :code:`T2` 是类型形参，
那么 :code:`[]map[int]bool` 可以被以下任何联合：

.. code-block:: go

  []map[int]bool   // 类型是一致的
  T1               // 添加 T1 → []map[int]bool 到替换映射
  []T1             // 添加 T1 → map[int]bool 到替换映射
  []map[T1]T2      // 添加 T1 → int and T2 → bool 到替换映射

另一方面， :code:`[]map[int]bool` 不能被以下任何联合：

.. code-block:: go

  int              // int 不是一个分片
  struct{}         // 结构体不是分片
  []struct{}       // 结构体不是映射
  []map[T1]string  // 映射元素类型不匹配

作为这个一般规则的一个例外，因为 `定义类型`_ :code:`D` 和类型字面值 :code:`L` 是永不等同的，
所以联合过程会转而用 :code:`D` 的潜在类型和 :code:`L` 去比较。
比如，给定一个定义类型

.. code-block:: go

  type Vector []float64

以及类型字面值 :code:`[]E` ，联合过程会比较 :code:`[]float64` 和 :code:`[]E`
并且添加条目 :code:`E` :html-role:`&RightArrow;` :code:`float64` 到替换映射。

函数实参类型推断
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. In this section and the section on constraint type inference we start with examples
   rather than have the examples follow the rules as is customary elsewhere in spec.
   Hopefully this helps building an intuition and makes the rules easier to follow.

函数实参类型推断从函数实参中推荐类型实参：
如果函数形参声明时带有使用了类型形参的类型 :code:`T` ，
那么将对应函数实参的类型与 :code:`T` 进行 `联合`_ 可能会推断出被 :code:`T`
所使用的类型形参的类型实参。

例如，给定泛型函数

.. code-block:: go

  func scale[Number ~int64|~float64|~complex128](v []Number, s Number) []Number

及调用

.. code-block:: go

  var vector []float64
  scaledVector := scale(vector, 42)

:code:`Number` 的类型实参可以通过联合 :code:`vector` 的类型与对应的类型形参
从而从函数实参 :code:`vector` 中推断得出： :code:`[]float64` 与 :code:`[]Number`
在结构上是匹配的且 :code:`float64` 与 :code:`Number` 是匹配的。
这会添加条目 :code:`Number` :html-role:`&RightArrow;` :code:`float64` 到 `替换映射`_ 。
如此处第二个函数实参这样的非类型化的实参会在函数实参类型推断的第一轮中被忽略，
且只有在还有未解决的类型形参时才会被考虑。

推断会在两个单独的阶段发生；每个阶段会在一份指定的（形参、实参）配对列表上进行操作：

* 列表 *Lt* 包含了所有使用了类型形参的形参类型和 *类型化的* 的函数实参所组成的（形参、实参）配对。
* 列表 *Lu* 包含了所有剩下的参数类型是单一类型形参的配对。在这个列表中，各自的函数实参都是非类型化的。

任何其它（形参、实参）配对是被忽略的。

通过构造，在 *Lu* 中配对的实参是 *非类型化的* 常量（或一个比较的非类型化的布尔型结果）。
且因为非类型化的值的 `默认类型`_ 总为预先声明的非复合类型，它们永远无法与复合类型匹配，
所以仅考虑是单一类型形参的形参类型就足够了。

每个列表都是在一个独立阶段中处理的：

1. 在第一个阶段中， *Lt* 中每个配对的形参和实参类型会被联合。
   如果一个配对的联合过程成功了，它们可能会产生添加到替换映射 *M* 的新条目。
   如果联合失败，那么类型推断就会失败。
2. 第二个阶段考虑 :code:`Lu` 列表的条目。那些类型实参已经被确定的类型形参在这个阶段会被忽略。
   针对每一个剩下的配对，（单一类型形参的）形参类型会与对应的非类型化的实参的 `默认类型`_ 进行联合。
   如果联合失败，那么类型推断就会失败。

当联合过程成功时，即使在最后的列表元素被处理到之前所有的类型实参就都被推断出了，
每个列表的处理还是会继续进行直到所有列表元素都被考虑到。

示例：

.. code-block:: go

  func min[T ~int|~float64](x, y T) T

  var x int
  min(x, 2.0)    // T 是 int ，它是从类型化的实参 x 中推断出的；2.0 是可分配给 int 的
  min(1.0, 2.0)  // T 是 float64 ，它是从 1.0 的默认类型中推断出的，且与 2.0 的默认类型匹配
  min(1.0, 2)    // 非法： （1.0 的）默认类型 float64 与（2 的）默认类型不匹配

在示例 :code:`min(1.0, 2)` 中，处理函数实参 :code:`1.0` 会产生替换映射条目
:code:`T` :html-role:`&RightArrow;` :code:`float64` 。
因为在所有非类型化实参被考虑之前处理过程会继续，所以一个错误被报告了。
这保证了类型推断不依赖非类型化实参的顺序。

约束类型推断
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

约束类型推断通过考虑类型约束来推断类型实参。
如果类型形参 :code:`P` 有带 `核心类型`_ :code:`C` 的约束，那么
`联合`_ :code:`P` 与 :code:`C` 可能推断出额外的类型实参，可能是 :code:`P`
的类型实参，如果这个已知，那么也可能是 :code:`C` 中使用的类型形参的类型实参。

例如，考虑一个带类型形参 :code:`List` 和 :code:`Elem` 的类型形参列表：

.. code-block:: go

  [List ~[]Elem, Elem any]

因为 :code:`Elem` 是 :code:`List` 的核心类型 :code:`[]Elem` 中的一个类型形参，
所以约束类型推断可以从 :code:`List` 的类型实参中推断 :code:`Elem` 的类型。
如果该类型实参是 :code:`Bytes` ：

.. code-block:: go

  type Bytes []byte

那么联合 :code:`Bytes` 的潜在类型与该核心类型就意味着联合 :code:`[]byte` 和 :code:`[]Elem` 。
这个联合过程会成功并且产生 `替换映射`_ ： :code:`Elem` :html-role:`&RightArrow;` :code:`byte` 。
因此，在这个例子中，约束类型推断能从第一个类型实参中推断出第二个的。

使用约束的核心类型可能会丢失一些信息：
针对一个（不太可能的）约束的类型集仅包含单一 `定义类型`_ :code:`N` 的情况，
对应的核心类型是 :code:`N` 的潜在类型而不是 :code:`N` 自己。在这种情况下，
约束类型推断可能成功但是实例化会失败，因为推断的类型不在约束的类型集里。
因此，约束类型推断使用约束的 *调整后的核心类型* ：
如果类型集仅包含单一类型，那就使用这个类型；否则使用约束的核心类型。

通常，约束类型推断分两个阶段进行：从给定的替换映射 *M* 开始

1. 对所有带调整后的核心类型的类型形参，联合该类型与其类型形参。
   如果有任意联合过程失败，那么约束类型推断失败。
2. 此时，一些 *M* 中的条目可能映射了类型形参到其它类型形参或包含有类型形参的类型。
   对于 *M* 中每个条目 :code:`P` :html-role:`&RightArrow;` :code:`A` ，其中 :code:`A`
   是或者包含有 *M* 中已存条目 :code:`Q` :html-role:`&RightArrow;` :code:`B` 的
   类型形参 :code:`Q` ，用对应的 :code:`B` 替换掉这些 :code:`A` 中的 :code:`Q` 。
   在无法进行进一步替换时停止。

约束类型推断的结果是一份没有类型形参 :code:`P` 出现在任一 :code:`A` 中的从类型形参 :code:`P`
到类型实参 :code:`A` 的最终替换映射。

例如，给定类型形参列表

.. code-block:: go

  [A any, B []C, C *A]

以及为类型形参 A 的提供的单个类型实参 :code:`int` 。初始的替换映射 *M*
会包含条目 :code:`A` :html-role:`&RightArrow;` :code:`int` 。

在第一个阶段，类型形参 :code:`B` 和 :code:`C` 与其对应约束的核心类型联合。这个过程添加了条目
:code:`B` :html-role:`&RightArrow;` :code:`[]C` 和 :code:`C` :html-role:`&RightArrow;` :code:`*A`
到 *M* 。

此时 *M* 中存在两个右侧是或者包含有 *M* 中其它条目的类型形参（ :code:`[]C` 和 :code:`*A` ）的条目。
在第二个阶段，这些类型形参会被用它们对应的类型取代。取代的顺序是无所谓的。从第一阶段后 *M* 的状态开始：

:code:`A` :html-role:`&RightArrow;` :code:`int` ,
:code:`B` :html-role:`&RightArrow;` :code:`[]C` ,
:code:`C` :html-role:`&RightArrow;` :code:`*A`

用 :code:`int` 取代 :html-role:`&RightArrow;` 右侧的 :code:`A`

:code:`A` :html-role:`&RightArrow;` :code:`int` ,
:code:`B` :html-role:`&RightArrow;` :code:`[]C` ,
:code:`C` :html-role:`&RightArrow;` :code:`*int`

用 :code:`*int` 取代 :html-role:`&RightArrow;` 右侧的 :code:`C`

:code:`A` :html-role:`&RightArrow;` :code:`int` ,
:code:`B` :html-role:`&RightArrow;` :code:`[]*int` ,
:code:`C` :html-role:`&RightArrow;` :code:`*int`

此时没有进一步替换的可能且映射已满。因此 *M* 代表了给定类型参数列表的类型形参到类型实参的最终映射。

.. _`位移表达式`:

运算符
------------------------------------------------------------

运算符把操作数结合进一个表达式。

::

  Expression = UnaryExpr | Expression, binary_op, Expression .
  UnaryExpr  = PrimaryExpr | unary_op, UnaryExpr .

  binary_op  = "||" | "&&" | rel_op | add_op | mul_op .
  rel_op     = "==" | "!=" | "<" | "<=" | ">" | ">=" .
  add_op     = "+" | "-" | "|" | "^" .
  mul_op     = "*" | "/" | "%" | "<<" | ">>" | "&" | "&^" .

  unary_op   = "+" | "-" | "!" | "^" | "*" | "&" | "<-" .

比较运算符会在 `其它地方`_ 讨论。对于其它二元运算符来说，操作数类型必须是 `一致的`_ ，除非运算涉及位移或者非类型化的 `常量`_ 。对于只涉及常量的运算，看 `常量表达式`_ 一节。

除了位移运算之外，如果一个操作数是非类型化的 `常量`_ 而另一个操作数不是，那么该常量会被隐式地 `转换`_ 为另一个操作数的类型。

在位移表达式的右侧的操作数必须为 `整数类型`_ ，或者可以被 :code:`uint` 类型的值 `所表示的`_
非类型化的常量。如果一个非常量位移表达式的左侧的操作数是一个无符号常量，那么它会先被隐式地转换为假如位移表达式被其左侧操作数单独替换后的类型。

.. note::
  译注： 2019 年 7 月版，在上面这句话中，”无符号整数类型“变成了”整数类型“，看后文的描述，应该是正数即可，负数则会恐慌。

.. code-block:: go

  var a [1024]byte
  var s uint = 33

  // 以下示例的结果针对 64 位整型给出。
  var i = 1<<s                   // 1 的类型为 init
  var j int32 = 1<<s             // 1 的类型为 int32； j == 0
  var k = uint64(1<<s)           // 1 的类型为 uint64； k == 1<<33
  var m int = 1.0<<s             // 1.0 的类型为 int； m == 1<<33
  var n = 1.0<<s == j            // 1.0 的类型为 int32； n == true
  var o = 1<<s == 2<<s           // 1 和 2 的类型为 int； o == false
  var p = 1<<s == 1<<33          // 1 的类型为 int； p == true
  var u = 1.0<<s                 // 非法： 1.0 的类型为 float64，不能位移
  var u1 = 1.0<<s != 0           // 非法： 1.0 的类型为 float64，不能位移
  var u2 = 1<<s != 1.0           // 非法： 1 的类型为 float64，不能位移
  var v1 float32 = 1<<s          // 非法： 1 的类型为 float32，不能位移
  var v2 = string(1<<s)          // 非法： 1 被转化为字符串，不能位移
  var w int64 = 1.0<<33          // 1.0<<33 是一个常量位移表达式； w == 1<<33
  var x = a[1.0<<s]              // 恐慌： 1.0 的类型为 int；但是 1<<33 溢出了数组边界
  var b = make([]byte, 1.0<<s)   // 1.0 的类型为 int； len(b) == 1<<33

  // 以下示例的结果针对 32 位整型给出。
  // 这意味着位移会溢出
  var mm int = 1.0<<s            // 1.0 的类型为 int； mm == 0
  var oo = 1<<s == 2<<s          // 1 和 2 的类型为 int； oo == true
  var pp = 1<<s == 1<<33         // 非法： 1 的类型为 int， 但 1<<33 溢出了 int
                                 //  译注： 在这里， 1<<s 是不报错的，其会先使 1 带类型 int，
                                 //         所以在位移的时候已经溢出了，而位移溢出并不会报错
  var xx = a[1.0<<s]             // 1.0 的类型为 int； xx == a[0]
  var bb = make([]byte, 1.0<<s)  // 1.0 的类型为 int； len(bb) == 0


运算符优先级
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

一元运算符有最高的优先级。由于 :code:`++` 和 :code:`--` 运算符构成了语句（而不是表达式），超出了运算符的结构。因此，语句 :code:`*p++` 等同于 :code:`(*p)++` 。

对于二元运算符来说有五个优先级。乘法运算符束缚力最强，接下来是加法运算符，比较运算符， :code:`&&` （逻辑与），和最后的 :code:`||` （逻辑或）::

  Precedence     Operator
      5             *  /  %  <<  >>  &  &^
      4             +  -  |  ^
      3             ==  !=  <  <=  >  >=
      2             &&
      1             ||

同一优先级的二元运算符按从左到右的顺序结合。比如， :code:`x / y * z` 等同于 :code:`(x / y) * z` 。

.. code-block:: go

  +x
  23 + 3*x[i]
  x <= f()
  ^a >> b
  f() || g()
  x == y+1 && <-chanInt > 0

算数运算符
------------------------------------------------------------

算数运算符应用于数字值，并产生一个和第一个操作数具有相同类型的结果。
四个标准的算数运算符（ :code:`+` , :code:`-` , :code:`*` , :code:`/`
）应用于 `整数类型`_ 、 `浮点数类型`_ 和 `复数类型`_ ， :code:`+`
还可以应用于 `字符串类型`_ 。位逻辑运算符和位移运算符仅应用于整数。

::

  +    和                      整数，浮点数，复数值，字符串
  -    差                      整数，浮点数，复数值
  *    积                      整数，浮点数，复数值
  /    商                      整数，浮点数，复数值
  %    余                      整数

  &    按位与　  (AND)          整数
  |    按位或　  (OR)           整数
  ^    按位异或  (XOR)          整数
  &^   按位清除  (AND NOT)      整数

  <<   向左位移                 整数 << 整数 >= 0
  >>   向右位移                 整数 >> 整数 >= 0

如果操作数类型是 `类型形参`_ ，那么运算符必须应用于该类型集中的每个类型。
操作数是作为类型形式实例化时带的类型实参的值被表示的，且运算也是以该类型实参的精度计算的。
比如，给定函数：

.. code-block:: go

  func dotProduct[F ~float32|~float64](v1, v2 []F) F {
    var s F
    for i, x := range v1 {
      y := v2[i]
      s += x * y
    }
    return s
  }

:code:`x * y` 的积以及 :code:`s += x * y` 的加法是依次以 :code:`float32` 或 :code:`float64`
的精度计算的，这依赖于 :code:`F` 的类型实参。

整数运算符
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

对于两个整数值 :code:`x` 和 :code:`y` ，其整数商 :code:`q = x / y` 和余数 :code:`r = x % y` 满足如下关系::

  x = q*y + r 且 |r| < |y|

随着 :code:`x / y` 截断到零（ `「截断除法」`_ ）。

::

   x     y     x / y     x % y
   5     3       1         2
  -5     3      -1        -2
   5    -3      -1         2
  -5    -3       1        -2

这个规则有一个例外，如果对于 :code:`x` 的整数类型来说，被除数 :code:`x` 是该类型中最负的那个值，那么，因为 `补码`_ 的 `整数溢出`_ ，商 :code:`q = x / -1` 等于 :code:`x` （并且 :code:`r = 0` ）。

::

                           x, q
  int8                     -128
  int16                  -32768
  int32             -2147483648
  int64    -9223372036854775808

如果除数是一个 `常量`_ ，那么它一定不能为零。如果在运行时除数为零，那么会发生一个 `run-time panic`_ 。如果被除数不为负值并且除数可以表示为以 2 为底数的一个次方常量，那么除法可以被向右位移所替换，计算余数可以被按位与运算符所替换::

   x     x / 4     x % 4     x >> 2     x & 3
   11      2         3         2          3
  -11     -2        -3        -3          1

位移运算符通过右侧操作数（必须为非负）所指定的位移数来位移左侧的操作数。如果在运行时位移数为负，那么会发生一个 `run-time panic`_ 。如果左侧操作数是一个带符号的整数，那么位移运算符实现算数位移；如果是一个不带符号的整数，那么实现逻辑位移。位移数是没有上限的。对于 :code:`n` 个位移数来说，位移行为犹如左侧操作数以间隔 1 来位移 :code:`n` 次。因此， :code:`x << 1` 等于 :code:`x*2` 而 :code:`x >> 1` 等于 :code:`x/2` ，不过向右位移会向负无穷截断。

对于整数操作数，一元运算符 :code:`+` , :code:`-` 和 :code:`^` 有如下定义::

  +x    　　　　               是 0 + x
  -x    取其负值               是 0 - x
  ^x    按位补码               是 m ^ x ，其中对于无符号的 x 来说， m = 「所有位 置 1 」
        　　　　               　       　　　对于带符号的 x 来说， m = -1
        　　　　               　       　　　**-1 的话也是所有位置均为 1 ，但是这里需要考虑符号位**

整数溢出
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

对于无符号整数值来说， :code:`+` , :code:`-` , :code:`*` 和 :code:`<<` 运算是以 :math:`2^n` 为模来计算的， :code:`n` 为 `无符号整数`_ 类型的位宽。大致来说就是，这些无符号整数运算丢弃了溢出的高位，并且程序可以依赖于 "wrap around" 。

对于带符号整数值来说， :code:`+` , :code:`-` , :code:`*` , :code:`/` 和 :code:`<<` 运算可以合法地溢出，其产生的值是存在的并且可以被带符号整数表示法、其运算和操作数明确地定义。溢出不会发生 `run-time panic`_ 。编译器不会在不发生溢出这个假设情况下来优化代码。比如，它不会假设 :code:`x < x + 1` 始终是真。

浮点数运算符
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

对于浮点数和复数来说， :code:`+x` 和 :code:`x` 是一样的，但是 :code:`-x` 是负的 :code:`x` 。除了 IEEE-754 标准外，没有规定浮点数或者复数除以零的值；是否发生 `run-time panic`_ 是由具体实现规定的。

某个实现可能会组合多个浮点数操为单一的融合操作（可能跨语句的），
然后产生一个与单独执行指令再取整所不同的值。一个显示的 `浮点数类型`_ `转换`_
会约到目标类型的精度，以防会丢弃该舍入的融合。

比如，有些架构提供了一个“积和熔加运算”（FMA）指令，该指令在运算 :code:`x*y + z` 是不会先约取中间结果 :code:`x*y` 。这些例子展示了什么时候 Go 实现会使用这个指令：

.. code-block:: go

  // FMA 允许被用来计算 r, 因为 x*y 不会被明确地约取：
  r  = x*y + z
  r  = z;   r += x*y
  t  = x*y; r = t + z
  *p = x*y; r = *p + z
  r  = x*y + float64(z)

  // FMA 不允许被用来计算 r, 因为它会省略 x*y 的舍入:
  r  = float64(x*y) + z
  r  = z; r += float64(x*y)
  t  = float64(x*y); r = t + z

字符串连接
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

字符串使用使用 :code:`+` 运算符或者 :code:`+=` 赋值运算符来连接。

.. code-block:: go

  s := "hi" + string(c)
  s += " and good bye"

字符串加法通过连接操作数来创建了一个新的字符串。

.. _`比较`:

.. _`被比较`:

.. _`可比较的`:

.. _`其它地方`:

比较运算符
------------------------------------------------------------

比较运算符比较两个操作数，然后产生一个非类型化的布尔值。

::

  ==    等于
  !=    不等于
  <     小于
  <=    小于等于
  >     大于
  >=    大于等于

在每一个比较中，第一个操作数必须是 `可分配`_ 给第二个操作数的类型的，或者反过来。

相等运算符 :code:`==` 和 :code:`!=` 应用到 *可比较的* 操作数上。排序运算符 :code:`<` , :code:`<=` , :code:`>` 或 :code:`>=` 应用到 *可排序的* 操作数上。术语以及比较的结果定义如下：

* 布尔值是可比较的。如果两个布尔值都为 :code:`true` 或者 :code:`false` ，那么它们相等。
* 通常情况下，整数值是可比较且可排序的。
* 浮点数值是可比较且可排序的，就像 IEEE-754 标准定义的。
* 复数值是可比较的。如果存在两个复数值 :code:`u` 和 :code:`v` ，满足 :code:`real(u) == real(v)` 并且 :code:`imag(u) == imag(v)` 的话，那么它们相等。
* 字符串值是可按字节顺序比较且排序的（按照字节的词法）。
* 指针值是可比较的。如果两个指针指向同一个变量，或者两个都为 :code:`nil` 的话，那么它们相等。指向不同 `零值`_ 变量的指针可能相同也可能不同。
* 信道值是可比较的。如果两个信道值由同一个 `make`_ 调用来创建或者两个的值都为 :code:`nil` ，那么它们相同。
* 接口值是可比较的。如果两个接口值有 `一致的`_ 动态类型以及相同的动态值，或者两个的值都为 :code:`nil` ，那么它们相同。
* 当非接口类型 :code:`X` 的值是可比较的且 :code:`X` `实现了`_ 接口类型 :code:`T` ，那么
  :code:`X` 的值 :code:`x` 和 :code:`T` 的值 :code:`t` 是可比较的。如果 :code:`t`
  的动态类型和 :code:`X` 一致并且 :code:`t` 的动态值等于 :code:`x` 的话，那么它们相等。
* 当结构体的所有字段都是可比较的，那么该结构体是可比较的。如果两个结构体的对应的非 `空白`_ 字段相等，那么两个结构体相等。
* 如果数组的元素值是可比较的，那么该数组是可比较的。如果两个数组对应的元素是相等的，那么两个数组相等。

当两个比较中的接口值的动态类型一致，但是该类型的值是不可比较的时候，会发生一个 `run-time panic`_ 。这种情况不仅仅发生在接口值比较上，同样也会发生在比较接口值数组或者带接口值字段的结构体上。

分片、映射和函数值是不可比较的。不过作为一个特例，一个分片、映射或者函数值可以和预先声明的标识符 :code:`nil` 来比较。指针、信道和接口值与 :code:`nil` 的比较也是允许的，并遵循上述通用规则。

.. code-block:: go

  const c = 3 < 4            // c 是非类型化的布尔常量"真"

  type MyBool bool
  var x, y int
  var (
    // 比较的结果为一个非类型化的布尔值。
    // 应用通用赋值规则。
    b3        = x == y // b3 类型为 bool
    b4 bool   = x == y // b4 类型为 bool
    b5 MyBool = x == y // b5 类型为 MyBool
  )


逻辑运算符
------------------------------------------------------------

逻辑运算符应用于 `布尔`_ 值，并产生一个和操作数相同类型的结果。右侧的操作数是按条件来求值的。

::

  &&    条件 与     p && q  是  "如果 p 则 q 否则 false"
  ||    条件 或     p || q  是  "如果 p 则 true 否则 q"
  !     非　 　     !p      是  "非 p"

  **这边的条件与(&&)是和按位与(&)区分开来的，其它亦然**

.. _`指针间接`:

.. _`寻址`:

.. _`解引用`:

.. _`可被寻址的`:

地址运算符
------------------------------------------------------------

对于类型为 :code:`T` 的操作数 :code:`x` 来说，地址运算 :code:`&x` 生成了一个类型为 :code:`*T` 的到 :code:`x` 的指针。该操作数必须是 *可被寻址的* ，也就是，一个变量、 :ruby:`指针间接|pointer indirection` 、或分片索引操作；或一个可寻址的结构体操作数的字段选择器；或一个可寻址的数组的数组索引操作。作为可被寻址要求的一个例外， :code:`x` 也可以是（可能带括号的） `复合字面值`_ 。如果 :code:`x` 的求值会导致一个 `run-time panic`_ ，那么 :code:`&x` 的求值也会。

对于指针类型 :code:`*T` 的操作数 :code:`x` 来说，指针间接 :code:`*x` 表示被 :code:`x` 指向的类型为 :code:`T` 的 `变量`_ 。如果 :code:`x` 是 :code:`nil` ，那么对于 :code:`*x` 的求值尝试会导致一个 `run-time panic`_ 。

.. code-block:: go

  &x
  &a[f(2)]
  &Point{2, 3}
  *p
  *pf(x)

  var x *int = nil
  *x   // 导致一个 run-time panic
  &*x  // 导致一个 run-time panic

.. _`接收`:

.. _`信道接收`:

.. _`接收操作`:

接收运算符
------------------------------------------------------------

对于核心类型为 `信道类型`_ 的操作数 :code:`ch` 而言，接收操作 :code:`<-ch` 的值是从信道
:code:`ch` 接收到的值。信道方向必须允许接收操作，并且接收操作的类型为信道的元素类型。
直到一个值可用前该表达式都会阻塞。从一个 :code:`nil` 信道接收值会永远阻塞下去。针对一个 `closed`_
信道的接收操作总是会立即进行，并在之前已经发送完成的值被接收完毕后产生一个该元素类型的 `零值`_ 。

.. code-block:: go

  v1 := <-ch
  v2 = <-ch
  f(<-ch)
  <-strobe  // 等待，直到时钟脉冲一次，并丢弃接收的值

用于 `赋值`_ 或特殊格式的初始化中的接收表达式

.. code-block:: go

  x, ok = <-ch
  x, ok := <-ch
  var x, ok = <-ch
  var x, ok T = <-ch

产生一个额外的非类型化的布尔值用于报告通信是否成功。如果接收的值被到该信道的成功的发送操作传递过来，那么 :code:`ok` 的值为 :code:`true` ，如果因为该信道已经关闭且为空，接收到的是零值，那么 :code:`ok` 为 :code:`false` 。

.. _`转换`:

.. _`变量转换`:

:ruby:`转换|Conversions`
------------------------------------------------------------

转换会把一个表达式的 `类型`_ 改成被该转换所指定的类型。一个转换可能会在字面上出现在源文件中，也可能 *隐含在* 表达式所在的上下文中。

一个 *显示的* 转换是 :code:`T(x)` 这样子形式的表达式，其中 :code:`T` 是一个类型而 :code:`x` 是一个可以被转换到类型 :code:`T` 的一个表达式。

::

  Conversion = Type, "(", Expression, [ "," ], ")" .

如果类型由运算符 :code:`*` 或者 :code:`<-` 开头，或者由关键字 :code:`func` 开头并且没有结果列表，那么当必要时它必须被括起来以避免混淆：

.. code-block:: go

  *Point(p)        // 同 *(Point(p))
  (*Point)(p)      // p 被转换为 *Point
  <-chan int(c)    // 同 <-(chan int(c))
  (<-chan int)(c)  // c 被转换为 <-chan int
  func()(x)        // 函数签名 func() x
  (func())(x)      // x 被转换为 func()
  (func() int)(x)  // x 被转换为 func() int
  func() int(x)    // x 被转换为 func() int (非歧义表达式)

如果一个 `常量`_ 值 :code:`x` 可以被类型为 :code:`T` 的值 `所表示`_ ，那么 :code:`x` 可以被转换为 :code:`T` 。特殊情况下，整数常量 :code:`x` 可以使用像非常量 :code:`x` `一样的规则`_ 被显示地转换为 `字符串类型`_ 。

转换常量到一个非 `类型形参`_ 的类型会产生一个类型化的常量。

.. code-block:: go

  uint(iota)               // unit 类型的 iota 值
  float32(2.718281828)     // float32 类型的 2.718281828
  complex128(1)            // complex128 类型的 1.0 + 0.0i
  float32(0.49999999)      // float32 类型的 0.5
  float64(-1e-1000)        // float64 类型的 0.0
  string('x')              // string 类型的 "x"
  string(0x266c)           // string 类型的 "♬"
  MyString("foo" + "bar")  // MyString 类型的 "foobar"
  string([]byte{'a'})      // 不是常量: []byte{'a'} 不是常量
  (*int)(nil)              // 不是常量: nil 不是常量， *int 不是布尔、数值或字符串类型
  int(1.2)                 // 非法: 1.2 不能被 int 表示
  string(65.0)             // 非法: 65.0 不是整数常量

转换常量到一个类型形参会产生一个该类型的 *非常量化* 值，
这个值会以该类型形参实例化时所带类似实参的值来表示。
比如，给定函数：

.. code-block:: go

  func f[P ~float32|~float64]() {
    … P(1.1) …
  }

转换 :code:`P(1.1)` 产生一个类型为 :code:`P` 的非常量化值，且值 :code:`1.1` 是以
:code:`float32` 或 :code:`float64` 表示的，取决于 :code:`f` 的类型实参。
因此，如果 :code:`f` 用 :code:`float32` 类型来实例化，那么表达式 :code:`P(1.1) + 1.2`
的值会用与非常量化的 :code:`float32` 加法相同的精度来计算。

非常量值 :code:`x` 在以下这些情况下可以被转换为类型 :code:`T` ：

* :code:`x` `可分配`_ 给 :code:`T` 。
* 忽略结构体标签（见下文），
  :code:`x` 的类型和 :code:`T` 不是 `类型形参`_
  但有 `一致的`_ `潜在类型`_ 。
* 忽略结构体标签（见下文），
  :code:`x` 的类型和 :code:`T` 都不是 `命名类型`_ 的指针类型，
  并且它们的基础类型不是类型形参但有一致的潜在类型。
* :code:`x` 的类型和 :code:`T` 都是整数或者浮点数类型。
* :code:`x` 的类型和 :code:`T` 都是复数类型。
* :code:`x` 是一个整数或者一个字节/ rune 分片，并且 :code:`T` 是字符串类型。
* :code:`x` 是一个字符串并且 :code:`T` 是一个字节/ rune 分片。
* :code:`x` 是一个分片， :code:`T` 是一个到数组的指针，且该分片与数组的类型有 `一致的`_ 的元素类型。

此外，如果 :code:`T` 或 :code:`x` 的类型 :code:`V` 是类型形参，
那么如果以下条件之一满足， :code:`x` 也可以被转换为类型 :code:`T` ：

* :code:`V` 和 :code:`T` 都是类型形参且 :code:`V` 类型集中的每个类型的值都可以被转换为
  :code:`T` 类型集中的每个类型。
* 只有 :code:`V` 是类型形参且 :code:`V` 类型集中的每个类型的值都可以被转换为 :code:`T` 。
* 只有 :code:`T` 是类型形参且 :code:`x` 可以被转换为 :code:`T` 类型集中的每个类型。

在为了转换的目的而比较结构体类型是否一致时， `结构体的标签`_ 是被忽略的：

.. code-block:: go

  type Person struct {
    Name    string
    Address *struct {
      Street string
      City   string
    }
  }

  var data *struct {
    Name    string `json:"name"`
    Address *struct {
      Street string `json:"street"`
      City   string `json:"city"`
    } `json:"address"`
  }

  var person = (*Person)(data)  // 忽略标签，潜在类型是一致的

数字类型之间或者数字类型和字符串类型之间的（非常量）转换有特殊的规则。这些转换可能改变 :code:`x` 的表现方式并产生运行时成本. 所有其它的转换仅改变其类型而不会改变 :code:`x` 的表现形式。

没有语言机制可以在指针和整数间做转换。在一些受限制的情况下，包 `unsafe`_ 实现了这个功能。

数字类型间的转换
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

以下的规则应用于非常量数值间的转换：

1. 当在 `整数类型`_ 间做转换时，如果值是一个带符号整数，那么它会用符号位扩展到隐式的无限精度；
   否则它会用零扩展。然后它会截断以满足结果类型的大小。比如，如果 :code:`v := unit16(0x10F0)`
   ，那么 :code:`uint32(int8(v)) == 0xFFFFFFF0` 。这种转换总是会产生一个有效的值；也不会有溢出指示。
2. 当转换 `浮点数类型`_ 到整数时，小数部分会被丢弃（截断到零）。
3. 当转换整数或者浮点数到浮点数类型，或者 `复数`_ 到其它复数类型时，结果值会约到目标类型所规定的精度。
   比如， :code:`float32` 类型变量 :code:`x` 的值可能使用超过 IEEE-754 32 位数的精度保存着，但是
   :code:`float32(x)` 表示的是把 :code:`x` 的值约到 32 位精度的结果。类似的， :code:`x + 0.1`
   可能使用了超过 32 位精度，但是 :code:`float32(x + 0.1)` 则不然。

在所有涉及浮点数或复数的非常量转换中，如果结果类型不能表示转换后的值，转换依旧是成功的，但结果值依赖实现。

.. _`一样的规则`:

从/到字符串的转换
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

1. 转换带/不带符号的整数值到字符串类型会产生包含该数 UTF-8 表示形式的字符串。超过有效 Unicode 代码点范围的值会被转换为 :code:`\\uFFFD` 。

   .. code-block:: go

     string('a')       // "a"
     string(-1)        // "\ufffd" == "\xef\xbf\xbd"
     string(0xf8)      // "\u00f8" == "ø" == "\xc3\xb8"
     type MyString string
     MyString(0x65e5)  // "\u65e5" == "日" == "\xe6\x97\xa5"

2. 转换字节分片到字符串类型会产生一个以该分片的元素作为连续字节的字符串。

   .. code-block:: go

     string([]byte{'h', 'e', 'l', 'l', '\xc3', '\xb8'})   // "hellø"
     string([]byte{})                                     // ""
     string([]byte(nil))                                  // ""

     type MyBytes []byte
     string(MyBytes{'h', 'e', 'l', 'l', '\xc3', '\xb8'})  // "hellø"

3. 转换 rune 分片到字符串会产生一个把独立的 rune 值转换为 string 后再级联的字符串。

   .. code-block:: go

     string([]rune{0x767d, 0x9d6c, 0x7fd4})   // "\u767d\u9d6c\u7fd4" == "白鵬翔"
     string([]rune{})                         // ""
     string([]rune(nil))                      // ""

     type MyRunes []rune
     string(MyRunes{0x767d, 0x9d6c, 0x7fd4})  // "\u767d\u9d6c\u7fd4" == "白鵬翔"

4. 转换字符串类型的值到字节类型的分片会产生一个以该字符串的字节作为连续元素的分片。

   .. code-block:: go

     []byte("hellø")   // []byte{'h', 'e', 'l', 'l', '\xc3', '\xb8'}
     []byte("")        // []byte{}

     MyBytes("hellø")  // []byte{'h', 'e', 'l', 'l', '\xc3', '\xb8'}

5. 转换字符串类型到 rune 类型分片会产生一个包含该字符串独立 Unicode 代码点的分片。

   .. code-block:: go

     []rune(MyString("白鵬翔"))  // []rune{0x767d, 0x9d6c, 0x7fd4}
     []rune("")                 // []rune{}

     MyRunes("白鵬翔")           // []rune{0x767d, 0x9d6c, 0x7fd4}

从分片到数组指针的转换
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

转换一个分片到一个数组指针会产生一个到该分片底层数组的指针。当分片的 `长度`_ 小于数组的长度时，会出现 `run-time panic`_ 。

.. code-block:: go

  s := make([]byte, 2, 4)
  s0 := (*[0]byte)(s)      // s0 != nil
  s1 := (*[1]byte)(s[1:])  // &s1[0] == &s[1]
  s2 := (*[2]byte)(s)      // &s2[0] == &s[0]
  s4 := (*[4]byte)(s)      // 恐慌： len([4]byte) > len(s)

  var t []string
  t0 := (*[0]string)(t)    // t0 == nil
  t1 := (*[1]string)(t)    // 恐慌： len([1]string) > len(t)

  u := make([]byte, 0)
  u0 := (*[0]byte)(u)       // u0 != nil

常量表达式
------------------------------------------------------------

常量表达式仅包含 `常量`_ 操作数，且是在编译的时候进行计算的。

在可以合法使用布尔、数字或字符串类型操作数的地方，分别都可以使用非类型化的布尔、数字和字符串常量作为操作数。

常量 `比较`_ 总是会产生一个非类型化的布尔常量。如果常量 `位移表达式`_ 的左侧操作数是一个非类型化的常量，那么其结果是一个整数常量；否则就是和左侧操作数同一类型的常量（必须是 `整数类型`_ ）。

任何其它在非类型化的常量上的操作结果都是同一个类别的非类型化的常量；也就是：布尔、整数、浮点数、复数或者字符串常量。如果一个二元运算（非位移）的非类型化的操作数是不同类的，那么其结果是在如下列表中靠后显示的操作数的类：整数、 rune、浮点数、复数。举例：非类型化的整数常量除以非类型化的复数常量会产生一个非类型化的复数常量。

.. code-block:: go

  const a = 2 + 3.0          // a == 5.0   (非类型化的浮点数常量)
  const b = 15 / 4           // b == 3     (非类型化的整数常量)
  const c = 15 / 4.0         // c == 3.75  (非类型化的浮点数常量)
  const Θ float64 = 3/2      // Θ == 1.0   (类型为 float64, 3/2 是整数除法)
  const Π float64 = 3/2.     // Π == 1.5   (类型为 float64, 3/2. 是浮点除法)
  const d = 1 << 3.0         // d == 8     (非类型化的整数常量)
  const e = 1.0 << 3         // e == 8     (非类型化的整数常量)
  const f = int32(1) << 33   // 非法的      (常量 8589934592 对于 int32 来说溢出了)
  const g = float64(2) >> 1  // 非法的      (float64(2) 是一个类型化的浮点数常量)
  const h = "foo" > "bar"    // h == true  (非类型化的布尔常量)
  const j = true             // j == true  (非类型化的布尔常量)
  const k = 'w' + 1          // k == 'x'   (非类型化的 rune 常量)
  const l = "hi"             // l == "hi"  (非类型化的字符串常量)
  const m = string(k)        // m == "x"   (字符串类型)
  const Σ = 1 - 0.707i       //            (非类型化的复数常量)
  const Δ = Σ + 2.0e-4       //            (非类型化的复数常量)
  const Φ = iota*1i - 1/1i   //            (非类型化的复数常量)

把内置函数 complex 应用到非类型化的整数、 rune 或者浮点数常量会产生一个非类型化的复数常量。

.. code-block:: go

  const ic = complex(0, c)   // ic == 3.75i  (非类型化的复数常量)
  const iΘ = complex(0, Θ)   // iΘ == 1i     (complex128 类型)

常量表达式总是会被精确地求值；中间值和常量本身可能会需求比任何在语言中预定义的类型所支持的更大的精度。以下都是合法的声明：

.. code-block:: go

  const Huge = 1 << 100         // Huge == 1267650600228229401496703205376  (非类型化的整数常量)
  const Four int8 = Huge >> 98  // Four == 4                                (int8 类型)

常量除法或取余操作的除数一定不能是零：

.. code-block:: go

  3.14 / 0.0   // 非法的：被零除了

*类型化的* 的常量的值必须是能被该常量类型所精确得 `表示的`_ 。以下常量表达式是非法的：

.. code-block:: go

  uint(-1)     // -1 不能作为 uint 来表示
  int(3.14)    // 3.14 不能作为 int 来表示
  int64(Huge)  // 1267650600228229401496703205376 不能作为 int64 来表示
  Four * 300   // 操作数 300 不能作为 int8 (Four 的类型) 来表示
  Four * 100   // 乘积 400 不能作为 int8 (Four 的类型) 来表示

用于一元按位补码运算符 :code:`^` 的掩码符合用于非常量的规则：对于无符号常量来说所有位都是 1，而对于带符号且非类型化的常量来说，则是一个整的 -1。

.. code-block:: go

  ^1         // 非类型化的整数常量，等于 -2
  uint8(^1)  // 非法的: 相当于 uint8(-2)， -2 不能被 uint8 所表示
  ^uint8(1)  // 类型化的 uint8 常量， 相当于 0xFF ^ uint8(1) = uint8(0xFE)
  int8(^1)   // 相当于 int8(-2)
  ^int8(1)   // 相当于 -1 ^ int8(1) = -2

实现限制：编译器可能会在计算非类型化的浮点数或者复数常量表达式时凑整；请参阅 `常量`_ 一节中的实现限制。这种凑整可能导致在整数上下文中该浮点数常量表达式无效，即使它在使用无限精度计算时将是整数，反之亦然。


.. _`通常的顺序`:

求值顺序
------------------------------------------------------------

在包的级别上， `初始化依赖关系`_ 确定了 `变量声明`_ 中独立的初始化表达式的求值顺序。除此之外，当对表达式/赋值/ `return 语句`_ 的 `操作数`_ 进行求值时，所有的函数调用、方法调用和通信操作都是以词法的从左至右的顺序被求值的。

比如，在（函数局部）赋值

.. code-block:: go

  y[f()], ok = g(h(), i()+x[j()], <-c), k()

中，函数调用和通信是按照 :code:`f()` , :code:`h()` , :code:`i()` , :code:`<-c` , :code:`g()` 和 :code:`k()` 的顺序发生的。不过，以上这些事件相对于 :code:`x` 的求值和索引，以及 :code:`y` 的求值的顺序却是没有规定的。

.. code-block:: go

  a := 1
  f := func() int { a++; return a }
  x := []int{a, f()}            // x 可以是 [1, 2] 或是 [2, 2]： a 和 f() 的求值顺序没有被规定
  m := map[int]int{a: 1, a: 2}  // m 可以是 {2: 1} 或是 {2: 2}： 两个映射赋值的求值顺序没有被规定
  n := map[int]int{a: f()}      // n 可以是 {2: 3} 或是 {3: 3}： 键和值的求值顺序没有被规定

.. note::

  如上，尽管我怎么尝试都是 :code:`a++` 在前，但这里要注意绝对不能依赖这个极大概率的顺序来编码。

在包的级别上，对独立的初始化表达式来说，初始化依赖关系会覆盖掉其原本从左至右的求值规则，但不会针对在每个表达式中的操作数：

.. code-block:: go

  var a, b, c = f() + v(), g(), sqr(u()) + v()

  func f() int        { return c }
  func g() int        { return a }
  func sqr(x int) int { return x*x }

  // 函数 u 和 v 独立于其它所有的变量和函数

函数调用是按照 :code:`u()` , :code:`sqr()` , :code:`v()` , :code:`f()` , :code:`v()` 和 :code:`g()` 的顺序发生的。

在单一表达式中的浮点数操作是根据运算符的结合性来求值的。明确的括号会通过覆盖默认的结合性来影响求值。在表达式 :code:`x + (y + z)` 中，加法 :code:`y + z` 在加 :code:`x` 前被执行。

语句
========================================

语句控制着执行。

::

  Statement =
    Declaration | LabeledStmt | SimpleStmt |
    GoStmt | ReturnStmt | BreakStmt | ContinueStmt | GotoStmt |
    FallthroughStmt | Block | IfStmt | SwitchStmt | SelectStmt | ForStmt |
    DeferStmt .

  SimpleStmt = EmptyStmt | ExpressionStmt | SendStmt | IncDecStmt | Assignment | ShortVarDecl .

终止语句
------------------------------------------------------------

*终止语句* 中断了一个 `块`_ 中常规控制流。以下语句是终结的：

1. `"return"`_ 或者 `"goto"`_ 语句。
2. 对内置函数 `panic`_ 的调用。
3. 语句列表以终止语句结束的 `块`_ 。
4. 满足如下条件的 `"if"`_ 语句：

   * "else" 分支存在，并且
   * 两个分支都是终止语句。

5. 满足如下的 `"for"`_ 语句：

   * 没有针对这个 "for" 语句的 "break" 语句，并且
   * 循环条件为空，并且
   * 这个 "for" 语句没有使用 "range" 子句。

6. 满足如下的 `"switch"`_ 语句：

   * 没有针对这个 "switch" 语句的 "break" 语句，
   * 有一个 default case，并且
   * 在每个 case 中（包括默认的）的语句列表以终止语句或者一个可能带标签的 `"fallthrough"`_ 的语句结束。

7. 满足如下的 `"select"`_ 语句：

   * 没有针对这个 "select" 语句的 "break" 语句，并且
   * 在每个 case 中（包括默认的）的语句列表是存在的并以终止语句结束。

8. 标记终止语句的 `标签语句`_ 。

所有其它语句都不是终止的。

如果语句列表非空且其最后的非空语句是终止的，那么这个 `语句列表`_ 以终止语句结束。

:ruby:`空语句|Empty statements`
------------------------------------------------------------

空语句什么都不做。

::

  EmptyStmt = .

.. _`标签`:

.. _`标签语句`:

:ruby:`标签语句|Labeled statements`
------------------------------------------------------------

标签语句可以是 :code:`goto` , :code:`break` 或 :code:`continue` 语句的目标。

::

  LabeledStmt = Label, ":", Statement .
  Label       = identifier .

.. code-block:: go

  Error: log.Panic("error encountered")

.. _`表达式语句`:

:ruby:`表达式语句|Expression statements`
------------------------------------------------------------

除了特定的内置函数外，函数/方法 `调用`_ 以及 `接收操作`_ 可以作为语句上下文出现。这种语句能够被括起来。

::

  ExpressionStmt = Expression .

下述内置函数不允许出现在语句上下文中：

::

  append cap complex imag len make new real
  unsafe.Add unsafe.Alignof unsafe.Offsetof unsafe.Sizeof unsafe.Slice

.. code-block:: go

  h(x+y)
  f.Close()
  <-ch
  (<-ch)
  len("foo")  // 如果 len 是内置函数，那么是非法的

.. _`发送`:

.. _`发送语句`:

:ruby:`发送语句|Send statements`
------------------------------------------------------------

发送语句在信道上发送一个值。
信道表达式的 `核心类型`_ 必须是 `信道类型`_ ，信道方向必须允许发送操作，
并且，发送值的类型必须 `可分配`_ 为信道的元素类型。

::

  SendStmt = Channel, "<-", Expression .
  Channel  = Expression .

信道和值表达式都会在通信开始前被求值。直到发送进行前，通信都是阻塞的。在无缓冲的信道上的发送操作只有在接收端准备好后才可以进行。在带缓冲的信道上的发送操作只要缓冲区还有空间就可以进行。在关闭的信道上进行发送会产生一个 `run-time panic`_ 。在值为 :code:`nil` 的信道上的发送是会永久阻塞的。

.. code-block:: go

  ch <- 3 // 发送值 3 到信道 ch

:ruby:`自增/减语句|IncDec statements`
------------------------------------------------------------

:code:`"++"` 和 :code:`"--"` 语句用非类型化的 `常量`_ 1 来增加或减少其操作数。和赋值一样，这个操作数必须是 `可被寻址的`_ 或者是一个映射索引表达式。

::

  IncDecStmt = Expression, ( "++" | "--" ) .

以下 `赋值`_ 语句在语义上是等同的：

::

  自增/减语句　         赋值
  x++                 x += 1
  x--                 x -= 1

.. _`赋`:

.. _`赋值`:

.. _`赋值语句`:

.. _`赋值运算符`:

:ruby:`赋值语句|Assignments`
------------------------------------------------------------

::

  Assignment = ExpressionList, assign_op, ExpressionList .

::

  assign_op = [ add_op | mul_op ], "=" .

左侧的每个操作数必须是 `可被寻址的`_ ，或一个映射索引表达式，或一个（仅对 = 赋值） `空白标识符`_ 。操作数可以被括起来。

.. code-block:: go

  x = 1
  *p = f()
  a[i] = 23
  (k) = <-ch  // 同： k = <-ch

当 *op* 是一个二元 `算数运算符`_ 时， *赋值操作* :code:`x op= y` 等同于 :code:`x = x op (y)` ，不过 :code:`x` 仅求值一次。 *op=* 结构是一个单独的 token. 在此赋值操作中，无论是左侧亦或是右侧的表达式列表，都必须仅包含一个确切的单一值表达式，并且左侧的表达式不能为空白标识符。

.. code-block:: go

  a[i] <<= 2
  i &^= 1<<n

多元赋值方式分配多值运算得到的每个值到一个变量列表。这里有两种形式。第一种，右侧的操作数是譬如函数调用、 `信道`_ 、 `映射`_ 运算 、 `类型断言`_ 这样的单个多值表达式。左侧的操作数的个数必须和值的个数匹配。比如，如果 :code:`f` 是一个返回两个值的函数，

.. code-block:: go

  x, y = f()

分配第一个值给 :code:`x` ，第二个值给 :code:`y` 。第二种形式，左侧操作数的个数必须等于右侧表达式的个数，每个表达式必须是单一的值，并且右侧第 n 个表达式会分配给左侧第 n 个操作数：

.. code-block:: go

  one, two, three = '一', '二', '三'

在此赋值中， `空白标识符`_ 提供了一个忽略右侧值的方法：

.. code-block:: go

  _ = x       // 对 x 求值，但是会忽略它
  x, _ = f()  // 对 f() 求值，但是忽略了它的第二个结果值

赋值会分两个阶段进行。第一阶段，左侧的 `索引表达式`_ 和 `指针间接`_ （包括在 `选择器`_ 中隐式的指针间接）以及右侧的表达式都会按照 `通常的顺序`_ 来求值。第二阶段，赋值按从左至右的顺序进行。

.. code-block:: go

  a, b = b, a  // 交换 a 和 b

  x := []int{1, 2, 3}
  i := 0
  i, x[i] = 1, 2  // 设 i = 1, x[0] = 2

  i = 0
  x[i], i = 2, 1  // 设 x[0] = 2, i = 1

  x[0], x[0] = 1, 2  // 先设 x[0] = 1, 然后 x[0] = 2 （所以最后 x[0] == 2）

  x[1], x[3] = 4, 5  // 设 x[1] = 4, 然后设 x[3] = 5

  type Point struct { x, y int }
  var p *Point
  x[2], p.x = 6, 7  // 设 x[2] = 6, 然后设 p.x = 7

  i = 2
  x = []int{3, 5, 7}
  for i, x[i] = range x {  // 设 i, x[2] = 0, x[0]
    break
  }
  // 循环结束后， i == 0 且 x == []int{3, 5, 3}

在赋值中，每个值都必须是 `可分配`_ 给需要分配的操作数的类型的，不过会有以下特殊情况：

1. 任何类型的值都可以被分配给空白标识符。
2. 当非类型化的常量被分配给一个接口类型变量或是空白标识符时，常量会先被隐式地 `转换`_ 为它的 `默认类型`_ 。
3. 当非类型化的布尔值被分配给一个接口类型变量或是空白标识符时，它会先被隐式地转换为布尔类型。

.. _`"if"`:

If 语句
------------------------------------------------------------

"if" 语句根据布尔表达式的值来有条件地指定两个分支的执行。当表达式求值得真时， "if" 分支被执行，否则执行 "else" 分支（存在的话）。

::

  IfStmt = "if", [ SimpleStmt, ";" ], Expression, Block, [ "else", ( IfStmt | Block ) ] .

.. code-block:: go

  if x > max {
    x = max
  }

表达式可能会前缀一个简单的语句，这个语句会在表达式被求值之前执行。

.. code-block:: go

  if x := f(); x < y {
    return x
  } else if x > z {
    return z
  } else {
    return y
  }

.. _`"switch"`:

Switch 语句
------------------------------------------------------------

"switch" 语句提供了多路执行。表达式或者类型会和在 "switch" 内的 "case" 做比较去确定执行哪一个分支。

::

  SwitchStmt = ExprSwitchStmt | TypeSwitchStmt .

有两种形式：表达式开关（switch）和类型开关。在表达式开关中， case 包含了要与 switch 表达式的值作比较的表达式。在类型开关中， case 包含了要与特别说明的 switch 表达式的类型作比较的类型。 switch 表达式在一个开关语句中仅求值一次。

.. _`表达式 "switch" 语句`:

:ruby:`表达式开关|Expression switches`
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

在表达式开关中， switch 表达式先求值完毕， case 表达式（不一定是常量）则按照从左至右、从上之下的顺序进行求值；第一个和 switch 表达式相等的 case 中对应的语句会被触发执行；其它 case 则会被跳过。如果没有 case 匹配且有一个 "default" case，那么会执行这个 case 的语句。最多只能有一个 *default* case ，它可以出现在 "switch" 语句的任意位置。当 switch 表达式不存在时，其相当于有一个布尔值 :code:`true` 。

::

  ExprSwitchStmt = "switch", [ SimpleStmt, ";" ], [ Expression ], "{", { ExprCaseClause }, "}" .
  ExprCaseClause = ExprSwitchCase, ":", StatementList .
  ExprSwitchCase = "case", ExpressionList | "default" .

如果 switch 表达式求值为一个非类型化的常量，它会先被隐式地 `转换`_ 为它的 `默认类型`_ 。预定义的非类型化的值 :code:`nil` 不能用在 switch 表达式中。开关表达式类型必须是 `可比较的`_ 。

如果 case 表达式是非类型化的，那么它会先被隐式地 `转换`_ 为 switch 表达式的类型。对于每个（可能是转换过的） case 表达式 :code:`x` 和 switch 表达式的值 :code:`t` ， `比较`_ :code:`x == t` 必定是有效的。

也就是说， switch 表达式就像是被用来声明和初始化一个没有明确类型的临时变量 :code:`t` ；为了测试相等性，这个临时变量 :code:`t` 的值会和每一个 case 表达式 :code:`x` 做判断。

在一个 case 或 default 子句中，最后的非空语句可能是一个（或许带 `标签`_ 的） `"fallthrough"`_ 语句用来指示控制应从本子句流出以流入下个子句的第一个语句。不然的话控制会流到 "switch" 语句的末尾。 "fallthrough" 语句可以作为除了表达式开关的最后一个子句外的其它所有子句的最后一条语句出现。

switch 表达式可以前缀一个简单的语句，这个语句会在表达式之前被求值。

.. code-block:: go

  switch tag {
  default: s3()
  case 0, 1, 2, 3: s1()
  case 4, 5, 6, 7: s2()
  }

  switch x := f(); {  // 缺少 switch 表达式就意味着 "true"
  case x < 0: return -x
  default: return x
  }

  switch {
  case x < y: f1()
  case x < z: f2()
  case x == 4: f3()
  }

实现限制：编译器可能会不允许多个 case 表达式求值结果为相同的常量。例如，现在的编译器不允许重复的整数、浮点数或字符串常量出现在 case 表达式中。

:ruby:`类型开关|Type switches`
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

类型开关用于比较类型而不是值。其它方面和表达式开关类似。它的标识是一个特殊的 switch 表达式，这个表达式形式是一个使用了关键字 :code:`type` 而不是一个实际类型的 `类型断言`_ 。

.. code-block:: go

  switch x.(type) {
  // cases
  }

然后 case 将实际的类型 :code:`T` 与表达式 :code:`x` 的动态类型进行匹配。与类型断言一样， :code:`x` 必须是 `接口类型`_ ，但不能是类型形参，并且在 case 中的每一个非接口类型 :code:`T` 必须实现 :code:`x` 的类型。在类型开关中， case 的类型必须都是 `不同的`_ 。

::

  TypeSwitchStmt  = "switch", [ SimpleStmt, ";" ], TypeSwitchGuard, "{", { TypeCaseClause }, "}" .
  TypeSwitchGuard = [ identifier, ":=" ], PrimaryExpr, ".", "(", "type", ")" .
  TypeCaseClause  = TypeSwitchCase, ":", StatementList .
  TypeSwitchCase  = "case", TypeList | "default" .
  TypeList        = Type, { ",", Type } .

TypeSwitchGuard 可能会包含一个 `短变量声明`_ 。当这种形式被使用后，对于每一个子句，该变量都会在 TypeSwitchCase 末尾的隐式 `块`_ 中被声明。且，在仅列出一个类型的 case 子句中，该变量类型就是此列出的类型；否则，该变量类型为 TypeSwitchGuard 中表达式的类型。

除了类型外， case 子句也可以使用预声明的标识符 `nil`_ ；当 TypeSwitchGuard 中的表达式为一个 :code:`nil` 接口值时，这个 case 会被选中。最多只可以有一个 :code:`nil` case。

给定一个 :code:`interface{}` 类型的表达式 :code:`x` ，以下类型开关：

.. code-block:: go

  switch i := x.(type) {
  case nil:
    printString("x is nil")                // i 类型为 x 的类型（interface{}）
  case int:
    printInt(i)                            // i 类型为 int
  case float64:
    printFloat64(i)                        // i 类型为 float64
  case func(int) float64:
    printFunction(i)                       // i 类型为 func(int) float64
  case bool, string:
    printString("type is bool or string")  // i 类型为 x 的类型（interface{}）
  default:
    printString("don't know the type")     // i 类型为 x 的类型（interface{}）
  }

可以被重写为：

.. code-block:: go

  v := x  // x 只被求值一次
  if v == nil {
    i := v                                 // i 类型为 x 的类型（interface{}）
    printString("x is nil")
  } else if i, isInt := v.(int); isInt {
    printInt(i)                            // i 类型为 int
  } else if i, isFloat64 := v.(float64); isFloat64 {
    printFloat64(i)                        // i 类型为 float64
  } else if i, isFunc := v.(func(int) float64); isFunc {
    printFunction(i)                       // i 类型为 func(int) float64
  } else {
    _, isBool := v.(bool)
    _, isString := v.(string)
    if isBool || isString {
      i := v                         // i 类型为 x 的类型（interface{}）
      printString("type is bool or string")
    } else {
      i := v                         // i 类型为 x 的类型（interface{}）
      printString("don't know the type")
    }
  }

`类型形参`_ 或 `泛型`_ 可以作为类型在 case 中使用。
如果在 `实例化`_ 上该类型在 switch 中产生了另一个重复的条目，
那么第一个匹配的 case 会被选中。

.. code-block:: go

  func f[P any](x any) int {
    switch x.(type) {
    case P:
      return 0
    case string:
      return 1
    case []P:
      return 2
    case []byte:
      return 3
    default:
      return 4
    }
  }

  var v1 = f[string]("foo")   // v1 == 0
  var v2 = f[byte]([]byte{})  // v2 == 2

TypeSwitchGuard 可以前缀一个简单的语句，这个语句在 guard 之前被求值。

"fallthrough" 语句在类型开关中是不被允许的。

.. _`"for"`:

For 语句
------------------------------------------------------------

"for" 语句规定了一个块的重复执行。有三种形式：迭代可以被一个单一条件、一个 "for" 子句或是一个 "range" 子句控制。

::

  ForStmt = "for", [ Condition | ForClause | RangeClause ], Block .
  Condition = Expression .

带单一条件的 for 语句
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

在它最简单的形式中， "for" 语句只要一个求值为真的布尔条件来指定一个块的重复执行。这个条件的值会在每次迭代前都被求一下。空条件相当于布尔值 :code:`true` 。

.. code-block:: go

  for a < b {
    a *= 2
  }

带 for 子句的 for 语句
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

带 ForClause 的 "for" 语句也是通过其条件来控制的，但是它会额外指定一个 *init* 和 *post* 语句，比如一个赋值、增量或减量语句。 Init 语句可以是一个 `短变量声明`_ ，但 post 语句一定不是。通过 init 语句声明的变量会在每次迭代时被重复使用。

::

  ForClause = [ InitStmt ], ";", [ Condition ], ";", [ PostStmt ] .
  InitStmt = SimpleStmt .
  PostStmt = SimpleStmt .

.. code-block:: go

  for i := 0; i < 10; i++ {
    f(i)
  }

Init 语句如果非空， 则它会在首次迭代的条件求值前被执行一次； post 语句会在每次块执行完后被执行（并且只在块执行过后）。 ForClause 每个元素都可以是空的，但是 `分号`_ 是必须要有的，除非仅存在一个条件元素。如果条件也省略了，那么就相当于是布尔值 :code:`true` 。

.. code-block:: go

  for cond { S() }    同    for ; cond ; { S() }
  for      { S() }    同    for true     { S() }

带 range 子句的 for 语句
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

带 "range" 子句的 "for" 语句会彻底地迭代数组的、分片的、字符串的或映射的所有条目，或是从信道接收到的值。针对每一个条目，它在分配 *迭代值* 给对应的存在的 *迭代变量* 后再执行语句块。

::

  RangeClause = [ ExpressionList, "=" | IdentifierList, ":=" ], "range", Expression .

"range" 子句中右侧的表达式被称为 *范围表达式* ，
它的核心类型必须是数组、到数组的指针、分片、字符串、映射或是允许 `接收操作`_ 的信道。
和赋值一样，如果左侧操作数存在，那么它一定是 `可被寻址的`_ 或映射索引表达式；它们表示迭代变量。
如果范围表达式是一个信道，那么最多允许一个迭代变量，其它情况下可以最多到两个。
如果最后的迭代变量是 `空白标识符`_ ，那么这个 range 子句和没有此空白标识符的子句是等同的。

范围表达式 :code:`x` 会在开始此循环前被求值一次，但有一个例外：当存在最多一个迭代变量且 :code:`len(x)` 是 `常量`_ 时，范围表达式不被求值。

左侧的函数调用在每次迭代时被求值。对于每个迭代，如果迭代变量存在，那么对应的迭代值是按以下说明产生的：

::

  范围表达式　                                第一个值　　         第二个值

  数组 或 分片　    a  [n]E, *[n]E, or []E    索引　    i  int    a[i]    E
  字符串           s  字符串类型　             索引　    i  int    看下面的 rune
  映射　           m  map[K]V                键　　    k  K      m[k]    V
  信道　           c  chan E, <-chan E       元素　    e  E

1. 对于数组、到数组的指针或是分片值 :code:`a` ，其索引迭代值是从索引 0 开始，以递增次序产生的。如果存在最多一个迭代变量， range 循环会创建从 :code:`0` 到 :code:`len(a) - 1` 的迭代值，且不会索引进数组或分片内。对于 :code:`nil` 分片而言，迭代数是 0。
2. 对于字符串值， "range" 子句从字节索引 0 开始迭代字符串中的 Unicode 代码点。在连续的迭代上，索引值是字符串中连续 UTF-8 编码的代码点的第一个字节的索引，而第二个值（类型是 :code:`rune` ）是对应的代码点的值。如果迭代遇到了无效的 UTF-8 序列，那么第二个值会变成 Unicode 替换字符 :code:`0xFFFD` ，且下一个迭代将在字符串中前进一个字节。

   .. note::

     译注，如下这段代码有助于理解

     .. code-block:: go

       for i, c := range "\x61\xF0\x62\x63\xe4\xb8\xad\xe6\x64\x65" {
         fmt.Printf("%d -> %c [%#x, %U]\n", i, c, string(c), c)
       }
       //output:
       // 0 -> a [0x61, U+0061]
       // 1 -> � [0xefbfbd, U+FFFD]
       // 2 -> b [0x62, U+0062]
       // 3 -> c [0x63, U+0063]
       // 4 -> 中 [0xe4b8ad, U+4E2D]
       // 7 -> � [0xefbfbd, U+FFFD]
       // 8 -> d [0x64, U+0064]
       // 9 -> e [0x65, U+0065]

3. 映射的迭代顺序是未指定的，并且不能保证两次完整的迭代是相同的。如果在迭代中某个未接触到的映射条目被移除了，那么对应的迭代值就不会产生。如果在迭代中新创建了一个映射条目，那这个条目可能会在迭代中被产生也可能被跳过。对于每个条目的创建或是一个迭代到下一个迭代，选择可能很多样。如果映射是 :code:`nil` ，迭代数为 0。
4. 对于信道，产生的迭代值是在信道 `关闭`_ 前信道上发送的连续值。如果信道是 :code:`nil` ，那么范围表达式会永久阻塞。

迭代值会像 `赋值语句`_ 一样被赋值给对应的迭代变量。

迭代变量可以被 "range" 子句使用 `短变量声明`_ （:=）的形式声明。这种情况下，它们的类型会被设置为对应迭代值的类型，且它们的 `作用域`_ 是 "for" 语句块；这些变量会在每次迭代时复用。如果迭代变量是在 "for" 语句外被声明的，那么在执行完毕后，它们的值会是最后一次迭代的值。

.. code-block:: go

  var testdata *struct {
    a *[7]int
  }
  for i, _ := range testdata.a {
    // testdata.a 不会被求值; len(testdata.a) 是常量
    // i 范围从 0 到 6
    f(i)
  }

  var a [10]string
  for i, s := range a {
    // i 类型为 int
    // s 类型为 string
    // s == a[i]
    g(i, s)
  }

  var key string
  var val interface{}  // m 的元素类型可赋予 val
  m := map[string]int{"mon":0, "tue":1, "wed":2, "thu":3, "fri":4, "sat":5, "sun":6}
  for key, val = range m {
    h(key, val)
  }
  // key == 迭代中遇到的最后一个映射键
  // val == map[key]

  var ch chan Work = producer()
  for w := range ch {
    doWork(w)
  }

  // 清空信道
  for range ch {}

.. _`并行执行函数`:

Go 语句
------------------------------------------------------------

"go" 语句会在同一地址空间执行一个函数调用作为一单独的并行控制流程（ *goroutine* ）。

::

  GoStmt = "go", Expression .

表达式必须是函数或方法调用；它不能是括起来的。对内置函数的调用会有和 `表达式语句`_ 一样的限制。

在调用的 goroutine 中的函数值和参数是按 `通常的情况来求值`_ 的，但不同于普通调用的是，程序执行不会等待被调用的函数执行完毕。相反，在新的 goroutine 中的函数是独立执行的。当函数终止，其 goroutine 也会终止。如果函数存在任何返回值，这些值会在函数完成时被丢弃。

.. code-block:: go

  go Server()
  go func(ch chan<- bool) { for { sleep(10); ch <- true}} (c)

.. _`"select"`:

Select 语句
------------------------------------------------------------

"select" 语句会选择一组或是 `发送`_ 或是 `接收`_ 的操作来进行。它看起来和 `"switch"`_ 语句类似，但它所有的 case 只涉及通信操作。

::

  SelectStmt = "select", "{", { CommClause }, "}" .
  CommClause = CommCase, ":", StatementList .
  CommCase   = "case", ( SendStmt | RecvStmt ) | "default" .
  RecvStmt   = [ ExpressionList, "=" | IdentifierList, ":=" ], RecvExpr .
  RecvExpr   = Expression .

带 RecvStmt 的 case 可能会分配 RecvExpr 的结果到一个或两个变量，变量是用 `短变量声明`_ 声明的。 RecvExpr 一定是一个（可能带括号的）接收操作。最多可以有一个 *default* case ，它可以出现在 case 列表的任意位置。

"select" 语句的执行按如下几个步骤进行：

1. 对于语句中的所有 case 来说，其接收操作的信道操作数及信道以及发送语句右侧的表达式会在进入 "select" 语句时以源码的顺序被执行仅一次。结果是一组需要接收或发送的信道，以及对应的需要发送的值。无论选择哪个（如果有）通信操作进行，在这个求值中的任何副作用都会发生。 RecvStmt 左侧的带短变量声明或赋值的表达式还不会被求值。

   .. note::

     译注，如下代码可执行后参考以助于理解

     .. code-block:: go

       var a [2]int
       var ca [2]chan int
       var c0 chan int = make(chan int, 1)
       var c1 chan int = make(chan int, 1)
       ca[0] = make(chan int, 1)
       ca[1] = make(chan int, 1)
       c0 <- 10
       c1 <- 99
       ca[1] <- 1
       select {
         case a[<-ca[1]] = <-c1:
           fmt.Println(a[1])
         case ca[0]<- <-c0:
           fmt.Println(<-ca[0])
         default:
           fmt.Println("default")
       }
       fmt.Println(<-c1)
       fmt.Println(<-ca[1])
       //fmt.Println(<-ca[0])

2. 如果可以发生一个或多个通信，通过统一的伪随机选择来确定一个来进行。否则，如果有一个默认的 case，那么这个默认 case 会被选择。如果没有默认的 case，那么这个 "select" 语句会阻塞，直到至少发生了一个通信。
3. 除非被选择的 case 是默认的 case，否则各自的通信操作会被执行。
4. 如果被选择的 case 是一个带短变量声明或赋值的 RecvStmt，那么左侧的表达式会被求值且接收到的值会被分配。
5. 被选择的 case 的语句列表被执行。

由于在 :code:`nil` 信道上的通信永不会进行，所以只带 :code:`nil` 信道且没有默认 case 的 select 会永久阻塞。

.. code-block:: go

  var a []int
  var c, c1, c2, c3, c4 chan int
  var i1, i2 int
  select {
  case i1 = <-c1:
    print("received ", i1, " from c1\n")
  case c2 <- i2:
    print("sent ", i2, " to c2\n")
  case i3, ok := (<-c3):  // 同： i3, ok := <-c3
    if ok {
      print("received ", i3, " from c3\n")
    } else {
      print("c3 is closed\n")
    }
  case a[f()] = <-c4:
    // 同：
    // case t := <-c4
    //   a[f()] = t
  default:
    print("no communication\n")
  }

  for {  // 发送（伪）随机比特序列到 c
    select {
    case c <- 0:  // 注意：没有语句，没有 fallthrough，没有折叠的 case
    case c <- 1:
    }
  }

  select {}  // 永久阻塞

.. _`"return"`:

.. _`返回语句`:

Return 语句
------------------------------------------------------------

函数 :code:`F` 中的 "return" 语句会终止 :code:`F` 的执行，并可选择地提供一个或更多的返回值。任何被 :code:`F` `推迟`_ 的函数会在 :code:`F` 返回到它调用者前被执行。

::

  ReturnStmt = "return", [ ExpressionList ] .

在没有结果类型的函数中， "return" 语句一定不指定任何返回值。

.. code-block:: go

  func noResult() {
    return
  }

有三种从带结果类型的函数内返回值的方法：

1. 返回值会明确地列在 "return" 语句中。每个表达式一定是单一值的且是 `可分配`_ 给对应的函数返回类型的元素。

   .. code-block:: go

     func simpleF() int {
       return 2
     }

     func complexF1() (re float64, im float64) {
       return -7.0, -4.0
     }

2. 在 "return" 语句中的表达式列表可以是对多值函数的单一调用。效果就犹如从这个函数返回的值被分配给带对应值类型的一个临时变量，然后这些变量会跟随在 "return" 语句后，并适用上述情况指明的规则。

   .. code-block:: go

     func complexF2() (re float64, im float64) {
       return complexF1()
     }

3. 如果函数结果值对其 `结果参数`_ 规定了名字，那么表达式列表可以为空。结果参数会作为本地变量，函数也可以在需要时给它们赋值。 "return" 语句会返回这些变量的值。

   .. code-block:: go

     func complexF3() (re float64, im float64) {
       re = 7.0
       im = 4.0
       return
     }

     func (devnull) Write(p []byte) (n int, _ error) {
       n = len(p)
       return
     }

不管它们是如何声明的，在进入函数时，所有结果值都会被初始化为其类型的 `零值`_ 。指定结果的 "return" 语句会在任何推迟函数执行前设置结果参数。

实现限制：当一个和结果参数同名的实体（常量、类型或变量）在 return 位置的 `作用域`_ 内时，编译器会不允许空的表达式列表出现在 "return" 语句中。

.. code-block:: go

  func f(n int) (res int, err error) {
    if _, err := f(n-1); err != nil {
      return  // 无效的返回语句： err 被遮蔽了
    }
    return
  }

.. _`"break"`:

Break 语句
------------------------------------------------------------

"break" 语句终止在相同函数内最内层的 `"for"`_ , `"switch"`_ 或 `"select"`_ 语句的执行。

::

  BreakStmt = "break", [ Label ] .

如果这里有一个标签，那它必须是一个封闭的 "for" 、 "switch" 或 "select" 语句，然后这个就是被终止执行的那个。

.. code-block:: go

  OuterLoop:
    for i = 0; i < n; i++ {
      for j = 0; j < m; j++ {
        switch a[i][j] {
        case nil:
          state = Error
          break OuterLoop
        case item:
          state = Found
          break OuterLoop
        }
      }
    }

.. _`"continue"`:

Continue 语句
------------------------------------------------------------

"continue" 语句在发布位置开始执行最内层 `"for"`_ 循环的下一次迭代。 "for" 循环必须在同一个函数内。

::

  ContinueStmt = "continue", [ Label ] .

如果这里有一个标签，那么必须是一个闭合的 "for" 语句，然后这个就是被执行功能的那个。

.. code-block:: go

  RowLoop:
    for y, row := range rows {
      for x, data := range row {
        if data == endOfRow {
          continue RowLoop
        }
        row[x] = data + bias(x, y)
      }
    }

.. _`"goto"`:

Goto 语句
------------------------------------------------------------

"goto" 语句转移控制到相同函数内对应标签的语句。

::

  GotoStmt = "goto", Label .

.. code-block:: go

  goto Error

执行 "goto" 语句一定不会使任何在 goto 点位时还不在 `作用域`_ 内的变量进入作用域。例如，这个例子：

.. code-block:: go

    goto L  // 坏的
    v := 3
  L:

是错误的，因为跳转到标签 :code:`L` 越过了 :code:`v` 创建。

在某个 `块`_ 外的 "goto" 语句不能跳转到这个块内。例如，这个例子：

.. code-block:: go

  if n%2 == 1 {
    goto L1
  }
  for n > 0 {
    f()
    n--
  L1:
    f()
    n--
  }

是错误的，因为标签 :code:`L1` 在 "for" 语句块内，但是 "goto" 不在。

.. _`"fallthrough"`:

Fallthrough 语句
------------------------------------------------------------

"fallthrough" 语句转移控制给 `表达式 "switch" 语句`_ 内下一个 case 子句的第一条语句。它仅作为此类子句的最终非空语句使用。

::

  FallthroughStmt = "fallthrough" .

.. _`推迟`:

Defer 语句
------------------------------------------------------------

"defer" 语句会调用一个被推迟到其环绕函数返回瞬间执行的函数，对应环绕函数返回的原因要么是执行了一个 `返回语句`_ 、到达了 `函数体`_ 的底部，要么是对应的 goroutine `panicking`_ 了。

::

  DeferStmt = "defer", Expression .

这个表达式一定是一个函数或者方法调用；它不能是括起来的。对内置函数的调用会如 `表达式语句`_ 一样被限制。

每次 "defer" 语句执行时，针对调用的函数值和参数是按 `通常的情况来求值`_ 并重新保存的，但实际的函数是不调用的。相反，被推迟的函数会在其环绕函数返回前，按照被推迟的反序被瞬间调用。也就是说，如果围绕函数通过一个明确的 `return 语句`_ 返回的话，那么被推迟的函数会在所有被 return 语句所设置的结果参数 *后* ，在函数返回到其调用者 *前* 被执行。如果被推迟函数求值得 :code:`nil` ，那么执行会在该被推迟的函数被调用时（而不是在 "defer" 语句被执行时） `恐慌`_ 。

例如，如果被推迟的函数是一个 `函数字面值`_ 并且其环绕函数有在该字面值作用域内的 `命名的结果参数`_ ，那么该被推迟的函数可以在这些结果参数被返回前访问并修改它们。如果被推迟的函数有任何返回值，这些值会在函数完成时被丢弃。（也看一下 `处理恐慌`_ 一节）

.. code-block:: go

  lock(l)
  defer unlock(l)  // 解锁发生在环绕函数返回前

  // 在环绕函数返回前打印 3 2 1 0
  for i := 0; i <= 3; i++ {
    defer fmt.Print(i)
  }

  // f 会返回 42
  func f() (result int) {
    defer func() {
      // 结果会在其被 return 语句设为 6 之后再被访问
      result *= 7
    }()
    return 6
  }

内置函数
========================================

内置函数是 `预先声明`_ 的。它们和其它任何函数一样调用，但是其中有一些接受类型而不是表达式作为其第一个实参。

内置函数没有标准的 Go 类型，所以它们只能出现在 `调用`_ 表达式中；它们不能作为函数值来使用。

.. _`closed`:

.. _`关闭`:

Close
------------------------------------------------------------

对于 `核心类型`_ 为 `信道类型`_ 的实参 :code:`ch`
，内置函数 :code:`close(c)` 标明了将不会再有值被发送到这个信道。如果 :code:`ch`
是一个仅可接收的信道，那么（关闭它）是一个错误。发送到或者关闭一个已经关闭的信道会发生
`run-time panic`_ 。 关闭 :code:`nil` 信道也会发生 `run-time panic`_ 。调用 :code:`close`
后，以及任何之前被发送的值都被接收后，接收操作不会阻塞而将是会返回对应信道类型的零值。多值
`接收操作`_ 会返回一个接收到的值，随同一个信道是否已经被关闭的指示符。

.. note::

  译注，这里返回的指示符标识的其实是信道是否还有值，即 :code:`true` or :code:`false`

.. _`一些表达式`:

.. _`长度`:

.. _`len`:

.. _`cap`:

.. _`cap(a)`:

长度和容量
------------------------------------------------------------

内置函数 :code:`len` 和 :code:`cap` 获取各种类型的实参并返回一个 :code:`int` 类型结果。实现会保证结果总是一个 :code:`int` 值。

::

  调用　     实参类型　　       结果

  len(s)    字符串类型　       按字节表示的字符串长度
            [n]T, *[n]T      数组长度（== n）
            []T              分片长度
            map[K]T          映射长度（定义的键的个数）
            chan T           在信道缓冲区内排队的元素个数
            类型形参　       见下文

  cap(s)    [n]T, *[n]T      数组长度（== n）
            []T              分片容量
            chan T           信道缓冲区容量
            类型形参　       见下文

如果实参类型是一个 `类型形参`_ :code:`P` ，那么调用 :code:`len(e)`
（或对应的 :code:`cap(e)` ）必须对 :code:`P` 类型集中的每个类型有效。
其结果是类型对应 :code:`P` `实例化`_ 时类型实参的实参的长度（或对应的容量）。

分片的容量是为其底层数组所分配的空间所对应的元素个数。任何时间都满足如下关系：

::

  0 <= len(s) <= cap(s)

:code:`nil` 分片、映射或者信道的长度是 0。 :code:`nil` 分片或信道的容量是 0。

如果 :code:`s` 是一个字符串常量，那么表达式 :code:`len(s)` 是一个 `常量`_ 。如果 :code:`s` 类型是一个数组或到数组的指针且表达式 :code:`s` 不包含 `信道接收`_ 或（非常量的） `函数调用`_ 的话， 那么表达式 :code:`len(s)` 和 :code:`cap(s)` 是常量；在这种情况下， :code:`s` 是不求值的。否则的话， :code:`len` 和 :code:`cap` 的调用不是常量且 :code:`s` 会被求值。

.. code-block:: go

  const (
    c1 = imag(2i)                    // imag(2i) = 2.0 是一个常量
    c2 = len([10]float64{2})         // [10]float64{2} 不包含函数调用
    c3 = len([10]float64{c1})        // [10]float64{c1} 不包含函数调用
    c4 = len([10]float64{imag(2i)})  // imag(2i) 是一个常量且没有函数调用
    c5 = len([10]float64{imag(z)})   // 无效的: imag(z) 是一个非常量的函数调用
  )
  var z complex128

.. _`new`:

分配
------------------------------------------------------------

内置函数 :code:`new` 获取类型 :code:`T` ，在运行时为此类型的 `变量`_ 分配存储空间，并返回一个 `指向`_ 它的类型为 :code:`*T` 的值。这个变量会按照 `初始化值`_ 一节所描述的来初始化。

.. code-block:: go

  new(T)

例如：

.. code-block:: go

  type S struct { a int; b float64 }
  new(S)

为 :code:`S` 类型变量分配存储空间，初始化它（ :code:`a=0, b=0.0` ），然后返回含有位置地址的类型为 :code:`*S` 的一个值。

.. _`make`:

制作分片、映射和信道
------------------------------------------------------------

内置函数 :code:`make` 获取类型 :code:`T` ，可选择性地接一个类型相关的表达式列表。
:code:`T` 的 `核心类型`_ 必须是分片、映射或者信道类型。
它会返回类型为 :code:`T` 的值（不是 :code:`*T` ）。存储内容会按照 `初始化值`_ 一节所描述的来初始化。

::

  调用　            核心类型 T　　   结果

  make(T, n)       分片　          带 n 长度和容量的类型为 T 的分片
  make(T, n, m)    分片　          带 n 长度和 m 容量的类型为 T 的分片

  make(T)          映射　          类型为 T 的映射
  make(T, n)       映射　          为约 n 个元素分配了初始化空间的类型为 T 的映射

  make(T)          信道　          类型为 T 的无缓冲区信道
  make(T, n)       信道　          类型为 T 的带缓冲区且缓冲区大小为 n 的信道

每个 *大小实参* :code:`n` 和 :code:`m` ，必须为 `整数类型`_
，或有一个仅包含整数类型的 `类型集`_ ，或是一个非类型化的 `常量`_
。常量大小实参必须是非负的且可被 :code:`int` 类型值 `所表示的`_
；如果它是个非类型化的常量，那么会被给定类型 :code:`int` 。如果
:code:`n` 和 :code:`m` 都提供了且为常量，那么 :code:`n` 一定不能大于 :code:`m`
。如果在运行时 :code:`n` 为负值或者大于了 :code:`m` ，那么会发生 `run-time panic`_ 。

.. code-block:: go

  s := make([]int, 10, 100)       // len(s) == 10, cap(s) == 100 的分片
  s := make([]int, 1e3)           // len(s) == cap(s) == 1000 的分片
  s := make([]int, 1<<63)         // 非法的: len(s) 不能被 int 类型的值所表示
  s := make([]int, 10, 0)         // 非法的: len(s) > cap(s)
  c := make(chan int, 10)         // 带大小为 10 的缓冲区的信道
  m := make(map[string]int, 100)  // 带为约 100 个元素初始化空间的映射

带映射类型和大小提示 :code:`n` 来调用 :code:`make` 会创建一个带持有 :code:`n` 个映射元素初始化空间的映射。其精度表现是依赖于具体实现的。

.. note::

  译注，关于对映射的取值，详见 `索引表达式`_ 一节。

添加到和拷贝分片
------------------------------------------------------------

内置函数 :code:`append` 和 :code:`copy` 会协助常见的切片操作。对于这两个函数，其结果和实参的内存引用是否交叠无关。

`variadic`_ 函数 :code:`append` 附加零个或多个值 :code:`x` 到分片 :code:`s`
，并返回带有与 :code:`s` 相同类型的结果分片。
:code:`s` 的 `核心类型`_ 必须是 :code:`[]E` 类型的分片。
值 :code:`x` 被传递给类型为 :code:`...E` 的形参，并应用对应的 `参数传递规则`_ 。
作为一种特殊的情况，如果 :code:`s` 的核心类型是 :code:`[]byte` ，那么 :code:`append`
也接受一个核心类型为 :code:`string` 且其后紧跟着一个 :code:`...` 的字符串类型的作为第二个实参。
这种形式会添加字符串内的字节。

.. code-block:: go

  append(s S, x ...E) S  // S 的核心类型是 []E

如果 :code:`s` 的容量不足以满足额外的值，那么 :code:`append` 会分配一个新的足够大的底层数组来同时满足已经存在的分片元素和那些额外的值。否则， :code:`append` 复用原来的底层数组。

.. code-block:: go

  s0 := []int{0, 0}
  s1 := append(s0, 2)                // 附加一个单一元素　     s1 == []int{0, 0, 2}
  s2 := append(s1, 3, 5, 7)          // 附加多个元素          s2 == []int{0, 0, 2, 3, 5, 7}
  s3 := append(s2, s0...)            // 附加一个分片          s3 == []int{0, 0, 2, 3, 5, 7, 0, 0}
  s4 := append(s3[3:6], s3[2:]...)   // 附加重叠的分片　　     s4 == []int{3, 5, 7, 2, 3, 5, 7, 0, 0}

  var t []interface{}
  t = append(t, 42, 3.1415, "foo")   //                     t == []interface{}{42, 3.1415, "foo"}

  var b []byte
  b = append(b, "bar"...)            // 附加字符串内容　　     b == []byte{'b', 'a', 'r' }

函数 :code:`copy` 从源 :code:`src` 拷贝分片元素到目的 :code:`dst` 并返回拷贝的元素个数。
两个实参的 `核心类型`_ 都必须是带 `一致的`_ 元素类型的分片。
拷贝的元素数量是 :code:`len(src)` 和 :code:`len(dst)` 中的最小值。
作为一个特殊情况，如果目标的核心类型是 :code:`[]byte` ，那么 :code:`copy`
也接受带核心类型 :code:`string` 的源实参。这种形式会从字符串中拷贝字节到字节分片中。

.. code-block:: go

  copy(dst, src []T) int
  copy(dst []byte, src string) int

例子：

.. code-block:: go

  var a = [...]int{0, 1, 2, 3, 4, 5, 6, 7}
  var s = make([]int, 6)
  var b = make([]byte, 5)
  n1 := copy(s, a[0:])            // n1 == 6, s == []int{0, 1, 2, 3, 4, 5}
  n2 := copy(s, s[2:])            // n2 == 4, s == []int{2, 3, 4, 5, 4, 5}
  n3 := copy(b, "Hello, World!")  // n3 == 5, b == []byte("Hello")

.. _`delete`:

映射元素的删除
------------------------------------------------------------

内置函数 :code:`delete` 会根据键 :code:`k` 从 `映射`_ :code:`m` 中删除元素。
:code:`k` 的值必须是 `可分配`_ 给 :code:`m` 的键类型的。

.. code-block:: go

  delete(m, k)  // 从映射 m 中删除元素 m[k]

如果 :code:`m` 的类型是 `类型形参`_
，那么所有该类型集中的类型都必须是映射，且它们必须有一致的键类型。

如果映射 :code:`m` 是 :code:`nil` 或元素 :code:`m[k]` 不存在，那么 :code:`delete` 是一个空操作。

.. _`组成`:

操纵复数
------------------------------------------------------------

有三个函数用来聚合和分解复数。内置函数 :code:`complex` 用浮点的实和虚部来构造一个复值，而 :code:`real` 和 :code:`imag` 从一个复值中提取其实部和虚部。

.. code-block:: go

  complex(realPart, imaginaryPart floatT) complexT
  real(complexT) floatT
  imag(complexT) floatT

实参的类型和返回值相对应。
对于 :code:`complex` ，两个实参必须是相同的 `浮点数类型`_ 且返回类型是带对应浮点成分的
`复数类型`_ ， :code:`complex64` 对应 :code:`float32` 实参， :code:`complex128`
对应 :code:`float64` 实参。如果有一个实参求值为一个非类型化的常量，那么它会先被隐式地
`转换`_ 为另一个实参类型。
如果两个实参都求值为非类型化的常量，那么它们必须是非复数或者它们的虚部一定为零，
然后函数的返回值也是一个非类型化的复数常量。

对于 :code:`real` 和 :code:`imag` ，实参必须是复数类型，返回值是对应的浮点类型： :code:`float32` 对应 :code:`complex64` 实参， :code:`float64` 对应 :code:`complex128` 实参。如果实参求值为一个非类型化的常量，那么它必须是一个数，然后函数的返回类型是一个非类型化的浮点常量。

:code:`real` 和 :code:`imag` 函数一起组成了 :code:`complex` 的反相，所以对于一个复数类型为 :code:`Z` 的值 :code:`z` 来说， :code:`z == Z(complex(real(z), imag(z)))` 。

如果这些函数的操作数都是常量，那么返回值也是一个常量。

.. code-block:: go

  var a = complex(2, -2)             // complex128
  const b = complex(1.0, -1.4)       // 非类型化的复数常量 1 - 1.4i
  x := float32(math.Cos(math.Pi/2))  // float32
  var c64 = complex(5, -x)           // complex64
  var s int = complex(1, 0)          // 非类型化的复数常量 1 + 0i 可以被转化为 int
  _ = complex(1, 2<<s)               // 非法的： 2 被认为是浮点类型，不能位移
  var rl = real(c64)                 // float32
  var im = imag(a)                   // float64
  const c = imag(b)                  // 非类型化的常量 -1.4
  _ = imag(3 << s)                   // 非法的： 3 被认为是复数类型，不能位移

类型形参类型的实参是不被允许的。

.. _`panicking`:

.. _`panic`:

.. _`恐慌`:

处理恐慌
------------------------------------------------------------

有两个内置函数， :code:`panic` 和 :code:`recover` ，协助报告和处理 `run-time panic`_ 和程序定义的错误状态。

.. code-block:: go

  func panic(interface{})
  func recover() interface{}

当执行函数 :code:`F` 时，对 :code:`panic` 的明确调用或 `run-time panic`_ 会终止 :code:`F` 的执行。任何被 :code:`F` `推迟`_ 的函数会照常执行。然后，任何被 :code:`F` 的调用者所推迟的函数会运行，以此类推直到被在执行中 goroutine 中的顶层函数所推迟的。在这个阶段，程序会终止并且错误状态会被报告，这个错误状态包括了给 :code:`panic` 的实参的值。这个终止过程被称为 *panicking* 。

.. code-block:: go

  panic(42)
  panic("unreachable")
  panic(Error("cannot parse"))

:code:`recover` 函数允许程序管理一个 panicking goroutine 的行为。假设函数 :code:`G` 推迟了调用 :code:`recover` 的函数 :code:`D` ，且恐慌发生在了和 :code:`G` 执行的同一个 goroutine 的函数中。当运行中的被推迟的函数到达了 :code:`D` 时， :code:`D` 对 :code:`recover` 调用的返回值是传递给 :code:`panic` 调用的值。如果 :code:`D` 正常返回而没有开始一个新的 :code:`panic` ，那么 panicking 序列会停止。在这种情况中，在 :code:`G` 和 :code:`panic` 调用之间的函数状态会被丢弃，然后恢复正常的执行。接着会运行被 :code:`G` 推迟的在 :code:`D` 前的函数，然后 :code:`G` 通过返回到它的调用者来终止执行。

如果以下任何条件成立，那么 :code:`recover` 的返回值为 :code:`nil` ：

* :code:`panic` 的实参是 :code:`nil` ；
* goroutine 没有 panicking；
* :code:`recover` 没有被一个延迟函数直接调用。

在以下例子中的 :code:`protect` 函数调用了函数实参 :code:`g` 并使调用者免受 :code:`g` 中发生的 run-time panic 之害。

.. code-block:: go

  func protect(g func()) {
    defer func() {
      log.Println("done")  // 即使这里有恐慌， Println 也能正常执行
      if x := recover(); x != nil {
        log.Printf("run time panic: %v", x)
      }
    }()
    log.Println("start")
    g()
  }

Bootstrapping
------------------------------------------------------------

目前的实现提供了一些在 bootstrapping 时有用的内置函数。这些函数已经被记录完整了但是不能保证会一直存在在语言中。它们不会返回一个结果。

::

  函数　      行为

  print      打印所有实参；实参的格式化和实现有关
  println    和 print 类似，但是会在每个实参间打印空格，在结尾打印新行

实现限制： :code:`print` 和 :code:`println` 不一定要可以接受任意的实参类型，但是布尔、数字和字符串 `类型`_ 的打印一定要支持。

包
========================================

Go 程序是通过连结 *包* 来构建的。反过来，包由一个或多个源文件构成，这些源文件一起声明属于包的常量、类型、变量和函数，并且可以在同一包的所有文件中访问。这些元素可能被 `暴露`_ 并在其它包中使用。

源文件组织
------------------------------------------------------------

每个源文件都是由以下组成的：定义其所属包的包子句，一组可能为空的用于声明其想要使用内容的包的导入声明，一组可能为空的函数、类型、变量和常量声明。

::

  SourceFile = PackageClause, ";", { ImportDecl ";" }, { TopLevelDecl, ";" } .

.. _`包名`:

.. _`包子句`:

:ruby:`包子句|Package clause`
========================================

每个源文件由包子句开始，其定义了文件所属的包。

::

  PackageClause  = "package", PackageName .
  PackageName    = identifier .

PackageName 一定不能是 `空白标识符`_ 。

.. code-block:: go

  package math

共享同一包名的一组文件形成了一个包的实现。实现可能要求一个包的源文件都在同一文件夹下。

.. _`导入`:

.. _`导入路径`:

:ruby:`导入声明|Import declarations`
------------------------------------------------------------

导入声明 陈述了 这个包含声明的源文件 依赖 *被导入的* 包的功能（ `程序初始化和执行`_ ）并启用了对该包被 `暴露`_ 的标识符的访问。此导入会命名一个标识符（包名）用于被访问，以及一个表示被导入包的导入路径。

::

  ImportDecl       = "import", ( ImportSpec | "(", { ImportSpec, ";" }, ")" ) .
  ImportSpec       = [ "." | PackageName ], ImportPath .
  ImportPath       = string_lit .

PackageName 是用在 `限定标识符`_ 中来访问导入源文件中的包的暴露标识符的。它是在文件 `块`_ 中被声明的。如果 PackageName 缺失，那它默认为被导入包的 `包子句`_ 中指定的标识符。如果明确的句号（ :code:`.` ）取代名字出现了，那么所有在那个包的包 `块`_ 中声明的包的暴露标识符将在这个导入包的源文件的文件块中被声明，并且必须不带限定符来访问。

导入路径的解释是依赖于实现的，但它通常是被编译包完整文件名的子字符串，并可能是相对于已安装包的库的。

实现限制：编译器可能会限制导入路径仅使用属于 `Unicode 的`_ L, M, N, P 和 S 主类的这些非空字符串（无空格的可见字符），并也可能去除了字符 :code:`!"#$%&'()*,:;<=>?[\\]^\`{|}` 和 Unicode 替换字符 U+FFFD 。

假定我们已经编译了一个包含包子句 :code:`package math` 的包，它暴露了函数 :code:`Sin` ，并将编译好的包安装在由 :code:`"lib/math"` 标记的文件。此表格说明了 :code:`Sin` 是如何在在各种导入声明后导入包的文件中被访问的。

::

  导入声明　　                  Sin 的本地名

  import   "lib/math"         math.Sin
  import m "lib/math"         m.Sin
  import . "lib/math"         Sin

导入声明声明了导入者和被导入包的依赖关系。在包中直接/间接导入它自己是非法的，直接导入一个没有引用任何其暴露标识符的包也是非法的。仅仅为了包的副作用（初始化）来导入一个包的话，使用 `空白`_ 标识符作为明确的包名：

.. code-block:: go

  import _ "lib/math"

一个示例包
------------------------------------------------------------

这里有一个实现并发质数筛选的完整 Go 包。

.. code-block:: go

  package main

  import "fmt"

  // 发送 2, 3, 4, … 序列到信道 'ch'
  func generate(ch chan<- int) {
    for i := 2; ; i++ {
      ch <- i  // 发送 'i' 到信道 'ch'
    }
  }

  // 从信道 'src' 拷贝值到信道 'dst'
  // 移除那些可被 'prime' 整除的
  func filter(src <-chan int, dst chan<- int, prime int) {
    for i := range src {  // 遍历从 'src' 接收的值
      if i%prime != 0 {
        dst <- i  // 发送 'i' 到信道 'dst'
      }
    }
  }

  // 质数筛选: 菊花链过滤器一起处理
  func sieve() {
    ch := make(chan int)  // 创建一个新的信道
    go generate(ch)       // 启动 generate() 作为子进程
    for {
      prime := <-ch
      fmt.Print(prime, "\n")
      ch1 := make(chan int)
      go filter(ch, ch1, prime)
      ch = ch1
    }
  }

  func main() {
    sieve()
  }

.. note::

  译注，简单说明这个质数发生器，质数是在大于 1 的自然数中，除了 1 和它自身无法被其他自然数整除的数，这个菊花链简直就是把这条定义发挥到了极致。

  主要看这个 for 循环，它创建了无数条 filter gorountine:

  * 第一条是以 3 作为起始数， 2 为除数，求得的第一个不被 2 整除的数发送给 :code:`ch1` ，因为一开始数小，所以就这样子的过滤条件足以求得第一个数必为质数；
  * 接下来，输出以此条过滤器求得的第一个数即质数，并将其作为下一条过滤器的除数，再以此条过滤器获得的下一个不被 2 （即上一条过滤器的除数）整除的数作为下一条过滤器的起始数，开始下一条过滤器；
  * 这样，就可以保证接下来的每一条过滤器的起始数已经经过上一条过滤器过滤过，每条过滤器的除数固定，就这样层层过滤，就可以过滤出除了 1 和其本身不会被其他自然数整除的所有数了，即可以无穷尽地执行下去。

程序初始化和执行
========================================

.. _`初始化值`:

零值
------------------------------------------------------------

当存储空间被分配给一个 `变量`_ （无论是通过一个声明、对 :code:`new` 的调用或是新的值被创建，还是通过一个复合字面值或对 :code:`make` 的调用）且没有提供明确的初始化时，这个变量或值会被给定一个默认值。这样一个变量或值的每个元素都会被设定到其类型的 *零值* ：布尔是 :code:`false` ，数字类型是 :code:`0` ，字符串类型是 :code:`""` ，指针、函数、接口、分片、信道和映射类型是 :code:`nil` 。初始化会被递归地完成，所以打个比方，如果结构数组的元素未指定值，则都将其每个元素字段置零值。

以下两个简单声明是相等：

.. code-block:: go

  var i int
  var i int = 0

在

.. code-block:: go

  type T struct { i int; f float64; next *T }
  t := new(T)

后，如下赋值成立：

.. code-block:: go

  t.i == 0
  t.f == 0.0
  t.next == nil

完成如下声明，也是等同的

.. code-block:: go

  var t T

.. _`init 函数`:

.. _`初始化依赖关系`:

包初始化
------------------------------------------------------------

在一个包内，包级别变量初始化是逐步进行的，每个步骤以 *声明顺序* 选择不依赖未初始化变量的最早变量。

更精确地说，如果包级别变量还没被初始化且其没有 `初始化表达式`_ 或其初始化表达式没有在未声明变量中有依赖，那么它就被认为是 *准备好初始化了* 。初始化通过重复初始化下一个最早声明且准备好初始化的包级变量来进行，直到没有变量准备好初始化了。

如果在此过程结束时还有变量没初始化，且这些变量是一个或多个初始化循环的一部分，那么程序是无效的。

由在右侧的单个（多值）表达式所初始化的左侧的多个变量是一起被初始化的：如果任意一个在左侧的变量被初始化了，那么这些变量都在同一个步骤被初始化。

.. code-block:: go

  var x = a
  var a, b = f() // a 和 b 是在 x 被初始化之前一起被初始化的

为了包初始化的目的， `空白`_ 变量会被像其它被描述的变量一样对待。

在多个文件中声明的变量的声明顺序是由对应文件提交给编译器的顺序来决定的：第一个文件中声明的变量会在任何第二个文件中声明的变量之前，以此类推。

依赖关系分析不依赖实际的变量值，仅依赖于源码内的词汇 *引用* ，且按照传递轨迹来分析的。例如，如果一个变量 :code:`x` 的初始化表达式引用了一个其实体引用了变量 :code:`y` 的函数，那么 :code:`x` 依赖 :code:`y` 。具体来说：

* 到一个变量或函数的引用是表示这个变量或函数的标识符。
* 到方法 :code:`m` 的引用是一个 :code:`t.m` 形式的 `方法值`_ 或 `方法表达式`_ ，其中 :code:`t` 的（静态）类型不能是接口类型，且方法 :code:`m` 在 :code:`t` 的方法集中。结果的函数值 :code:`t.m` 是否被调用是无关紧要的。
* 如果一个变量、函数或方法 :code:`x` 的初始化表达式或主体（对于函数和方法而言）包含一个到变量 :code:`y` 或到依赖于 :code:`y` 的函数或方法的引用，那么 :code:`x` 是依赖 :code:`y` 的。

比如，给定声明

.. code-block:: go

  var (
    a = c + b  // == 9
    b = f()    // == 4
    c = f()    // == 5
    d = 3      // 初始化结束后等于 5
  )

  func f() int {
    d++
    return d
  }

初始化顺序是 :code:`d, b, c, a` 。注意的是，初始化表达式中的子表达式的顺序是无所谓的：示例中 :code:`a = c + b` 和 :code:`a = b + c` 得出的是相同的初始化顺序。

依赖分析是分包执行的；只有涉及到在当前包中声明的变量、函数和（非接口）方法的引用才会被考虑。如果变量间存在对其它的、隐藏的、数据的依赖，那么这些变量间的初始化顺序是不明的。

比如，给定声明

.. code-block:: go

  var x = I(T{}).ab()   // x 存在在 a 和 b 上的未被发现的隐藏依赖
  var _ = sideEffect()  // 与 x, a, 或 b 无关
  var a = b
  var b = 42

  type I interface      { ab() []int }
  type T struct{}
  func (T) ab() []int   { return []int{a, b} }

变量 :code:`a` 会在 :code:`b` 后被初始化，但是 :code:`x` 是在 :code:`b` 之前、在 :code:`b` 和 :code:`a` 之间、还是在 :code:`a` 之后，以及 :code:`sideEffect()` 会在什么时候被调用（在 :code:`x` 初始化前还是后）都是不明的。

变量也可以被包块中声明的不带实参和结果类型的名为 :code:`init` 的函数所初始化。

.. code-block:: go

  func init() { … }

单一包中可以定义多个这样的函数，甚至是在单一源文件内也没问题。在包块内， :code:`init` 标识符仅用于声明 :code:`init` 函数，但标识符本身是未 `声明的`_ 。因此 :code:`init` 函数不能在程序中的任何位置被引用。

不带导入声明的包是这样初始化的：按照出现在源码中的顺序分配初始化值到它所有的 **包级** 变量，再调用:code:`init` 函数（可能会在多个文件中，那就按照提交到编译器的顺序）。如果包有导入声明，那么在初始化包本身之前，被导入的包会先初始化好。如果多个包导入了一个包，那么被导入的包只会初始化一次。通过构造可以保证包的导入不存在循环初始化依赖关系。

包的初始化（变量初始化和对 :code:`init` 函数的调用）在单一 goroutine 内，循序的，每次一个包地发生。 :code:`init` 函数可以发起其它与初始化代码并行运行的 goroutine。不过，初始化过程总是会序列化 :code:`init` 函数：在上一个没有返回前不会调用下一个。

为了确保可重现的初始化行为，建议构建系统以词法文件名顺序将属于同一个包的多个文件呈现给编译器。

程序执行
------------------------------------------------------------

一个完整的程序是通过按轨迹地连接一个单一的，未导入的被叫做 *main package* 的包与其它所有其导入的包来创建的。主包的包名一定是 :code:`main` ，并且声明一个无实参也无返回值的 :code:`main` 函数。

.. code-block:: go

  func main() { … }

程序通过先初始化主包再调用 :code:`main` 函数来开始执行。当这个函数调用返回时，程序退出。并不会等待其它（非 :code:`main` ） goroutine 完成。

.. _`error`:

错误
========================================

预先声明的类型 :code:`error` 定义如下：

.. code-block:: go

  type error interface {
    Error() string
  }

它是表示错误条件的常见接口， :code:`nil` 值代表没有错误。例如，从文件读入数据的函数可能被定义为：

.. code-block:: go

  func Read(f *File, b []byte) (n int, err error)

.. _`run-time panic`:

Run-time panics
========================================

像尝试超出数组边界的索引这样的执行错误会触发一个 *run-time panic* ，它等同于带由实现所定义的接口类型 :code:`runtime.Error` 的值来对内置函数 `panic`_ 的调用，这个类型满足预先声明的接口类型 `error`_ 。表示不同运行时错误条件的确切错误值是未指定的。

.. code-block:: go

  package runtime

  type Error interface {
    error
    // 或许还有其它方法
  }

系统注意事项
========================================

.. _`unsafe`:

.. _`某些值`:

:code:`unsafe` 包
------------------------------------------------------------

编译器已知且可以通过 `导入路径`_ :code:`"unsafe"` 访问的内置包 :code:`unsafe` 提供了包括违反类型系统操作在内的用于低级编程的功能集。使用 :code:`unsafe` 的包必须手动审查以确保类型安全，且可能不具备可移植性。该包提供了以下接口：

.. code-block:: go

  package unsafe

  type ArbitraryType int  // 任意 Go 类型的简写； 它不是一个真实的类型
  type Pointer *ArbitraryType

  func Alignof(variable ArbitraryType) uintptr
  func Offsetof(selector ArbitraryType) uintptr
  func Sizeof(variable ArbitraryType) uintptr

  type IntegerType int  // 整数类型的速记；其并不是一个真正的类型
  func Add(ptr Pointer, len IntegerType) Pointer
  func Slice(ptr *ArbitraryType, len IntegerType) []ArbitraryType

.. These conversions also apply to type parameters with suitable core types.
   Determine if we can simply use core type insted of underlying type here,
   of if the general conversion rules take care of this.

:code:`Pointer` 是一个 `指针类型`_ 但是 :code:`Pointer` 值可能不能被 `解引用`_
。任何指针或 `潜在类型`_ :code:`uintptr` 的值都可以被 `转换`_
为潜在类型 :code:`Pointer` 的类型，反之亦然。在
:code:`Pointer` 和 :code:`uintptr` 间的转换效果是由实现定义的。

.. code-block:: go

  var f float64
  bits = *(*uint64)(unsafe.Pointer(&f))

  type ptr unsafe.Pointer
  bits = *(*uint64)(ptr(&f))

  var p ptr = nil

函数 :code:`Alignof` 和 :code:`Sizeof` 获取任意类型的表达式 :code:`x` 并分别返回假想变量 :code:`v` 的定位或大小（ :code:`v` 就像是通过 :code:`var v = x` 声明的）。

函数 :code:`Offsetof` 获取一个（可能带括号的） `选择器`_ :code:`s.f` （这个选择器表示由 :code:`s` 或 :code:`*s` 所表示结构体的字段 :code:`f` ），并返回相对于结构体地址的以字节表示的字段偏移量。如果 :code:`f` 是一个 `嵌入字段`_ ，那么必须可以在无需指针间接的情况下通过结构体字段访问。对于带字段 :code:`f` 的结构体 :code:`s` ：

.. code-block:: go

  uintptr(unsafe.Pointer(&s)) + unsafe.Offsetof(s.f) == uintptr(unsafe.Pointer(&s.f))

.. note::

  译注， go-1.15.3 测试，如果使用 :code:`new` 内置函数对结构体进行初始化，那么会不符合上述对字段地址的描述。

计算机架构可能会要求内存地址是 *对其的* ；也就是说，使变量的地址为一个因子的倍数，这个因子是变量类型的 :ruby:`对准值|alignment` 。函数 :code:`Alignof` 获取一个表示任意类型变量的表达式，并以字节为单位返回变量（类型）的对准值。对于一个变量 :code:`x` ：

.. code-block:: go

  uintptr(unsafe.Pointer(&x)) % unsafe.Alignof(x) == 0

如果 :code:`T` 是 `类型形参`_ ，或者它是一个包含可变大小字段或元素的数组或者结构体类型，
那么类型 :code:`T` （的变量）有 *可变大小* 。否则其大小是 *常量* 。
如果调用 :code:`Alignof` 、 :code:`Offsetof` 、 :code:`Sizeof` 时的实参
（或对于 :code:`Offsetof` 来说的选择器表达式 :code:`s.f` 中的结构体 :code:`s` ）
是常量大小的类型，那么这些调用是类型为 :code:`uintptr` 的编译时 `常量表达式`_ 。


函数 :code:`Add` 会加 :code:`len` 到 :code:`ptr` 并返回一个更新好的指针
:code:`unsafe.Pointer(uintptr(len) + uintptr(ptr))` 。
:code:`len` 实参必须为 `整数类型`_ 或者一个非类型化的 `常量`_ 。
常数 :code:`len` 实参必须可以被一个 :code:`int` 类型的值 `所表示`_
；如果它是非类型化的常量那么它会被给定类型 :code:`int` 。
`有效使用`_ :code:`Pointer` 的规则仍然适用。

函数 :code:`Slice` 返回了一个分片，该分片的底层数组起始于 :code:`ptr` 且其长度和容量为 :code:`len` 。 :code:`Slice(ptr, len)` 等同于

.. code-block:: go

  (*[len]ArbitraryType)(unsafe.Pointer(ptr))[:]

除了这样外，还有一个特殊的情况，当 :code:`ptr` 为 :code:`nil` 且 :code:`len` 为零时， :code:`Slice` 返回 :code:`nil` 。

:code:`len` 实参必须为 `整数类型`_ 或者一个非类型化的 `常量`_ 。一个常数 :code:`len` 实参必须是非负的且可以被一个 :code:`int` 类型的值 `所表示`_ ；如果它是非类型化的常量那么它会被给定类型 :code:`int` 。在运行时，如果 :code:`len` 为负，或 :code:`ptr` 为 :code:`nil` 但 :code:`len` 不为 :code:`nil` ，那么 `run-time panic`_ 会发生。

大小和对准值保证
------------------------------------------------------------

对于 `数字类型`_ ，以下大小是保证的：

::

  类型　                                以字节为单位的大小

  byte, uint8, int8                     1
  uint16, int16                         2
  uint32, int32, float32                4
  uint64, int64, float64, complex64     8
  complex128                           16

以下最小对准值属性是保证的：

1. 对于任意类型变量 :code:`x` ： :code:`unsafe.Alignof(x)` 最小为 1。
2. 对于结构体类型变量 :code:`x` ： :code:`unsafe.Alignof(x)` 是所有 :code:`unsafe.Alignof(x.f)` （对于 :code:`x` 的每个字段 :code:`f` ）中最大的值，但最小为1。
3. 对于数组类型变量 :code:`x` ： :code:`unsafe.Alignof(x)` 和数组元素类型变量的对准值相同。

.. note::
  译注，这边我一开始很纠结为什么 complex128 类型的对准值是 8 字节，后来发现 complex64 的对准值是 4 字节，所以大胆猜测它是拆开来算的

如果结构体或数组没有包含大于零大小的字段（或元素，对数组而言），那么它大小为零。两个不同的零大小的变量在内存中可能拥有同一个地址。

.. _`go.dev`: https://go.dev/
.. _`Go 1.17 编程语言规范 【译】`: https://bitbili.net/golang_1.17_spec.html
.. _`Extended Backus-Naur form`: https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form
.. _`ISO/IEC 14977:1996 PDF 压缩档`: http://standards.iso.org/ittf/PubliclyAvailableStandards/s026153_ISO_IEC_14977_1996(E).zip
.. _`UTF-8`: http://en.wikipedia.org/wiki/UTF-8
.. _`Unicode 等價性`: https://zh.wikipedia.org/wiki/Unicode等價性
.. _`The Unicode Standard 8.0`: http://www.unicode.org/versions/Unicode8.0.0/
.. _`Compart`: https://www.compart.com/en/unicode/category
.. _`Unicode 的`: https://www.unicode.org/versions/Unicode6.3.0/
.. _`补码`: https://en.wikipedia.org/wiki/Two's_complement
.. _`the commit msg of 30501bb`: https://github.com/golang/go/commit/30501bbef9fcfc9d53e611aaec4d20bb3cdb8ada
.. _`「截断除法」`: http://en.wikipedia.org/wiki/Modulo_operation
.. _`反射接口`: https://pkg.go.dev/reflect#StructTag
.. _`Talk:Significand`: https://en.wikipedia.org/wiki/Talk%3ASignificand
.. _`知乎-原码、反码、补码的产生、应用以及优缺点有哪些？`: https://www.zhihu.com/question/20159860
.. _`有效使用`: https://pkg.go.dev/unsafe#Pointer
