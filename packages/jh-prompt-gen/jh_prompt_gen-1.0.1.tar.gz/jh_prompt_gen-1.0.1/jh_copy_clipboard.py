#!/usr/bin/env python3
"""
jh-copy-clipboard.py

Copy file(s) or directory contents to clipboard or stdout with headers and indentation.
Supports ignore patterns via a .jhclipignore file or custom ignore file.
Default ignore patterns include common binary extensions (*.png, *.jpg, etc).

Examples:
  jh-copy-clipboard.py path/to/file
  jh-copy-clipboard.py path/to/dir -i '*.pyc' -i 'node_modules/'
  jh-copy-clipboard.py path/to/dir -I custom_ignore.txt --return
"""
import argparse
import os
import fnmatch
import pyperclip
from concurrent.futures import ThreadPoolExecutor
from typing import List

# Banner width for separators
BANNER_WIDTH = 80


def make_banner(text: str, width: int = BANNER_WIDTH, char: str = '-') -> str:
    """
    Center `text` in a line of repeated `char` of total length `width`.
    E.g., "---- filename.py ----".
    """
    label = f" {text} "
    pad = max(width - len(label), 0)
    left = pad // 2
    right = pad - left
    return f"{char * left}{label}{char * right}"


def should_exclude(rel_path: str, patterns: List[str]) -> bool:
    """
    Return True if `rel_path` matches any ignore pattern.
    Semantics mirror .gitignore:
      - Glob patterns via fnmatch on full path
      - Patterns without '/' match any path segment
      - Patterns ending with '/' match directories only
    """
    norm = rel_path.replace(os.sep, '/')
    parts = norm.split('/')
    for pat in patterns:
        if fnmatch.fnmatch(norm, pat):
            return True
        if '/' not in pat and pat in parts:
            return True
        if pat.endswith('/') and norm.startswith(pat.rstrip('/') + '/'):
            return True
    return False


def read_file_output(path: str, base: str, patterns: List[str]) -> List[str]:
    """
    Read file at `path`, add a banner and tab-indent each line.
    Skip if excluded by patterns.
    """
    out: List[str] = []
    rel = os.path.relpath(path, base)
    # Strip only leading "./", preserve leading dots
    rel_norm = rel[2:] if rel.startswith('./') else rel
    if should_exclude(rel_norm, patterns):
        return out
    out.append(make_banner(rel_norm) + "\n")
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                out.append('\t' + line.rstrip('\n') + '\n')
    except Exception as e:
        out.append(f"Error reading {path}: {e}\n")
    out.append("\n")
    return out


def process_dir(dir_path: str, base: str, patterns: List[str], out: List[str]) -> None:
    """
    Traverse directory, exclude matches, then read files in parallel and append in sorted order.
    """
    file_list: List[tuple[str, str]] = []
    for root, dirs, files in os.walk(dir_path):
        rel_root = os.path.relpath(root, base)
        rel_root_norm = rel_root[2:] if rel_root.startswith('./') else rel_root
        # Prune excluded dirs
        dirs[:] = [d for d in dirs if not should_exclude(f"{rel_root_norm}/{d}", patterns)]
        for name in sorted(files):
            tmp = f"{rel_root_norm}/{name}"
            rel_file = tmp[2:] if tmp.startswith('./') else tmp
            if not should_exclude(rel_file, patterns):
                file_list.append((rel_file, os.path.join(root, name)))
    # Read files concurrently
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(read_file_output, full, base, patterns): rel
                   for rel, full in file_list}
        # Append results in sorted order
        for rel, _ in sorted(file_list, key=lambda x: x[0]):
            for fut, r in list(futures.items()):
                if r == rel:
                    out.extend(fut.result())
                    del futures[fut]
                    break


def main() -> None:
    """
    Parse CLI args, collect files, then copy to clipboard or print to stdout.
    """
    parser = argparse.ArgumentParser(
        prog='jh-copy-clipboard',
        description='Copy file or directory contents with banners.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('path', help='Path to file or directory')
    parser.add_argument('-i', '--ignore', action='append', default=[],
                        help='Glob pattern to ignore (repeatable)')
    parser.add_argument('-I', '--ignore-file', dest='ignore_file',
                        help='Custom ignore file (overrides .jhclipignore)')
    parser.add_argument('--return', action='store_true', dest='return_text',
                        help='Print to stdout instead of copying')
    args = parser.parse_args()

    target = args.path
    base_dir = (os.path.dirname(os.path.abspath(target))
                if os.path.isfile(target) else os.path.abspath(target))

    # Default binary ignores
    raw_patterns = ['*.png', '*.jpg', '*.jpeg', '*.gif',
                    '*.bmp', '*.pdf', '*.zip', '*.tar', '*.gz']
    # CLI ignore patterns
    for pat in args.ignore:
        raw_patterns.extend(x.strip() for x in pat.split(',') if x.strip())
    # Load ignore-file patterns
    ignore_file = args.ignore_file or os.path.join(base_dir, '.jhclipignore')
    if os.path.isfile(ignore_file):
        with open(ignore_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    raw_patterns.append(line)

    output: List[str] = []
    if os.path.isfile(target):
        output = read_file_output(target, base_dir, raw_patterns)
    elif os.path.isdir(target):
        process_dir(target, base_dir, raw_patterns, output)
    else:
        parser.error(f"'{target}' is not a file or directory.")

    text = ''.join(output)
    if args.return_text:
        print(text)
    else:
        pyperclip.copy(text)


if __name__ == '__main__':
    main()
