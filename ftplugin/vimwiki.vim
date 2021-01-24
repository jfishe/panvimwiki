" vim: set fdm=marker et ts=4 sw=4 sts=4:

" File: vimwiki.vim
" Description: Vimwiki_Pandoc additions to filetype vimwiki
" Author: John D. Fisher

if exists('b:did_ftplugin_vimwiki_pandoc')
  finish
endif
let b:did_ftplugin_vimwiki_pandoc = 1  " Don't load another plugin for this buffer

command! -buffer -bang -nargs=0 VimwikiConvertWeek call vimwiki_pandoc#convert_week(<bang>0, 1)
command! -buffer -bang -nargs=0 VimwikiConvertToday call vimwiki_pandoc#convert_week(<bang>0, 1, 1)
