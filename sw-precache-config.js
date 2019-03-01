module.exports = {
  staticFileGlobs: [
    "!(index|tags|categories|search).html",
    "!(drafts|tag|category)/!(tags|categories|search).html",
    "**/!(drafts|tag|category)/!(tags|categories|search).html",
    "images/**.*",
    "images/**/**.*",
    "static/**.*",
    "static/!(highlightjs)/**.*",
    "static/!(highlightjs)/**/**.*",
    "theme/css/bootstrap.min.css",
    "theme/css/imageviewer.css",
    "theme/css/pygments/github.css",
    "theme/js/bootstrap.min.js",
    "theme/js/jquery.slim.min.js",
    "theme/js/imageviewer.min.js",
  ],
  navigateFallback: '/offline.html',
  navigateFallbackWhitelist: [
  ],
  templateFilePath: 'service-worker.tmpl'
}
