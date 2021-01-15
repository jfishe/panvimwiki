" vim: set fdm=marker et ts=4 sw=4 sts=4:

function! vimwiki_pandoc#convert_week() abort
    let l:today = expand('%:t:r')

    python3 << EOF
import datetime
import vim
from vimwiki_docx.catvimwiki import get_last_monday, catdiary, del_empty_heading

enddate = datetime.date.fromisoformat( vim.eval('l:today') )
startdate = get_last_monday(enddate)
diary = catdiary(startdate, enddate)
convert_week = del_empty_heading(diary)
EOF

    execute 'edit ' . py3eval('str(convert_week)')
    VimwikiRenumberAllLists
    update
endfunction

function! vimwiki_pandoc#convert_from_to(startdate, enddate) abort
    " python3 'from vimwiki_docx.vimwiki_week import convert_last_week'
    python3 from vimwiki_docx.vimwiki_week import convert_from_to
    return py3eval('str(convert_from_to("' . a:startdate . '","' . a:enddate . '"))')
endfunction
