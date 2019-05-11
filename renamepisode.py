#!/bin/env python

"""
Simple script for renaming TV show files into a standard format.

Here, we use Kodi's suggestion for describing the season and episode.
For example, for season 2, episode 7, the video file should contain "S02E07".

This script is currently able to match and fix the following formats:
   * 207
   * 0207
   * 2.07
   * 02.07
   * s02e07
   * s2e7

Please be careful when passing movie files, as the year may be incorrectly
interpreted. "Movie.2010.DVDRip.avi" could become "Movie.S20E10.DVDRip.avi".

Optional arguments:

:arg 0: path where the script should run (defaults to current dir)
:arg 1: -p|--preview - does not rename, just prints the expected outcome
:arg 2: -f|--force - does not ask for confirmation (potentially destructive)
:arg 3: -t|--title - capitalize the first letter of each segment
:arg 4: -l|--lower|--lowercase - uncapitalize whole filename
:arg 5: -u|--upper|--uppercase - capitalize whole filename
"""

import argparse
import os
import re
import sys
from itertools import combinations

OPTIONS = (
    {
        'key': ['path'],
        'kwargs': {
            'action': 'store',
            'nargs': '?',
            'default': '.',
            'help': 'path where the script should look for files',
        }
    },
    {
        'key': ['-p', '--preview'],
        'kwargs': {
            'action': 'store_true',
            'help': 'do not rename, just print the expected outcome',
        }
    },
    {
        'key': ['-f', '--force'],
        'kwargs': {
            'action': 'store_true',
            'help': 'do not ask for confirmation (potentially destructive)',
        }
    },
    {
        'key': ['-t', '--title'],
        'kwargs': {
            'action': 'store_true',
            'help': 'capitalize the first letter of each segment',
        }
    },
    {
        'key': ['-l', '--lower', '--lowercase'],
        'kwargs': {
            'action': 'store_true',
            'help': 'uncapitalize whole filename',
        }
    },
    {
        'key': ['-u', '--upper', '--uppercase'],
        'kwargs': {
            'action': 'store_true',
            'help': 'capitalize whole filename',
        }
    },
)

ANSWERS = {
    'y': True,
    'yes': True,
    'n': False,
    'no': False,
}

EXTENSIONS = (
    # Video
    'mp4', 'm4a', 'm4v', 'f4v', 'f4a', 'm4b', 'm4r', 'f4b', 'mov', '3gp',
    '3gp2', '3g2', '3gpp', '3gpp2', 'ogg', 'ogv', 'ogx', 'wmv', 'wma', 'asf',
    'webm', 'flv', 'avi', 'vob', 'qt', 'rm', 'rmvb', 'amv', 'nsv', 'mkv',
    # Subtitles
    'srt', 'sub', 'sbv',
)


def validate_options():
    """Parse arguments and check for inconsistencies."""
    mutexes = (
        ('force', 'preview'),
        ('title', 'lower', 'upper'),
    )
    parser = argparse.ArgumentParser(
        description='Rename your TV show files into a standard format.')
    for opt in OPTIONS:
        parser.add_argument(*opt['key'], **opt['kwargs'])
    options = vars(parser.parse_args())

    for mutex in mutexes:
        for a, b in combinations(mutex, 2):
            if options[a] and options[b]:
                raise ValueError(f'Conflicting options: {a} and {b}')
    return options


def get_extension(filename):
    """Match video formats and return file extension, if valid."""
    regex = r'^.+\.({})$'.format("|".join(EXTENSIONS))
    match = re.match(regex, filename)
    return match and match.group(1)


def rename(filename, extension, preview, force, title, lower, upper):
    """Match expected regex and changes filename upon confirmation."""
    newname = filename.replace(extension, '')
    regex = r'^(.*)\bs?(?<!\b(h|x)\.)(\d+).?([^\d]\d|\d\d)\b(.*\.)(.*)$'
    match = re.match(regex, filename)

    if match:
        prefix = match.group(1)
        season = int(match.group(3))
        episode = int(re.match(r'(\d+)', match.group(4)).group(1))
        suffix = match.group(5)
        newname = f'{prefix}S{season:02d}E{episode:02d}{suffix}'

    if title:
        newname = newname.title()
    elif lower:
        newname = newname.lower()
    elif upper:
        newname = newname.upper()

    newname = f'{newname}{extension}'
    if filename == newname:
        return

    print(f'{filename} --> {newname}')

    if preview:
        # Nothing more to be done for preview
        return

    if not force:
        # Ask for confirmation
        answer = ''
        while answer not in ANSWERS:
            question = 'Are you sure you want to rename this file? [y/n]\n'
            answer = input(question).lower()

        if ANSWERS.get(answer) is False:
            return

    os.rename(filename, newname)
    return newname


def main():
    """Gather options and traverse files in path."""
    options = validate_options()
    path = options.pop('path')
    os.chdir(path)
    for filename in os.listdir():
        extension = get_extension(filename)
        if extension:
            rename(filename, extension, **options)


if __name__ == '__main__':
    main()
