"""Pandoc filters and Vim plugin VimwikiConvert from Vimwiki to Docx.

Panvimwiki provides tools for conversion to Microsoft Word docx or other
output formats supported by
`Pandoc a universal document converter <https://pandoc.org/>`_.
Panvimwiki provides command line tools as well as Vim commands to
concatenate and convert Diary Notes or convert any Vimwiki note.
"""

from importlib.metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
