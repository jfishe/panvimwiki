" Panvimwiki ftplugin
" File: vimwiki.vim
" Description: Panvimwiki additions to filetype vimwiki
" Maintainer: John D. Fisher
" Last Change: 2021-01-29

if exists('b:did_ftplugin_panvimwiki') || &compatible
            \ || !executable('pandoc') || !has('patch-8.2.0578h')
  finish
endif
let b:did_ftplugin_panvimwiki = 1  " Don't load another plugin for this buffer

let s:save_cpo = &cpo
set cpo&vim

if !exists(":VimwikiConvert")
  command -buffer -bang -nargs=0 VimwikiConvert
        \ call panvimwiki#convert(<bang>0)
endif
if !exists(":VimwikiConvertWeek")
  command -buffer -bang -nargs=0 VimwikiConvertWeek
        \ call panvimwiki#convert(<bang>0, 1)
endif

let b:undo_ftplugin = get(b:, 'undo_ftplugin', '')
if !empty('b:undo_ftplugin')
  let b:undo_ftplugin ..= " | "
endif
let b:undo_ftplugin ..= "delcommand VimwikiConvertWeek"
      \ .. " | delcommand VimwikiConvert"
      \ .. " | unlet b:did_ftplugin_panvimwiki"

let &cpo = s:save_cpo
unlet s:save_cpo
" vim:tabstop=4:shiftwidth=4:expandtab:textwidth=99:foldmethod=marker
