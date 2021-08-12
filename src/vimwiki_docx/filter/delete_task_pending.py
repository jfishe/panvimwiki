#!/usr/bin/env python3
r"""Remove Pending and Waiting tasks and set Start tasks to [.]{.done1}.

Plain text filter

- Read stdin.
- Remove Pending [ ] and Waiting [W] tasks.
- Change Start [S] task to [.].
- Write filtered result to stdout.

Example
_______
bash> echo '1. [ ] Numbered list done0 item 0 should NOT appear\n' \

bash> '2. [.] Numbered list done1 item 1 should appear' |

bash> delete_task_pending

2. [.] Numbered list done1 item 1 should appear

"""

from vimwiki_docx.filter.prefilter import prefilter

DELETE = r"\s\[[\sW]\]"
REPLACE = (r"\s\[S\]", " [.]")


def main():
    """Filter stdio with action()."""
    prefilter(delete=DELETE, replace=REPLACE)


if __name__ == "__main__":
    main()
