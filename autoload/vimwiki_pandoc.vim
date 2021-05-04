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

function! vimwiki_pandoc#convert_week(bang, shiftheading, ...) abort "{{{
    if a:0 == 0
        let l:today_only = v:false
    else
        let l:today_only = v:true
    endif

    " Path for Vimwiki Diary buffer
    let l:diary_path = vimwiki#path#path_norm(
        \ vimwiki#path#join_path(
        \ vimwiki#vars#get_wikilocal('path'),
        \ vimwiki#vars#get_wikilocal('diary_rel_path')
        \ ))
    let l:current_path = vimwiki#path#path_norm(expand('%:p:h').'/')

    if ! vimwiki#path#is_equal(l:current_path, l:diary_path)
        echomsg 'Vimwiki Pandoc Error: You can only convert Vimwiki diary files.'
        return
    endif
    " Today is the basename for the Vimwiki Diary buffer.
    let l:today = expand('%:t:r')


    " Path for Vimwiki templates
    let l:datadir = s:get_pandoc_datadir('')

    " TODO: refactor into python3 file
    python3 << trim EOF
        import vim

        from pathlib import Path

        from vimwiki_docx.catvimwiki import del_empty_heading
        from vimwiki_docx.vimwiki_week import concatenate_diary

        end_date: str = vim.eval(r"l:today")

        today_only: bool = vim.eval(r"l:today_only")
        if today_only is False:
            start_date: str = None
        else:
            start_date = end_date

        diary: Path = concatenate_diary(
            start_date = start_date,
            end_date = end_date,
            diary_path = vim.eval(r"l:diary_path")
        )

        diary = del_empty_heading(diary)
    EOF


    " help taskwiki_disable
    let l:undo_taskwiki_disable = get(g:, 'taskwiki_disable', '')
    if empty('l:taskwiki_disable')
        let g:taskwiki_disable = 'disable'
    endif

    silent execute 'tabedit'  py3eval('str(diary)')
    silent VimwikiRenumberAllLists
    silent update

    " TODO: refactor to separate function.
    let l:input = expand('%')
    let l:output = expand('%:p:r').'.docx'

    let l:cmd = 'pandoc --from=vimwiki --to=docx'
                \ .' --shift-heading-level-by='.a:shiftheading
    if l:datadir !=? ''
        let l:cmd = l:cmd.' --data-dir='.shellescape(l:datadir)
    endif
    let l:cmd = l:cmd.' --output='.shellescape(l:output)

    if has('win32') || has('win64')
      silent execute '!start /b' l:cmd l:input
    else
      silent execute '!' l:cmd l:input
    endif

    " Copy path to MS Word file to clipboard.
    if has('win32') || has('win64')
        let @+ = l:output
    elseif executable('wslpath')
        let @+ = system('wslpath -w '..shellescape(l:output))
    endif

    " Open in MS Word.
    if a:bang
        silent tabclose
        if (has('win32') || has('win64'))
            silent execute '!start /b' shellescape(l:output)
        elseif executable('wslpath')
            silent execute system('wslview $(wslpath -w '..shellescape(l:output)..')')
        endif
    else
        edit
    endif

    if empty('l:taskwiki_disable')
        unlet g:taskwiki_disable
    endif
endfunction "}}}

let &cpo = s:save_cpo
unlet s:save_cpo
" vim:tabstop=4:shiftwidth=4:expandtab:textwidth=99:foldmethod=marker
