srcdir := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))

help: ## Prints help for targets with comments
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
# Directory to install Vim testing framework Vader and plugins required for
# testing.
bundledir := tests/vim/bundle

vader: ${bundledir}/vader.vim ${bundledir}/vimwiki ${bundledir}/panvimwiki | ${bundledir}  ## Required for tox -e vim and tests/vim/test_vimwiki_convert.py::test_vim_vader_all Clone Vader and Vimwiki. Link panvimwiki folders.

.PHONY: vader

${bundledir}/vader.vim: | ${bundledir}
	git clone https://github.com/junegunn/vader.vim.git ${bundledir}/vader.vim

${bundledir}/vimwiki: | ${bundledir}
	git clone https://github.com/vimwiki/vimwiki.git ${bundledir}/vimwiki

${bundledir}/panvimwiki: | ${bundledir}
	mkdir ${bundledir}/panvimwiki
	ln -s ${srcdir}/after ${bundledir}/panvimwiki/after
	ln -s ${srcdir}/autoload ${bundledir}/panvimwiki/autoload
	ln -s ${srcdir}/plugin ${bundledir}/panvimwiki/plugin
	ln -s ${srcdir}/doc ${bundledir}/panvimwiki/doc

${bundledir}:
	mkdir ${bundledir}

# https://raw.githubusercontent.com/plasticboy/vim-markdown/master/Makefile
build/:
	mkdir build

doc/:
	mkdir doc

docsdir := docs/_build/markdown/api

${docsdir}/panvimwiki.md ${docsdir}/panvimwiki.filter.md:
		${MAKE} --directory=docs markdown

# doc/panvimwiki.txt: README.md ${docsdir}/panvimwiki.md ${docsdir}/panvimwiki.filter.md build/go/bin/md2vim | doc/
# 		pandoc --from=markdown --to=markdown --shift-heading-level-by=-1 \
# 			README.md --output=doc/tmp.md
# 		cat ${docsdir}/panvimwiki.md ${docsdir}/panvimwiki.filter.md | sed -E \
# 			-e '/^### ([^(].*)\(/ {' -e "# match header 3 function signature" \
# 			-e 'h' -e '# save the matched line to the hold space' \
# 			-e 's/\(.*$$//' -e '# remove (args, kwargs)' \
# 			-e 'p' -e '# print trimmed header 3' \
# 			-e 'g' -e '# restore the matched line' \
# 			-e 's/### //p' -e '# change from header 3 to paragraph text' \
# 			-e '}' \
# 		>> doc/tmp.md
# 		build/go/bin/md2vim -cols 76 -tabs 2 -desc 'Filter and convert Vimwiki notes using pandoc.' \
# 			doc/tmp.md doc/panvimwiki.txt
# 		cat doc/panvimwiki.txt | sed -E \
# 			-e '1{s/([^[:space:]]+)/\*\1\*/}' \
# 			-e 's/`\|/|/g' -e "# remove left backquote from link" \
# 			-e 's/\|`/|/g' -e "# remove right backquote from link" \
# 			-e '/^.{78,}\|$$/ {' -e '# wrap table of contents over 78' \
# 				-e 'h' -e '# save the matched line to the hold space' \
# 				-e 's/^(.*)\.(\|[^|]*\|)$$/\1/' -e '# make content title' \
# 				-e 'p' -e '# print title' \
# 				-e 'g' -e '# restore the matched line' \
# 				-e 's/^.*\.(\|[^|]*\|)$$/ \1/' -e '# make link' \
# 				-e ':c' -e 's/^(.{1,77})$$/ \1/' -e 'tc' -e '# align right' \
# 				-e '}' \
# 			-e '/^.{78,}\*$$/ {' -e '# wrap HEADINGS over 78' \
# 				-e 'h' -e '# save the matched line to the hold space' \
# 				-e 's/^(.*) (\*[^*]*\*)$$/\1/' -e '# make content title' \
# 				-e 'p' -e '# print title' \
# 				-e 'g' -e '# restore the matched line' \
# 				-e 's/^.*(\*[^*]*\*)$$/ \1/' -e '# make link' \
# 				-e ':c' -e 's/^(.{1,77})$$/ \1/' -e 'tc' -e '# align right' \
# 				-e '}' \
# 			-e '/^\*\s`[^`]*`:( |$$)/ {' \
# 				-e "h" -e "# save the matched line to the hold space" \
# 				-e 's/^\*\s`([^`]{3,})`:.*/ \*\1\*/' -e "# make command reference" \
# 				-e 's/^\*\s`([^`]{1,2})`:.*/ \*panvimwiki-\1\*/' -e "# short command" \
# 				-e ":a" -e "s/^(.{1,77})$$/ \1/" -e "ta" -e "# align right" \
# 				-e "G" -e "# append the matched line after the command reference" \
# 				-e "}" \
# 			-e '/^\*\s`g:panvimwiki_[[:alnum:]_]*`$$/ {' \
# 				-e "h" -e "# save the matched line to the hold space" \
# 				-e 's/^\*\s`([^`]*)`$$/ \*\1\*/' -e "# make global variable reference" \
# 				-e ":g" -e "s/^(.{1,77})$$/ \1/" -e "tg" -e "# align right" \
# 				-e "G" -e "# append the matched line after the global variable reference" \
# 				-e "}" \
# 			> doc/tmp.md && cp -f doc/tmp.md doc/panvimwiki.txt && rm -f doc/tmp.md
# 		echo -n "\n\n    vim:textwidth=78:tabstop=4:filetype=help:norightleft:" \
# 			>> doc/panvimwiki.txt

vimdoc_targets := doc/panvimwiki.txt doc/panvimwiki-package.txt doc/panvimwiki-filter.txt
lua-filter := build/panvimdoc/scripts/include-files.lua
to := build/panvimdoc/scripts/panvimdoc.lua

vimdoc: ${vimdoc_targets} ## Convert Markdown documentation to Vim Help format in doc/panvimwiki.txt.

.PHONY: vimdoc

doc/panvimwiki.txt: README.md
doc/panvimwiki-package.txt: ${docsdir}/panvimwiki.md
doc/panvimwiki-filter.txt: ${docsdir}/panvimwiki.filter.md

# Receipe for converting Markdown to Vim help
${vimdoc_targets}: | ${lua-filter} ${to} doc/
	pandoc \
		--from=markdown \
		--shift-heading-level-by=-1 \
		--metadata=project:$(notdir $(basename $@)) \
		--lua-filter=${lua-filter} \
		--to=${to} \
		--output=$@ \
		$<
# cat ${docsdir}/panvimwiki.md ${docsdir}/panvimwiki.filter.md | sed -E \
# 	-e '/^### ([^(].*)\(/ {' -e "# match header 3 function signature" \
# 	-e 'h' -e '# save the matched line to the hold space' \
# 	-e 's/\(.*$$//' -e '# remove (args, kwargs)' \
# 	-e 'p' -e '# print trimmed header 3' \
# 	-e 'g' -e '# restore the matched line' \
# 	-e 's/### //' -e '# change from header 3 to paragraph text' \
# 	-e 's/(.*$$)/\1\n\n/' -e '# append newline' \
# 	-e '}' \
# 	>> doc/tmp.md
# cat README.md doc/tmp.md | \
# 	pandoc \
# 		--shift-heading-level-by=-1 \
# 		--metadata=project:panvimwiki \
# 		--lua-filter=${lua-filter} \
# 		--to=${to} \
# 		--output=doc/panvimwiki.txt

# Prerequire go tool chain.
# $ sudo apt-get install golang
# Install the dependencies.
build/go/bin/md2vim: | build/
	GOPATH=`pwd`/build/go go get github.com/FooSoft/md2vim

${lua-filter} ${to}: | build/
	cd build && \
	git clone https://github.com/kdheepak/panvimdoc.git

clean: ## Remove build, dist, tests/vim/bundle and docs/_build
	tox -e clean
	${MAKE} --directory=docs clean
	rm -rf ${bundledir}
	rm -f doc/*
	rm tests/vim/prepm.docx

.PHONY: clean
