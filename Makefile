# https://raw.githubusercontent.com/plasticboy/vim-markdown/master/Makefile
build:
	mkdir build

doc: README.md build/go/bin/md2vim
		pandoc --from=markdown --to=markdown --shift-heading-level-by=-1 \
			README.md --output=doc/tmp.md
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
