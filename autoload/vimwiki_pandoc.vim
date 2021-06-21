" Vimwiki_Pandoc autoload
" Description: Concatenate, filter and convert Vimwiki Diary using Pandoc
" Home: https://github.com/jfishe/vimwiki_docx
" Maintainer: John D. Fisher <jdfenw@gmail.com>
" Last Change: 2021-01-29

if exists('g:loaded_vimwiki_pandoc_auto') || !has('python3') || &compatible
            \ || !executable('pandoc') || !has('patch-8.2.0578h')
    finish
endif
let g:loaded_vimwiki_pandoc_auto = 1

let s:save_cpo = &cpo
set cpo&vim

function! s:get_pandoc_datadir(name) abort "{{{
    if a:name ==? ''
        let name = 'reference.docx'
    else
        let name = a:name
    endif

    let fname = vimwiki#path#path_norm(
        \ vimwiki#path#join_path(
        \ vimwiki#vars#get_wikilocal('template_path'), name
        \ ))

    if filereadable(fname)
        return fnamemodify(fname, ':p:h')
    else
        return ''
    endif
endfunction "}}}

function! vimwiki_pandoc#convert(bang, shiftheading, ...) abort "{{{
    " Convert the current Vimwiki buffer to docx and copy path to "+ register.
    "
    " By default, convert current buffer only.
    "
    " If passed extra arguments (a:0 > 0), assume Diary Note and combine
    " all diary notes from the preceding Monday through the current buffer.
    "
    " bang : Open converted docx file in default program, e.g., MS Word.
    "
    " shiftheading : Pass value to pandoc, as in:
    "   `pandoc -shift-heading-level-by=<shiftheading>`
    " Path for Vimwiki Diary buffer
    let l:diary_path = vimwiki#path#path_norm(
        \ vimwiki#path#join_path(
        \ vimwiki#vars#get_wikilocal('path'),
        \ vimwiki#vars#get_wikilocal('diary_rel_path')
        \ ))
    let l:current_path = vimwiki#path#path_norm(expand('%:p:h')..'/')

    let l:format = 'docx'

    if a:0 > 0
        let l:today_only = v:false
        if ! vimwiki#path#is_equal(l:current_path, l:diary_path)
            echomsg 'Vimwiki Pandoc Error: You can only concatenate Vimwiki Diary Notes.'
            return
        endif
        let l:isdiary = v:true
    elseif vimwiki#path#is_equal(l:current_path, l:diary_path)
        let l:isdiary = v:true
        let l:today_only = v:true
    else
        let l:isdiary = v:false
        let l:today_only = v:true
    endif

    " Today is the basename for the Vimwiki Diary buffer.
    let l:today = expand('%:t:r')

    " Path for Vimwiki templates
    let l:datadir = s:get_pandoc_datadir('')

    python3 << trim EOF
        from vimwiki_docx.wiki2pandoc import wiki2pandoc

        outputfile = wiki2pandoc()
    EOF
    let l:output = py3eval('outputfile')

    " Copy path to MS Word file to clipboard.
    if has('win32') || has('win64')
        let @+ = l:output
    elseif executable('wslpath')
        let @+ = system('wslpath -w '..shellescape(l:output))
    endif

    " Open in MS Word.
    if a:bang
        if (has('win32') || has('win64'))
            silent execute '!start /b' shellescape(l:output)
        elseif executable('wslpath')
            silent execute system('wslview "$(wslpath -w '..shellescape(l:output)..')"')
        endif
    endif
endfunction "}}}

let &cpo = s:save_cpo
unlet s:save_cpo
" vim:tabstop=4:shiftwidth=4:expandtab:textwidth=99:foldmethod=marker
