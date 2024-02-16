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

vimdoc_targets := doc/panvimwiki.txt
lua-filter := build/panvimdoc/scripts

vimdoc: ${vimdoc_targets} ## Convert Markdown documentation to Vim Help format in doc/panvimwiki.txt.

.PHONY: vimdoc

doc/panvimwiki.txt: README.md

# Recipe for converting Markdown to Vim help, based on build/panvimdoc/panvimdoc.sh
${vimdoc_targets}: | ${lua-filter}/include-files.lua ${lua-filter}/panvimdoc.lua ${lua-filter}/skip-blocks.lua doc/
	pandoc \
		--citeproc \
		--shift-heading-level-by=-1 \
		--metadata=project:$(notdir $(basename $@)) \
		--metadata=vimversion: \
		--metadata=toc:true \
		--metadata=description:'Filter and convert Vimwiki notes using pandoc.' \
		--metadata=dedupsubheadings:false \
		--metadata=ignorerawblocks:true \
		--metadata=docmapping:true \
		--metadata=docmappingproject:true \
		--metadata=treesitter:true \
		--metadata=incrementheadinglevelby:0 \
		--lua-filter=${lua-filter}/include-files.lua \
		--lua-filter=${lua-filter}/skip-blocks.lua \
		--to=${lua-filter}/panvimdoc.lua \
		--output=$@ \
		$<
	pipx run pre-commit run --files $@

${lua-filter}/include-files.lua ${lua-filter}/panvimdoc.lua ${lua-filter}/skip-blocks.lua: | build/
	cd build && \
	git clone https://github.com/kdheepak/panvimdoc.git

clean: ## Remove build, dist, tests/vim/bundle and docs/_build
	tox -e clean
	${MAKE} --directory=docs clean
	rm -rf ${bundledir}
	rm -f doc/*
	rm tests/vim/prepm.docx

.PHONY: clean
