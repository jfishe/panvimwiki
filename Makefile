srcdir := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))
tmpdir := $(srcdir)/tmp

# Convert Markdown documentation to Vim Help format in doc/panvimwiki.txt,
# using Lua scripts in lua-filter.
vimdoc_targets := doc/panvimwiki.txt
lua-filter := build/panvimdoc/scripts

ENVFILE := .env

# Directory to install Vim testing framework Vader and plugins required for
# testing.
bundledir := tests/vim/bundle

VADER_DIR := tests/vim
VADER_INPUT := $(VADER_DIR)/reference_citation.md

help: ## Prints help for targets with comments
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: help test vader vimdoc clean

test: vader $(ENVFILE)  ## Run pytest with pretty printing, in a virtual environment.
	uv run --env-file=.env -- pytest --pretty

vader: $(VADER_INPUT) $(bundledir)/vader.vim $(bundledir)/vimwiki $(bundledir)/panvimwiki $(ENVFILE) | $(bundledir)/ $(tmpdir)/  ## Required for tox -e vim and tests/vim/test_vimwiki_convert.py::test_vim_vader_all Clone Vader and Vimwiki. Link panvimwiki folders.

# $(VADER_INPUT): tests/func/reference_citation.md
tests/vim/%.md: tests/func/%.md
	cp $< $@

$(bundledir)/vader.vim: | $(bundledir)/
	git clone https://github.com/junegunn/vader.vim.git $(bundledir)/vader.vim

$(bundledir)/vimwiki: | $(bundledir)/
	git clone https://github.com/vimwiki/vimwiki.git $(bundledir)/vimwiki

$(bundledir)/panvimwiki: | $(bundledir)/
	mkdir $(bundledir)/panvimwiki
	ln -s $(srcdir)/after $(bundledir)/panvimwiki/after
	ln -s $(srcdir)/autoload $(bundledir)/panvimwiki/autoload
	ln -s $(srcdir)/plugin $(bundledir)/panvimwiki/plugin
	ln -s $(srcdir)/doc $(bundledir)/panvimwiki/doc

$(bundledir)/ $(tmpdir)/ build/ doc/:
	mkdir -p $@

# https://raw.githubusercontent.com/plasticboy/vim-markdown/master/Makefile
# build/:
# 	mkdir build

# doc/:
# 	mkdir doc

# Create .env file if it doesn't exist
$(ENVFILE):
	echo "TOP=$(srcdir)" > $@
	echo "TMP=$(tmpdir)" >> $@
	echo "COVERAGE_PROCESS_START=$(srcdir)/.coveragerc" >> $@

vimdoc: $(vimdoc_targets) ## Convert Markdown documentation to Vim Help format in doc/panvimwiki.txt.

doc/panvimwiki.txt: README.md

# Recipe for converting Markdown to Vim help, based on build/panvimdoc/panvimdoc.sh
$(vimdoc_targets): | $(lua-filter)/include-files.lua $(lua-filter)/panvimdoc.lua $(lua-filter)/skip-blocks.lua doc/
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
		--lua-filter=$(lua-filter)/include-files.lua \
		--lua-filter=$(lua-filter)/skip-blocks.lua \
		--to=$(lua-filter)/panvimdoc.lua \
		--output=$@ \
		$<
	uvx prek run --files $@

$(lua-filter)/include-files.lua $(lua-filter)/panvimdoc.lua $(lua-filter)/skip-blocks.lua: | build/
	cd build && \
	git clone https://github.com/kdheepak/panvimdoc.git

clean: ## Remove build, dist, tests/vim/bundle and docs/_build
	tox -e clean
	$(MAKE) --directory=docs clean
	rm -rf $(bundledir) $(tmpdir)
	rm -f doc/*
	rm .coverage .coverage.* .coverage_covimerage
	# rm tests/vim/prepm.docx
