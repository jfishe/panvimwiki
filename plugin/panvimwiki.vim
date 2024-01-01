" Panvimwiki plugin
" File: panvimwiki.vim
" Description: Convert Vimwiki to other formats using pandoc
" Home: https://github.com/jfishe/panvimwiki
" Maintainer: John D. Fisher <jdfenw@gmail.com>
" Last Change: 2024-01-01

" Should we load? {{{1
if exists('g:panvimwiki_loaded') || !has("python3") || &compatible
    finish
endif
let g:panvimwiki_loaded = 1
" }}}1

" Save current &cpo and reset to Vim default compatibility options.
let s:save_cpo = &cpoptions
set cpoptions&vim

let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

" python3 << EOF
" #import sys

" # from os.path import normpath, join
" #from pathlib import Path

" #import vim

" #plugin_root_dir = Path(vim.eval("s:plugin_root_dir"))
" #python_root_dir = plugin_root_dir / "../python3"

" #sys.path.insert(0, str(python_root_dir.resolve()))
" from panvimwiki.vimwiki_week import convert_last_week
" EOF

" Restore Vim compatibility options.
let &cpoptions = s:save_cpo
unlet s:save_cpo
" vim:tabstop=2:shiftwidth=2:expandtab:textwidth=99:foldmethod=marker
