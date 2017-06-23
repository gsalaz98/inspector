#!/usr/bin/env python3

#       Copyright Gerardo Salazar (gsalaz98) 2017
# Distributed under the MIT Open Source License.
#     (See accompanying file LICENSE or copy at
#         https://opensource.org/licenses/MIT)

# This script checks source file(s) (*.h, *.hpp, *.c, *.cpp) for a license
# and inserts it into source file(s) if not found.

import re
import os
import sys
import subprocess

PROJECT_NAME = "Discorded"

FILE_PATH = os.path.realpath(__file__)
PARENT_DIR = os.path.dirname(FILE_PATH)
PROJECT_DIR = os.path.dirname(PARENT_DIR)
GIT_IGNORE = PROJECT_DIR + '/.gitignore'

IGNORED_FILE = []
IGNORED_DIR = []

class DirectoryError(Exception):
    # Custom class to throw errors for directory related issues
    pass

class FileError(Exception):
    # Custom class to throw errors for file related issues
    pass

if PROJECT_NAME not in PARENT_DIR:
    raise DirectoryError("File is not in project directory")

# Check if `git` is installed on the system the script is being ran on
try:
    subprocess.check_output(['git'])
except subprocess.CalledProcessError:
    print("`git` is not installed on your system. Please install and try again.")

def get_ignored():
    """
    function get_ignored(None) -> None:

    Summary:
    Retrieves user defined ignored files/directories listed
    in the '.gitignore' file at the project root.

    Throws:
    `FileError` if '.gitignore' can't be found at the project's root directory

    TODO:
    Check if the project has more than one '.gitignore' file and handle accordingly.
    """
    if not os.path.isfile(GIT_IGNORE):
        raise FileError(".gitignore file not found in root project directory")

    with open(GIT_IGNORE) as gitignore:
        for line in gitignore:
            # remove newline characters.
            line = line.replace('\n', '')

            # regular expression matches anything not alphanumeric (blank)
            if line.startswith('#') or not re.match("^[^\s]", line):
                continue

            if os.path.isdir(PROJECT_DIR + '/' + line[1:]) or line.endswith('/'):
                IGNORED_DIR.append(line)
            else:
                IGNORED_FILE.append(line)

def get_authors(path, file_name=None, recursive=False):
    """
    function get_authors(path, file_name=None, recursive=Bool) -> generator:

    Summary:
    Grabs the authors for a given file and returns a generator object with
    the author name(s) as a `str`.

    Throws:
    `DirectoryError` if 'path' isn't a valid path.
    `TypeError` if 'path' and 'recursive' are both their default values.
    `FileError` if 'file_name' is not a valid file name or file is not found.
    `FileError` if 'file_name' is found in '.gitignore'
    `subprocess.CalledProcessError` if git returns a non-zero exit code.
    """
    if not os.path.ispath(path):
        raise DirectoryError("Argument `path` is invalid. Path not found.")
    if file_name is None ablank spacend not recursive:
        raise TypeError("Neither `file_name` or `recursive` have been set.")
    if file_name is not None and not os.path.isfile(path + '/' + file_name):
        raise FileError("Argument `file_name` is invalid. File not found.")
    # check if `file_name` is one of the ignored files in '.gitignore'
    # consider TODO: make it so the user can choose if they want to proceed
    if file_name is in IGNORED_FILE:
        raise FileError("`file_name` found in '.gitignore'.")

    final_path = path if file_name is None else (path + '/' + file_name)
    shortlog = None

    if not recursive:
        try:
            shortlog = subprocess.check_output(['git', 'shortlog', '-s', final_path])
        except subprocess.CalledProcessError as err:
            print('Invalid path or file name. Printing stack trace...')
            print(err)

        # subprocess returns information as a byte object.
        # Let's convert it into a python `str` object.
        shortlog = shortlog.decode('utf-8')
        # then, convert it into a list.
        shortlog = shortlog.split('\n')
        # last element contains no data. Let's get rid of it.
        del shortlog[-1]

        for name in shortlog:
            # There is always 8 characters before the author's name
            name_substr = slice(7, None, None)
            yield name[name_substr]

    if recursive:
        try:


def add_license(follow_gitignore=True):
    pass

if __name__ == '__main__':
    get_ignored()

    print("Ignored Files: ", end='')
    print(IGNORED_FILE)

    print("Ignored Directories: ", end='')
    print(IGNORED_DIR)

