" Vimwiki_Pandoc autoload
" Description: Concatenate, filter and convert Vimwiki Diary using Pandoc
" Home: https://github.com/jfishe/vimwiki_docx
" Maintainer: John D. Fisher <jdfenw@gmail.com>
" Last Change: 2021-01-29

if exists('g:loaded_vimwiki_pandoc_auto') || !has('python3') || &compatible
            \ || !executable('pandoc')
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

    let fname = expand(vimwiki#vars#get_wikilocal('template_path').name)

    if filereadable(fname)
        return fnamemodify(fname, ':p:h')
    else
        return ''
    endif
endfunction "}}}

function! s:diary_path(...) abort "{{{
    " https://github.com/vimwiki/vimwiki/blob/619f04f89861c58e5a6415a4f83847752928252d/autoload/vimwiki/diary.vim#L21
    let idx = a:0 == 0 ? vimwiki#vars#get_bufferlocal('wiki_nr') : a:1
    return vimwiki#vars#get_wikilocal('path', idx).vimwiki#vars#get_wikilocal('diary_rel_path', idx)
endfunction "}}}

function! vimwiki_pandoc#convert_week(bang, shiftheading, ...) abort "{{{
    if a:0 == 0
        let l:today_only = v:false
    else
        let l:today_only = v:true
    endif

    " Path for Vimwiki Diary buffer
    let l:diary_path = vimwiki#path#path_norm(s:diary_path())

    let l:current_path = vimwiki#path#path_norm(expand('%:p:h').'/')

    if ! vimwiki#path#is_equal(l:current_path, l:diary_path)
        echomsg 'Vimwiki Pandoc Error: You can only convert Vimwiki diary files.'
        return
    endif
    " Today is the basename for the Vimwiki Diary buffer.
    let l:today = expand('%:t:r')


    " Path for Vimwiki templates
    let l:datadir = fnameescape(s:get_pandoc_datadir(''))

    " TODO: refactor into python3 file
    python3 << trim EOF
        import vim
        import datetime

        from pathlib import Path

        from vimwiki_docx.catvimwiki import (
            catdiary,
            get_last_monday,
            del_empty_heading,
        )

        start_date: str = vim.eval(r"l:today")

        today_only: bool = vim.eval(r"l:today_only")
        if today_only is False:
            enddate: datetime.date = datetime.date.fromisoformat(start_date)
            startdate: datetime.date = get_last_monday(enddate)
        else:
            startdate = datetime.date.fromisoformat(start_date)
            enddate = startdate

        diary: Path = catdiary(
            startdate=startdate, enddate=enddate, wikidiary=Path(vim.eval(r"l:diary_path"))
        )

        diary = del_empty_heading(diary)
    EOF

    execute 'tabedit'  py3eval('str(diary)')
    VimwikiRenumberAllLists
    update

    " TODO: refactor to separate function.
    let l:input = fnameescape(expand('%'))
    let l:output = fnameescape(expand('%:p:r').'.docx')

    let l:cmd = 'pandoc --from=vimwiki --to=docx'
                \ .' --shift-heading-level-by='.a:shiftheading
    if l:datadir !=? ''
        let l:cmd = l:cmd.' --data-dir='.l:datadir
    endif
    let l:cmd = l:cmd.' --output='.l:output

    silent execute '!start /b' l:cmd l:input

    " Copy path to MS Word file to clipboard.
    let @+ = l:output

    " Open in MS Word.
    if a:bang
        tabclose
        silent execute '!start /b' l:output
    else
        edit
    endif
endfunction "}}}

let &cpo = s:save_cpo
unlet s:save_cpo
" vim:tabstop=4:shiftwidth=4:expandtab:textwidth=99:foldmethod=marker
