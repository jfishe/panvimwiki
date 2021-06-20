"""Vim interface to convert Vimwiki to another format using pandoc."""

try:
    import vim
except ModuleNotFoundError:
    pass

from pathlib import Path

from vimwiki_docx.vimwiki_week import concatenate_diary
from vimwiki_docx.convert import convert


def wiki2pandoc() -> str:
    """Concatenate Diary Notes and/or convert Vimwiki Notes to selected format.

    Returns
    -------
    Absolute path to converted Vimwiki file

    """
    isdiary: bool = vim.eval(r"l:isdiary")
    today_only: bool = vim.eval(r"l:today_only")
    to: str = vim.eval(r"l:format")

    if isdiary and today_only is False:
        end_date: str = vim.eval(r"l:today")
        start_date = None

        inputfile: Path = concatenate_diary(
            start_date=start_date,
            end_date=end_date,
            diary_path=vim.eval(r"l:diary_path"),
        )
    else:
        inputfile = Path(vim.eval(r"expand('%:p')"))

    outputfile: Path = inputfile.with_suffix(("." + to))

    extra_args = [
        "--shift-heading-level-by",
        vim.eval(r"a:shiftheading"),
    ]
    datadir: str = vim.eval(r"l:datadir")
    if datadir != "":
        extra_args.extend(
            [
                "--data-dir",
                datadir,
            ]
        )

    convert(
        inputfile=str(inputfile),
        outputfile=str(outputfile),
        to=to,
        extra_args=extra_args,
    )

    return str(outputfile)
