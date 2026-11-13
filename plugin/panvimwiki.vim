" Panvimwiki plugin
" File: panvimwiki.vim
" Description: Convert Vimwiki to other formats using pandoc
" Home: https://github.com/jfishe/panvimwiki
" Maintainer: John D. Fisher <jdfenw@gmail.com>
" Last Change: 2026-11-13

" Should we load? {{{1
if exists('g:panvimwiki_loaded') || !has('python3') || &compatible
    finish
endif
let g:panvimwiki_loaded = 1
" }}}1

" Save current &cpo and reset to Vim default compatibility options.
let s:save_cpo = &cpoptions
set cpoptions&vim

let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

" Add g:panvimwiki_python_path to Vim's Python sys.path. {{{1
" A String or List of directories, e.g., a virtual environment's
" site-packages. Each entry is expanded with glob(), so `~` and wildcards
" such as `python3.*` work. site.addsitedir() also processes .pth files.
function! s:AddPythonPath() abort
  let l:paths = get(g:, 'panvimwiki_python_path', [])
  if type(l:paths) != v:t_list
    let l:paths = [l:paths]
  endif
  let l:dirs = []
  for l:path in l:paths
    let l:dirs += glob(l:path, 1, 1)
  endfor
  if empty(l:dirs)
    return
  endif
  call py3eval('[__import__("site").addsitedir(d) for d in vim.eval("l:dirs")]')
endfunction
call s:AddPythonPath()
" }}}1

" Restore Vim compatibility options.
let &cpoptions = s:save_cpo
unlet s:save_cpo
" vim:tabstop=2:shiftwidth=2:expandtab:textwidth=99:foldmethod=marker
