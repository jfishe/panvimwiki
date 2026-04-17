"""Process filters and convert to output format using pandoc."""

from __future__ import annotations

import os
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
    postfilters: tuple[str, ...] | None = None,
    extra_args: tuple[str, ...] | None = EXTRA_ARGS,
) -> str | None:
    """Convert Vimwiki with pandoc, applying selected filters.

    :py:mod:`panvimwiki.filter` lists provided pre-, post- and pandoc-filters.

    Parameters
    ----------
    inputfile
          Vimwiki file absolute path

    outputfile
          Converted file absolute path or None to return a string.

    format
          Pandoc input format. See ``pandoc --list-input-formats``

    to
          Pandoc output format. See ``pandoc --list-output-formats``

    prefilters
          Selected Vimwiki stdio executable filters. Any executable that
          receives input ``format`` as stdin and produces stdout should work.
          `None` skips prefilters.

    filters
          Selected pandoc filters.  Any valid ``pandoc --filter <filter name>``
          should work. None skips filters but still runs pandoc.

    postfilters
          Selected Vimwiki stdio executable filters. Any executable that
          receives pandoc ``to`` format as stdin and produces stdout should
          work. None skips postfilters.

    extra_args
          Additional pandoc arguments and parameters to pass to
          :py:func:`pypandoc.convert_text`. Refer to ``pandoc --help``
          for valid content.

    Raises
    ------
    RuntimeError
          Output to docx only works by using a outputfile. Pandoc requires an
          outputfile for binary document formats.

    Returns
    -------
    str or None
          Converted string, if outputfile is None, or None.
    """
    with open(inputfile, encoding="utf8") as fin:
        source = fin.read()

    # Ensure Python-based filter executables use UTF-8
    # for stdio on Windows (and elsewhere).
    # This prevents UnicodeEncodeError/DecodeError
    # when piping text through subprocesses.
    utf8_env = os.environ.copy()
    utf8_env.setdefault("PYTHONIOENCODING", "utf-8")
    utf8_env.setdefault("PYTHONUTF8", "1")

    # Prefilter
    if prefilters is not None:
        for cmd in prefilters:
            filter_out = subprocess.run(
                cmd,
                input=source,
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
                errors="strict",
                env=utf8_env,
            )
            source = filter_out.stdout

    # Pandoc Filter
    pandoc_args = extra_args or ()

    try:
        source = pypandoc.convert_text(
            source=source,
            to=to,
            format=format,
            filters=filters,
            outputfile=None,
            extra_args=pandoc_args,
        )
    except RuntimeError:
        return pypandoc.convert_text(
            source=source,
            to=to,
            format=format,
            filters=filters,
            outputfile=outputfile,
            extra_args=pandoc_args,
        )

    # Postfilter
    if postfilters is not None:
        for cmd in postfilters:
            filter_out = subprocess.run(
                cmd,
                input=source,
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
                errors="strict",
                env=utf8_env,
            )
            source = filter_out.stdout

    if outputfile is None:
        return source
    else:
        with open(
            outputfile,
            mode="w",
            encoding="utf-8",
        ) as f:
            f.write(source)
        return None
