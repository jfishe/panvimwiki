" Panvimwiki autoload
" File: panvimwiki.vim
" Description: Concatenate, filter and convert Vimwiki Diary using Pandoc
" Home: https://github.com/jfishe/panvimwiki
" Maintainer: John D. Fisher <jdfenw@gmail.com>
" Last Change: 2024-01-01

if exists('g:loaded_panvimwiki_auto') || !has('python3') || &compatible
            \ || !executable('pandoc') || !has('patch-8.2.0578h')
    finish
endif
let g:loaded_panvimwiki_auto = 1

let s:save_cpo = &cpo
set cpo&vim

" function! panvimwiki#expand_citeproc() abort
"     python3 from panvimwiki.wiki2pandoc import expand_citeproc
"     call ExpandCiteproc(expand('%f'))
" endfunction

function! panvimwiki#convert(bang, ...) abort "{{{
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
    if exists('g:panvimwiki_settings')
        let l:format = get(g:panvimwiki_settings, 'format', 'docx')
        let l:extra_args = get(g:panvimwiki_settings, 'extra_args', '0')
    else
        let l:format = 'docx'
        let l:extra_args = '0'
    endif

    let l:diary_path = vimwiki#path#path_norm(
                \ vimwiki#path#join_path(
                \ vimwiki#vars#get_wikilocal('path'),
                \ vimwiki#vars#get_wikilocal('diary_rel_path')
                \ ))
    let l:current_path = vimwiki#path#path_norm(expand('%:p:h')..'/')

    if a:0 > 0
        let l:is_concatenate = 1
        try
            if ! vimwiki#path#is_equal(l:current_path, l:diary_path)
                throw 'Vimwiki Pandoc Error: You can only concatenate Vimwiki Diary Notes.'
            endif
        endtry

        let l:is_diary = 1
    elseif vimwiki#path#is_equal(l:current_path, l:diary_path)
        let l:is_diary = 1
        let l:is_concatenate = 0
    else
        let l:is_diary = 0
        let l:is_concatenate = 0
    endif

    " Assume the basename for the Vimwiki Diary buffer is in ISO format.
    " " TODO:  <26-06-21, jdfenw@gmail.com> Generalize to other Vimwiki file
    " name conventions "
    let l:end_date = expand('%:t:r')

    python3 from panvimwiki.wiki2pandoc import wiki2pandoc

    " Vim_bridge embeds quotation marks in the string.
    let l:output = Wiki2pandoc(l:is_diary, l:is_concatenate, l:format, l:end_date, '', l:extra_args)[1:-2]

    " Copy path to MS Word file to clipboard.
    if has('clipboard')
        if has('win32') || has('win64')
            let @+ = l:output
        elseif executable('wslpath')
            let @+ = system('wslpath -w '..shellescape(l:output))
        endif
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
" vim:tabstop=2:shiftwidth=2:expandtab:textwidth=99:foldmethod=marker
