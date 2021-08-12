" vim: set fdm=marker et ts=4 sw=4 sts=4:

" File: panvimwiki.vim
" Description: Convert Vimwiki to other formats using pandoc
" Author: John D. Fisher

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
