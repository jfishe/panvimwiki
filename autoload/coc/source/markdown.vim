" Vim source for markdown yaml header

function! coc#source#markdown#init() abort
  return {
        \ 'shortcut': 'Zettelkasten',
        \ 'priority': 9,
        \ 'filetypes': ['markdown', 'pandoc', 'vimwiki'],
        \ 'triggerCharacters': ['type:', 'status:']
        \}
endfunction

function! coc#source#markdown#complete(option, cb) abort
  let yaml = {
        \ 'type:': ['literature', 'reference', 'index', 'note'],
        \ 'status:': ['Create', 'Process', 'Reviewed']
        \ }
  let items = map(yaml[a:option['line']], '" " .. v:val')
  call a:cb(items)
endfunction
