PY=python3
PELICAN?=pelican
PELICANOPTS?=

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
NODEJSDIR=$(BASEDIR)/bitbiliTheme
CONFFILE=$(BASEDIR)/pelicanconf.py
CONFFILETEST=$(BASEDIR)/pelicanconf-t.py
PUBLISHCONF=$(BASEDIR)/publishconf.py
PUBLISHCONFTEST=$(BASEDIR)/publishconf-t.py

help:
	@echo 'Makefile for a pelican Web site                                        '
	@echo '                                                                       '
	@echo 'Usage:                                                                 '
	@echo '   make html                        (re)generate the web site          '
	@echo '   make clean                       remove the generated files         '
	@echo '   make regenerate                  regenerate files upon modification '
	@echo '   make publish                     generate using production settings '
	@echo '   make serve                       serve site at http://localhost:8000'
	@echo '   make devserver                   start/restart develop_server.sh    '
	@echo '   make stopserver                  stop local server                  '
	@echo '   ssh_upload                       upload the web site via SSH        '
	@echo '   rsync_upload                     upload the web site via rsync+ssh  '
	@echo '   dropbox_upload                   upload the web site via Dropbox    '
	@echo '   ftp_upload                       upload the web site via FTP        '
	@echo '   s3_upload                        upload the web site via S3         '
	@echo '   github                           upload the web site via gh-pages   '
	@echo '                                                                       '


html:
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

htmlt:
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILETEST) $(PELICANOPTS)

drafts:
	cp -r drafts content

rmdrafts:
	[ ! -d content/drafts ] || rm -rf content/drafts
	rm -rf $(OUTPUTDIR)/*

rmcc:
	find content/ -iname "*.zht.rst" -delete

clean:
	[ ! -d $(OUTPUTDIR) ] || find $(OUTPUTDIR) -not -type d -not -wholename "*/.git*"  -not -iname "*.pdf" -not -wholename "*/fa/*.svg" -not -wholename "*/cc/*.png" -delete

cleancc: clean
	find -iname "*.zht.rst" -delete

ZH=$(shell find content -iname "*.zh.rst")

%.zht.rst: %.zh.rst
	opencc -c s2twp.json -i $^ -o $@
	sed -i 's/:lang: zh/:lang: zht/g' $@
	sed -i 's/\.zh\./\.zht\./g' $@

cc: $(patsubst %.zh.rst,%.zht.rst,$(ZH))

regenerate: cleancc
	$(PELICAN) -r $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

serve:
	cd $(OUTPUTDIR) && $(PY) -m pelican.server

devserver:
	$(BASEDIR)/develop_server.sh restart

stopserver:
	kill -9 `cat pelican.pid`
	kill -9 `cat srv.pid`
	@echo 'Stopped Pelican and SimpleHTTPServer processes running in background.'

theme:
	(cd theme && (scons -Q || make) )

css:
	cd $(NODEJSDIR) && \
		yarn sass -s compressed src/css/index.scss:static/css/index.min.css && \
		yarn sass -s compressed src/css/style.scss:static/css/style.min.css && \
		yarn sass -s compressed src/css/page.scss:static/css/page.min.css

js: css
	cd $(NODEJSDIR) && \
		find dist/ -name '*js' -delete && \
		yarn run minifyJS && \
		yarn run copyWBJS
	cp $(NODEJSDIR)/dist/workbox-window.prod.mjs* $(INPUTDIR)/static/

js-after:
	cd $(NODEJSDIR) && \
		yarn run generateSW
	cp -a $(NODEJSDIR)/dist/sw.js $(OUTPUTDIR)/
	cp -a $(NODEJSDIR)/dist/sw.js $(OUTPUTDIR)/service-worker.js

copy_static:
	cp -a $(INPUTDIR)/demos $(OUTPUTDIR)/
	cp -a $(INPUTDIR)/static $(OUTPUTDIR)/
	cp -a $(INPUTDIR)/images $(OUTPUTDIR)/
	cp -a $(INPUTDIR)/nocimages $(OUTPUTDIR)/
	cp -a $(INPUTDIR)/mis $(OUTPUTDIR)/

publishtest: rmdrafts js
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONFTEST) $(PELICANOPTS)
	$(MAKE) rsthtml
	$(MAKE) js-after
	$(MAKE) copy_static

publish: rmdrafts js
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF) $(PELICANOPTS)
	$(MAKE) rsthtml
	$(MAKE) js-after
	$(MAKE) copy_static

rsthtml:
	(cd $(OUTPUTDIR) && find -iname "*.rst" | parallel -I@ pygmentize -f html -o @.html @)

ssh_upload:
	$(MAKE) publish
	scp -P $(SSH_PORT) -r $(OUTPUTDIR)/* $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR)

rsync_upload:
	$(MAKE) publish
	rsync -e "ssh -p $(SSH_PORT)" -P -rvz --delete $(OUTPUTDIR)/ $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR) --cvs-exclude

ftp_upload:
	$(MAKE) publish
	lftp ftp://$(FTP_USER)@$(FTP_HOST) -e "mirror -R $(OUTPUTDIR) $(FTP_TARGET_DIR) ; quit"

s3_upload:
	$(MAKE) publish
	s3cmd sync $(OUTPUTDIR)/ s3://$(S3_BUCKET) --acl-public --delete-removed

github:
	(cd $(OUTPUTDIR) && git checkout master)
	$(MAKE) renderpdf
	env SITEURL="" $(MAKE) publish
	(cd $(OUTPUTDIR) && git add -A . && git commit -m "update html" && git push --quiet)

gitcafe:
	(cd $(OUTPUTDIR) && git checkout gitcafe-pages)
	env SITEURL="" $(MAKE) publish
	(cd $(OUTPUTDIR) && git add . && git commit -m "update" && git push -u gitcafe gitcafe-pages --quiet)

.PHONY: html help clean regenerate serve devserver publish ssh_upload rsync_upload dropbox_upload ftp_upload s3_upload github cc theme cleancc drafts rmdrafts rsthtml
