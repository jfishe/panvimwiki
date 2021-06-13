"""Process filters."""

import subprocess
from typing import Tuple

import pypandoc

PREFILTER = (
    "delete_bullet_star.py",
    "delete_task_pending.py",
)
FILTER = (
    "delete_empty_heading.py",
    "delete_tag_lines.py",
    "delete_taskwiki_heading.py",
)


def convert(
    inputfile: str,
    outputfile: str,
    to: str = "markdown",
    prefilters: Tuple[str, ...] = PREFILTER,
    filters: Tuple[str, ...] = FILTER,
):
    """Convert Vimwiki with pandoc after applying prefilters and pandoc filters.

    Parameters
    ----------
    inputfile : Vimwiki file absolute path

    outputfile : Converted file absolute path

    to : Pandoc output format. See `pandoc --list-output-formats`

    prefilters : Selected Vimwiki stdio executable filters.
                 See `pydoc vimwiki_docx.convert`
                 for provided filters. Any executable that receives
                 Vimwiki format as stdin and produces stdout should work.

    filters : Selected pandoc filters.
              See `pydoc vimwiki_docx.convert`
              for provided filters. Any valid
              `pandoc --filter <filter name>` should work.

    Returns
    -------
    None

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
    pypandoc.convert_text(
        source=source,
        to=to,
        format="vimwiki",
        filters=filters,
        outputfile=outputfile,
    )
