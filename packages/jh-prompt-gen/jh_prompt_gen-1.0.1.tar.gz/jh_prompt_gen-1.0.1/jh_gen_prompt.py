#!/usr/bin/env python3
"""
jh-gen-prompt.py

Collect code via copy-jh-clipboard.py and build a ChatGPT prompt from a template.
Templates are defined in .jhpromptconfig under `default_prompt_pattern` or named patterns.

Examples:
  jh-gen-prompt path/to/dir "Implement feature X"
  jh-gen-prompt.py path/to/file "Add logging" -i '*.pyc' -I ignore.txt -p pattern_1

Placeholders available by default:
  {code}     - the captured code
  {feature}  - the feature description positional arg
Additional placeholders from .jhpromptconfig; override via -f. Use --pattern to select.
"""
import argparse
import os
import subprocess
import sys
from typing import Dict, Any

import pyperclip


def read_prompt_config(path: str) -> Dict[str, Any]:
    """
    Parse .jhpromptconfig into a dict of keys to values.

    Supported formats:
      KEY=value                -> single-line values
      KEY=\"""...\""" or '''...''' -> multi-line values
    Blank lines and lines starting with '#' are ignored.

    Returns:
      dict where each key maps to its string value.
    """
    cfg: Dict[str, Any] = {}
    if not os.path.isfile(path):
        return cfg
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip('\n')
        if not line.strip() or line.lstrip().startswith('#'):
            i += 1
            continue
        if '=' in line:
            key, rest = line.split('=', 1)
            key = key.strip()
            val = rest.lstrip()
            # multi-line with triple quotes
            if val.startswith("'''") or val.startswith('"""'):
                quote = val[:3]
                buf: list[str] = []
                txt = val[3:]
                if txt.endswith(quote) and len(txt) > len(quote):
                    buf.append(txt[:-3])
                else:
                    if txt:
                        buf.append(txt)
                    i += 1
                    while i < len(lines):
                        part = lines[i].rstrip('\n')
                        if part.endswith(quote):
                            buf.append(part[:-3])
                            break
                        buf.append(part)
                        i += 1
                cfg[key] = '\n'.join(buf)
            else:
                cfg[key] = val.strip().strip('"').strip("'")
        i += 1
    return cfg


def main() -> None:
    """
    Build and copy a formatted prompt.

    Usage:
      gen-jh-prompt.py <path> <feature> [-i PATTERN]... [-I IGNORE_FILE] [-c CONFIG_FILE] [-f KEY=VAL]... [--pattern NAME]
    """
    parser = argparse.ArgumentParser(
        prog='jh-gen-prompt',
        description='Easily generate great LLM prompts including code and a named template.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('path', help='File or directory for code capture')
    parser.add_argument('feature', help='New feature description')
    parser.add_argument('-i', '--ignore', action='append', default=[],
                        help='Glob ignore pattern for code capture')
    parser.add_argument('-I', '--ignore-file', dest='ignore_file',
                        help='Custom ignore file for code capture')
    parser.add_argument('-c', '--config-file', dest='config_file',
                        help='Path to .jhpromptconfig (overrides default)')
    parser.add_argument('-f', '--filler', action='append', default=[],
                        help='Additional placeholder=value overrides')
    parser.add_argument('-p', '--pattern', dest='pattern_name',
                        help='Select named pattern from config (e.g. pattern_1)')
    args = parser.parse_args()

    base = args.path if os.path.isdir(args.path) else os.path.dirname(args.path)
    cfg_path = args.config_file or os.path.join(base, '.jhpromptconfig')
    cfg = read_prompt_config(cfg_path)

    # Determine template: named -> default_prompt_pattern -> fallback
    if args.pattern_name:
        if args.pattern_name not in cfg:
            print(f"Pattern '{args.pattern_name}' not found in config.", file=sys.stderr)
            sys.exit(1)
        pattern = cfg[args.pattern_name]
    else:
        pattern = cfg.get('default_prompt_pattern')
    default = "{code}\n---\nNew Feature: {feature}"
    pattern = pattern or default

    # Capture code
    cmd = ['jh-copy-clipboard', '--return', args.path]
    if args.ignore_file:
        cmd += ['-I', args.ignore_file]
    for pat in args.ignore:
        cmd += ['-i', pat]

    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running jh-copy-clipboard: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    code = proc.stdout

    # Build context
    context: Dict[str, Any] = {**cfg, 'code': code, 'feature': args.feature}
    for f in args.filler:
        if '=' in f:
            k, v = f.split('=', 1)
            context[k] = v

    # Render and copy
    try:
        prompt = pattern.format(**context)
        pyperclip.copy(prompt)
        print("Prompt copied to clipboard.")
    except KeyError as e:
        print(f"Missing placeholder: {e.args[0]}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
