" Panvimwiki ftplugin
" File: vimwiki.vim
" Description: Panvimwiki additions to filetype vimwiki
" Home: https://github.com/jfishe/panvimwiki
" Maintainer: John D. Fisher <jdfenw@gmail.com>
" Last Change: 2024-01-01

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

if vimwiki#vars#get_wikilocal('syntax') ==# 'markdown'
  if !exists(":VimwikiReference")
    python3 from panvimwiki.wiki2pandoc import expand_citeproc
    command -buffer -nargs=0 VimwikiReference
          \ call ExpandCiteproc()
    let b:undo_ftplugin ..= " | delcommand VimwikiReference"
  endif
  if !exists(":VimwikiMarkdownFormat")
    python3 from panvimwiki.wiki2pandoc import vimwiki_task_link
    command -buffer -nargs=0 VimwikiMarkdownFormat
          \ call VimwikiTaskLink()
    let b:undo_ftplugin ..= " | delcommand VimwikiMarkdownFormat"
  endif
endif

let &cpo = s:save_cpo
unlet s:save_cpo
" vim:tabstop=2:shiftwidth=2:expandtab:textwidth=99:foldmethod=marker
