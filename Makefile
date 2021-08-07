srcdir := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))

help: ## Prints help for targets with comments
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
# Directory to install Vim testing framework Vader and plugins required for
# testing.
bundledir := tests/vim/bundle

vader: ${bundledir}/vader.vim ${bundledir}/vimwiki ${bundledir}/vimwiki_docx | ${bundledir}  ## Required for tox -e vim and tests/vim/test_vimwiki_convert.py::test_vim_vader_all Clone Vader and Vimwiki. Link vimwiki_docx folders.

.PHONY: vader

${bundledir}/vader.vim: | ${bundledir}
	git clone https://github.com/junegunn/vader.vim.git ${bundledir}/vader.vim

${bundledir}/vimwiki: | ${bundledir}
	git clone https://github.com/vimwiki/vimwiki.git ${bundledir}/vimwiki

${bundledir}/vimwiki_docx: | ${bundledir}
	mkdir ${bundledir}/vimwiki_docx
	ln -s ${srcdir}/after ${bundledir}/vimwiki_docx/after
	ln -s ${srcdir}/autoload ${bundledir}/vimwiki_docx/autoload
	ln -s ${srcdir}/plugin ${bundledir}/vimwiki_docx/plugin
	ln -s ${srcdir}/doc ${bundledir}/vimwiki_docx/doc

${bundledir}:
	mkdir ${bundledir}

# https://raw.githubusercontent.com/plasticboy/vim-markdown/master/Makefile
build:
	mkdir build

docsdir := docs/_build/text/api

${docsdir}/vimwiki_docx.txt ${docsdir}/vimwiki_docx.filter.txt:
		${MAKE} --directory=docs text

vimdoc: README.md ${docsdir}/vimwiki_docx.txt ${docsdir}/vimwiki_docx.filter.txt build/go/bin/md2vim ## Convert Markdown documentation to Vim Help format in doc/vimwiki_pandoc.txt.
		pandoc --from=markdown --to=markdown --shift-heading-level-by=-1 \
			README.md --output=doc/tmp.md
		cat ${docsdir}/vimwiki_docx.txt ${docsdir}/vimwiki_docx.filter.txt | \
			pandoc --from=rst --to=markdown \
			>> doc/tmp.md
		build/go/bin/md2vim -cols 76 -tabs 2 -desc 'Filter and convert Vimwiki notes using pandoc.' \
			doc/tmp.md doc/vimwiki_pandoc.txt
		cat doc/vimwiki_pandoc.txt | sed -E \
			-e '1{s/([^[:space:]]+)/\*\1\*/}' \
			-e 's/`\|/|/g' -e "# remove left backquote from link" \
			-e 's/\|`/|/g' -e "# remove right backquote from link" \
			-e '/^\*\s`[^`]*`:( |$$)/ {' \
				-e "h" -e "# save the matched line to the hold space" \
				-e 's/^\*\s`([^`]{3,})`:.*/ \*\1\*/' -e "# make command reference" \
				-e 's/^\*\s`([^`]{1,2})`:.*/ \*vimwiki_pandoc-\1\*/' -e "# short command" \
				-e ":a" -e "s/^(.{1,78})$$/ \1/" -e "ta" -e "# align right" \
				-e "G" -e "# append the matched line after the command reference" \
			-e "}" \
			-e '/^\*\s`g:vimwiki_pandoc_[[:alnum:]_]*`$$/ {' \
				-e "h" -e "# save the matched line to the hold space" \
				-e 's/^\*\s`([^`]*)`$$/ \*\1\*/' -e "# make global variable reference" \
				-e ":g" -e "s/^(.{1,78})$$/ \1/" -e "tg" -e "# align right" \
				-e "G" -e "# append the matched line after the global variable reference" \
			-e "}" \
			> doc/tmp.md && cp -f doc/tmp.md doc/vimwiki_pandoc.txt && rm -f doc/tmp.md
		echo -n "\n\n    vim:textwidth=78:tabstop=4:filetype=help:norightleft:" \
			>> doc/vimwiki_pandoc.txt

.PHONY: doc

# Prerequire go tool chain.
# $ sudo apt-get install golang
# Install the dependencies.
build/go/bin/md2vim: | build
	GOPATH=`pwd`/build/go go get github.com/FooSoft/md2vim

clean: ## Remove build, dist, tests/vim/bundle and docs/_build
	tox -e clean
	${MAKE} --directory=docs clean
	rm -rf ${bundledir}
	rm -f doc/*

.PHONY: clean
