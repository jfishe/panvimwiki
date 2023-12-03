"""Process filters and convert to output format using pandoc."""

import subprocess
from pathlib import Path

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
    outputfile: str | None,
    format: str = "vimwiki",
    to: str = "markdown",
    prefilters: tuple[str, ...] | None = PREFILTER,
    filters: tuple[str, ...] | None = FILTER,
    extra_args: tuple[str, ...] = EXTRA_ARGS,
) -> str | None:
    """Convert Vimwiki with pandoc after applying prefilters and pandoc filters.

    Parameters
    ----------
    inputfile
          Vimwiki file absolute path

    outputfile
          Converted file absolute path or None to return a string.

    format
          Pandoc input format. See `pandoc --list-input-formats`

    to
          Pandoc output format. See `pandoc --list-output-formats`

    prefilters
          Selected Vimwiki stdio executable filters.  See `pydoc
          panvimwiki.convert` for provided filters. Any executable that
          receives Vimwiki format as stdin and produces stdout should work.
          An empty tuple will skip prefilters.

    filters
          Selected pandoc filters.  See `pydoc panvimwiki.convert` for
          provided filters. Any valid `pandoc --filter <filter name>` should
          work.

    extra_args
        Additional pandoc arguments and parameters.  See `pydoc
        pypandoc.convert_text` for details and `pandoc --help` for valid
        content.

    Returns
    -------
    str or None
        Converted string, if outputfile is None, or None.
    """
    with open(inputfile, encoding="utf8") as fin:
        source = fin.read()

    # Prefilter
    if prefilters is not None:
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

    return pypandoc.convert_text(
        source=source,
        to=to,
        format=format,
        filters=filters,
        outputfile=outputfile,
        extra_args=extraargs,
    )
