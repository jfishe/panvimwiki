" Test stub for dist#vim9#Open(), used by tests/vim/VimwikiConvert.vader's
" "VimwikiConvert bang" case so it doesn't launch a real external program.
" Loaded via autoload by prepending tests/vim/autoload_stubs to
" 'runtimepath', ahead of the real $VIMRUNTIME/autoload/dist/vim9.vim.
function! dist#vim9#Open(path) abort
  let g:panvimwiki_test_open_path = a:path
endfunction
