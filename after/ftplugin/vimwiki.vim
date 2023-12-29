" Panvimwiki ftplugin
" File: vimwiki.vim
" Description: Panvimwiki additions to filetype vimwiki
" Maintainer: John D. Fisher
" Last Change: 2023-12-03

if exists('b:did_ftplugin_panvimwiki') || &compatible
            \ || !executable('pandoc') || !has('patch-8.2.0578h')
  finish
endif
let b:did_ftplugin_panvimwiki = 1  " Don't load another plugin for this buffer

let s:save_cpo = &cpo
set cpo&vim

let b:undo_ftplugin = get(b:, 'undo_ftplugin', '')
if !empty('b:undo_ftplugin')
  let b:undo_ftplugin ..=  " | unlet b:did_ftplugin_panvimwiki"
else
  let b:undo_ftplugin = "unlet b:did_ftplugin_panvimwiki"
endif

if !exists(":VimwikiConvert")
  command -buffer -bang -nargs=0 VimwikiConvert
        \ call panvimwiki#convert(<bang>0)
  let b:undo_ftplugin ..= " | delcommand VimwikiConvert"
endif
if !exists(":VimwikiConvertWeek")
  command -buffer -bang -nargs=0 VimwikiConvertWeek
        \ call panvimwiki#convert(<bang>0, 1)
  let b:undo_ftplugin ..= " | delcommand VimwikiConvertWeek"
endif

if vimwiki#vars#get_wikilocal('syntax') ==# 'markdown' && !exists(":VimwikiReference")
  command -buffer -nargs=0 VimwikiReference
        \ call panvimwiki#expand_citeproc()
  let b:undo_ftplugin ..= " | delcommand VimwikiReference"
endif

let &cpo = s:save_cpo
unlet s:save_cpo
" vim:tabstop=4:shiftwidth=4:expandtab:textwidth=99:foldmethod=marker
