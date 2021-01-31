" Vimwiki_Pandoc ftplugin
" File: vimwiki.vim
" Description: Vimwiki_Pandoc additions to filetype vimwiki
" Maintainer: John D. Fisher
" Last Change: 2021-01-29

if exists('b:did_ftplugin_vimwiki_pandoc')
  finish
endif
let b:did_ftplugin_vimwiki_pandoc = 1  " Don't load another plugin for this buffer

let s:save_cpo = &cpo
set cpo&vim

if !exists(":VimwikiConvertWeek")
  command -buffer -bang -nargs=0 VimwikiConvertWeek
        \ call vimwiki_pandoc#convert_week(<bang>0, 1)
endif
if !exists(":VimwikiConvertToday")
  command -buffer -bang -nargs=0 VimwikiConvertToday
        \ call vimwiki_pandoc#convert_week(<bang>0, 1, 1)
endif

let b:undo_ftplugin = get(b:, 'undo_ftplugin', '')
if !empty('b:undo_ftplugin')
  let b:undo_ftplugin ..= " | "
endif
let b:undo_ftplugin ..= "delcommand VimwikiConvertWeek"
      \ .. " | delcommand VimwikiConvertToday"
      \ .. " | unlet b:did_ftplugin_vimwiki_pandoc"

let &cpo = s:save_cpo
unlet s:save_cpo
" vim:tabstop=4:shiftwidth=4:expandtab:textwidth=99:foldmethod=marker
