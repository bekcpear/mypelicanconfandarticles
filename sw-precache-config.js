module.exports = {
  staticFileGlobs: [
    "!(tags|categories|search).html",
    "!(drafts|tag|category)/!(tags|categories|search).html",
    "**/!(drafts|tag|category)/!(tags|categories|search).html",
		"favicon.ico",
    "images/**.*",
    "images/**/**.*",
    "static/**.*",
    "static/**/**.*",
    "theme/css/style.min.css",
    "theme/css/page.css",
    "theme/css/pygments/github.css",
		"count.js",
    "theme/js/bchk.js",
    "theme/js/tool.js",
    "theme/images/fa/solid/external-link-alt.svg",
    "theme/images/fa/solid/expand.svg",
    "theme/images/fa/solid/compress.svg",
    "theme/images/fa/solid/chevron-left.svg",
    "theme/images/fa/solid/chevron-right.svg",
    "theme/images/fa/solid/caret-square-up.svg",
    "theme/images/fa/solid/check.svg",
    "theme/images/fa/solid/undo-alt.svg",
    "theme/images/fa/solid/fill.svg",
    "theme/images/fa/regular/comment-alt.svg",
    "theme/images/fa/regular/file-code.svg",
    "theme/images/fa/regular/file-alt.svg",
    "theme/images/fa/brands/creative-commons.svg",
    "theme/images/fa/brands/creative-commons-by.svg",
    "theme/images/fa/brands/creative-commons-sa.svg",
  ],
  navigateFallback: '/offline.html',
  navigateFallbackWhitelist: [
  ],
  templateFilePath: 'service-worker.tmpl'
}
