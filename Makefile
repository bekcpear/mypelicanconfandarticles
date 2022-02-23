PY=python3
PELICAN?=pelican
PELICANOPTS?=

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
NODEJSDIR=$(BASEDIR)/bitbiliNewTheme
CONFFILE=$(BASEDIR)/pelicanconf.py
CONFFILETEST=$(BASEDIR)/pelicanconf_test.py
PUBLISHCONF=$(BASEDIR)/publishconf.py
PUBLISHCONFTEST=$(BASEDIR)/publishconf_test.py

help:
	@echo 'Makefile for a pelican Web site                                        '
	@echo '                                                                       '
	@echo 'Usage:                                                                 '
	@echo '   make clean                  remove the generated files              '
	@echo '   make cleanout               remove the output dir                   '
	@echo '   make publish                generate using production settings      '
	@echo '   make publishtest            generate using test-production settings '
	@echo '                                                                       '


rmdrafts:
	[ ! -d content/drafts ] || rm -rf content/drafts

cleanout:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)/*

clean:
	[ ! -d $(OUTPUTDIR) ] || find $(OUTPUTDIR) -not -type d -not -wholename "*/.git*"  -not -iname "*.pdf" -not -wholename "*/fa/*.svg" -not -wholename "*/cc/*.png" -delete

templ:
	cd $(NODEJSDIR) && \
		yarn run prepareDist

css: templ
	cd $(NODEJSDIR) && \
		yarn run minifyCSS

js: css
	cd $(NODEJSDIR) && \
		yarn run doWebpack

sw:
	cd $(NODEJSDIR) && \
		yarn run generateSW
	cp -a $(NODEJSDIR)/dist/assets/js/sw.js $(OUTPUTDIR)/
	cp -a $(NODEJSDIR)/dist/assets/js/sw.js $(OUTPUTDIR)/service-worker.js

rsthtml:
	(cd $(OUTPUTDIR) && find -iname "*.rst" | parallel -I@ pygmentize -f html -o @.html @)

copy_static:
	cp -a $(INPUTDIR)/assets $(OUTPUTDIR)/
	cp -a $(INPUTDIR)/demos $(OUTPUTDIR)/
	cp -a $(INPUTDIR)/images $(OUTPUTDIR)/
	cp -a $(INPUTDIR)/mis $(OUTPUTDIR)/
	cp -a $(INPUTDIR)/nocimages $(OUTPUTDIR)/
	cp -a $(INPUTDIR)/rootpath/* $(OUTPUTDIR)/

publishtest: rmdrafts cleanout js
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONFTEST) $(PELICANOPTS)
	$(MAKE) rsthtml
	$(MAKE) sw
	$(MAKE) copy_static

publish: rmdrafts cleanout js
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF) $(PELICANOPTS)
	$(MAKE) rsthtml
	$(MAKE) sw
	$(MAKE) copy_static

.PHONY: html help clean cleanout publish publishtest rmdrafts rsthtml
