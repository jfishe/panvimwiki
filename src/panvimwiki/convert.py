"""Process filters and convert to output format using pandoc."""

import subprocess
from pathlib import Path
from typing import Tuple

import pypandoc

PREFILTER = (
    "delete_bullet_star",
    "delete_task_pending",
)
FILTER = (
    "delete_tag_lines",
    "delete_empty_heading",
    "delete_taskwiki_heading",
)
EXTRA_ARGS = (
    "--shift-heading-level-by",
    "1",
    "--data-dir",
    str(Path.home() / "vimwiki_html/templates"),
)


def convert(
    inputfile: str,
    outputfile: str,
    to: str = "markdown",
    prefilters: Tuple[str, ...] = PREFILTER,
    filters: Tuple[str, ...] = FILTER,
    extra_args: Tuple[str, ...] = EXTRA_ARGS,
) -> None:
    """Convert Vimwiki with pandoc after applying prefilters and pandoc filters.

    Parameters
    ----------
    inputfile
          Vimwiki file absolute path

    outputfile
          Converted file absolute path

    to
          Pandoc output format. See `pandoc --list-output-formats`

    prefilters
          Selected Vimwiki stdio executable filters.  See `pydoc
          panvimwiki.convert` for provided filters. Any executable that
          receives Vimwiki format as stdin and produces stdout should work.

    filters
          Selected pandoc filters.  See `pydoc panvimwiki.convert` for
          provided filters. Any valid `pandoc --filter <filter name>` should
          work.

    extra_args
        Additional pandoc arguments and parameters.  See `pydoc
        pypandoc.convert_text` for details and `pandoc --help` for valid
        content.

    """
    with open(inputfile, mode="r", encoding="utf8") as fin:
        source = fin.read()

    # Prefilter
    for cmd in prefilters:
        filter_out = subprocess.run(
            cmd,
            input=source,
            capture_output=True,
            text=True,
            check=True,
        )
        source = filter_out.stdout

    # Pandoc Filter
    if extra_args is None:
        extraargs = ()
    else:
        extraargs = extra_args

    pypandoc.convert_text(
        source=source,
        to=to,
        format="vimwiki",
        filters=filters,
        outputfile=outputfile,
        extra_args=extraargs,
    )
