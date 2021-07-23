# https://raw.githubusercontent.com/plasticboy/vim-markdown/master/Makefile
build:
	mkdir build

doc: build/html2vimdoc build/vim-tools
	sed -e '/^\[!\[Build Status\]/d' \
	    -e '/^1\. \[/d' README.md > doc/tmp.md # remove table of contents
	build/html2vimdoc/bin/python build/vim-tools/html2vimdoc.py -f vimwiki_pandoc \
		doc/tmp.md | \
		sed -E -e "s/[[:space:]]*$$//" -e "# remove trailing spaces" \
		    -e "/^.{79,}\|$$/ {" -e "# wrap table of contents over 79" \
		    -e "h" -e "# save the matched line to the hold space" \
		    -e "s/^(.*) (\|[^|]*\|)$$/\1/" -e "# make content title" \
		    -e "p" -e "# print title" \
		    -e "g" -e "# restore the matched line" \
		    -e "s/^.* (\|[^|]*\|)$$/ \1/" -e "# make link" \
		    -e ":c" -e "s/^(.{1,78})$$/ \1/" -e "tc" -e "# align right" \
		    -e "}" \
		    -e "/^- '[^']*':( |$$)/ {" \
		    -e "h" -e "# save the matched line to the hold space" \
		    -e "s/^- '([^']{3,})':.*/ \*\1\*/" -e "# make command reference" \
		    -e "s/^- '([^']{1,2})':.*/ \*vim-markdown-\1\*/" -e "# short command" \
		    -e ":a" -e "s/^(.{1,78})$$/ \1/" -e "ta" -e "# align right" \
		    -e "G" -e "# append the matched line after the command reference" \
		    -e "}" \
		    -e "/^- 'g:vim_markdown_[[:alnum:]_]*'$$/ {" \
		    -e "h" -e "# save the matched line to the hold space" \
		    -e "s/^- '([^']*)'$$/ \*\1\*/" -e "# make global variable reference" \
		    -e ":g" -e "s/^(.{1,78})$$/ \1/" -e "tg" -e "# align right" \
		    -e "G" -e "# append the matched line after the global variable reference" \
		    -e "}" > doc/vimwiki_pandoc.sed.txt && rm -f doc/tmp.md
		md2vim README.md doc/vimwiki_pandoc.md2vim.txt
		build/html2vimdoc/bin/python build/vim-tools/html2vimdoc.py -f vimwiki_pandoc \
		README.md > doc/vimwiki_pandoc.html2vimdoc.txt

.PHONY: doc

# Prerequire Python and virtualenv.
# $ sudo pip install virtualenv
# Create the virtual environment.
# Install the dependencies.
build/html2vimdoc: build/vim-tools | build
	virtualenv build/html2vimdoc
	build/html2vimdoc/bin/python -m pip install --upgrade pip
	build/html2vimdoc/bin/python -m pip install -r build/vim-tools/requirements.txt

build/vim-tools: | build
	git clone https://github.com/ycm-core/vim-tools.git build/vim-tools
