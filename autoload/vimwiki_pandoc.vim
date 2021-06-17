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
    if a:0 > 0
        let l:today_only = v:false
        " Path for Vimwiki Diary buffer
        let l:diary_path = vimwiki#path#path_norm(
            \ vimwiki#path#join_path(
            \ vimwiki#vars#get_wikilocal('path'),
            \ vimwiki#vars#get_wikilocal('diary_rel_path')
            \ ))
        let l:current_path = vimwiki#path#path_norm(expand('%:p:h').'/')

        if ! vimwiki#path#is_equal(l:current_path, l:diary_path)
            echomsg 'Vimwiki Pandoc Error: You can only concatenate Vimwiki Diary Notes.'
            return
        endif
    else
        let l:today_only = v:true
    endif

    " Today is the basename for the Vimwiki Diary buffer.
    let l:today = expand('%:t:r')

    " Path for Vimwiki templates
    let l:datadir = s:get_pandoc_datadir('')

    " TODO: refactor into python3 file
    python3 << trim EOF
        import vim

        from pathlib import Path

        from vimwiki_docx.vimwiki_week import concatenate_diary
        from vimwiki_docx.convert import convert

        today_only: bool = vim.eval(r"l:today_only")

        if today_only is False:
            end_date: str = vim.eval(r"l:today")
            start_date: str = None
" TODO:  <15-06-21, yourname> "
            inputfile: Path = concatenate_diary(
                start_date = start_date,
                end_date = end_date,
                diary_path = vim.eval(r"l:diary_path")
            )

        to: str = "docx"
        outputfile: Path = inputfile.with_suffix(("." + to))

        extra_args = [
            "--shift-heading-level-by",
            vim.eval(r"a:shiftheading"),
        ]
        datadir = vim.eval(r"l:datadir")
        if datadir != "":
            extra_args.extend(["--data-dir", datadir,])

        convert(
            inputfile=str(inputfile),
            outputfile=str(outputfile),
            to=to,
            extra_args=extra_args,
        )
    EOF


    " Copy path to MS Word file to clipboard.
    let l:output = py3eval('str(outputfile)')

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
            silent execute system('wslview $(wslpath -w '..shellescape(l:output)..')')
        endif
    endif
endfunction "}}}

let &cpo = s:save_cpo
unlet s:save_cpo
" vim:tabstop=4:shiftwidth=4:expandtab:textwidth=99:foldmethod=marker
