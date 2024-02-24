"""Vim interface to convert Vimwiki to another format using pandoc."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import vim  # noqa
from vim_bridge import bridged

from panvimwiki.convert import convert
from panvimwiki.vimwiki_week import concatenate_diary


@bridged
def vimwiki_task_link() -> None:
    r"""Convert pandoc tasks and wikilinks to Vimwiki markdown.

    Example
    -------
    Call pandoc to convert vimwiki-syntax-links to pandoc markdown. Remove
    pandoc link title, "wikilink", for compatibility with Vimiwki markdown
    syntax, equivalent to: ::

        $ pandoc --from=markdown+wikilinks_title_after_pipe-task_lists \
              --standalone \
              --wrap=none \
              --to=markdown | wikilink_markdown

    """
    path = Path(vim.eval("expand('%f')"))
    convert(
        inputfile=str(path),
        outputfile=str(path),
        format="markdown+wikilinks_title_after_pipe-task_lists",
        to="markdown-citations",
        prefilters=None,
        filters=None,
        extra_args=(
            "--citeproc",
            "--standalone",
            "--wrap",
            "none",
        ),
        postfilters=("wikilink_markdown",),
    )


@bridged
def expand_citeproc() -> None:
    """Resolve pandoc citeproc references to GFM div anchors.

    Preserve Vimwiki [[URL|Description]] style links with
    `gfm+wikilinks_title_after_pipe`.

    `wikilink_markdown` removes backslash-escapes from `task_lists` for
    compatibility with Vimwiki and Taskwiki `vimwiki-todo-lists`.

    """
    path = Path(vim.eval("expand('%f')"))
    convert(
        inputfile=str(path),
        outputfile=str(path),
        format="markdown+wikilinks_title_after_pipe-task_lists",
        to="gfm+wikilinks_title_after_pipe",
        prefilters=None,
        filters=None,
        extra_args=(
            "--citeproc",
            "--standalone",
            "--wrap",
            "none",
        ),
        postfilters=("wikilink_markdown",),
    )


@bridged
def wiki2pandoc(
    is_diary: str,
    is_concatenate: str,
    to: str = "docx",
    end_date: str | None = "",
    start_date: str | None = "",
    extra_args: Literal["0"] | list[str] = "0",
) -> str:
    """Bridged to Vim function Wiki2pandoc.

    Concatenate Diary Notes and/or convert Vimwiki Notes to selected format.

    Parameters
    __________
    is_diary
        String containing a 0, False, or 1, True, whether current buffer is a
        Vimwiki DiaryNote.

    is_concatenate
        String containing a 0, False, or 1, True, whether multiple Vimwiki
        DiaryNotes from start_date to end_date should concatenate before
        conversion. Otherwise convert the current buffer only and ignore the
        dates.

    to
        Output format (defaults to docx)

    end_date
        Depending on is_concatenate, the end date for concatenating Vimwiki
        DiaryNotes. Coerce an empty string to None.

    start_date
        Depending on is_concatenate, the start date for concatenating Vimwiki
        DiaryNotes. Coerce an empty string to None.

    extra_args : list or str
        "0" or a list of valid pandoc arguments, e.g.,

        .. code:: python

           ["--shift-heading-level-by", "1", "--data-dir", "vimwiki_html/templates"]

        Coerce "0" to an empty list.
        See `pydoc pypandoc.convert_text` for details and `pandoc --help` for
        valid content.

    Returns
    -------
    str
        Absolute path to converted Vimwiki file

    """
    isdiary: bool = bool(int(is_diary))
    isconcatenate: bool = bool(int(is_concatenate))
    if extra_args == "0":
        extra_args = []

    if isdiary and isconcatenate:
        if end_date == "":
            end_date = None
        if start_date == "":
            start_date = None
        diary_path = vim.eval(
            r"vimwiki#path#path_norm("
            r"vimwiki#path#join_path("
            r"vimwiki#vars#get_wikilocal('path'),"
            r"vimwiki#vars#get_wikilocal('diary_rel_path')"
            r"))"
        )
        inputfile: Path = concatenate_diary(
            start_date=start_date,
            end_date=end_date,
            diary_path=diary_path,
        )
        outputfile: Path = inputfile.with_suffix("." + to)
    else:
        inputfile = Path(vim.eval(r"expand('%:p')"))
        wiki_path = Path(
            vim.eval(r"vimwiki#path#path_norm(vimwiki#vars#get_wikilocal('path'))")
        )

        path_html = Path(
            vim.eval(r"vimwiki#path#path_norm(vimwiki#vars#get_wikilocal('path_html'))")
        )
        outputfile = inputfile.with_suffix("." + to)
        outputfile = path_html.parent / Path(to) / outputfile.relative_to(wiki_path)
        outputfile.parent.mkdir(parents=True, exist_ok=True)

    convert(
        inputfile=str(inputfile),
        outputfile=str(outputfile),
        to=to,
        extra_args=tuple(extra_args),
    )

    return str(outputfile)
