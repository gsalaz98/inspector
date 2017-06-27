#!/usr/bin/env python3

# Copyright Gerardo Salazar (gsalaz98) 2017
# Distributed under the MIT Open Source License.
# (See accompanying file LICENSE or copy at https://opensource.org/licenses/MIT)

import re
import os
import subprocess

class Inspector(object):
    class DirectoryError(Exception):
        """Custom class to throw errors for directory related issues"""
        pass

    class FileError(Exception):
        """Custom class to throw errors for file related issues"""
        pass

    def __init__(self, project_name=os.path.basename(os.getcwd())):
        self.project_name = project_name
        self.project_dir = project_name

        if self.project_name != os.path.basename(os.getcwd()):
            self.file_path = os.path.realpath(__file__)
            self.parent_dir = os.path.dirname(self.file_path)
            self.project_dir = os.path.dirname(self.parent_dir)

        self.git_ignore = self.project_dir + '/.gitignore'

        self.ignored_files = []
        self.ignored_dir = []

        if self.project_name not in self.parent_dir:
            raise self.DirectoryError("File is not in project directory")
        # Check if `git` is installed on the system the script is being ran on
        try:
            subprocess.check_output(['git'])
        except subprocess.CalledProcessError:
            print("`git` is not installed on your system. Please install and try again.")

    def get_ignored(self):
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
        if not os.path.isfile(self.git_ignore):
            raise self.FileError(".gitignore file not found in root project directory")

        with open(self.git_ignore) as gitignore:
            for line in gitignore:
                # remove newline characters.
                line = line.replace('\n', '')

                # regular expression matches anything not alphanumeric (blank)
                if line.startswith('#') or not re.match("^[^\s]", line):
                    continue

                if os.path.isdir(self.project_dir + '/' + line[1:]) or line.endswith('/'):
                    self.ignored_dir.append(line)
                else:
                    self.ignored_files.append(line)

    def is_ignored(self, files):
        if isinstance(files, list):
            pass
        elif isinstance(files, str):
            pass
        else:
            raise TypeError("Parameter 'files' must be type 'list' or 'str'.")

    def get_authors(self, path, recursive=True, file_name=None):
        """
        function get_authors(path, recursive, file_name) -> generator:

        Parameters:
        'path' -> str: path of the file or folder you are trying to extract information from
        'file_name' -> str (optional): specific file name
        'recursive' -> bool (optional): enables recursive option

        Summary:
        Grabs the authors for a given file and returns a generator object with
        the author name(s) as a `str`.

        Throws:
        `DirectoryError` if 'path' isn't a valid path.
        `TypeError` if 'path' and 'recursive' are both their default values or both set.
        `FileError` if 'file_name' is not a valid file name or file is not found.
        `FileError` if 'file_name' is found in '.gitignore'
        `subprocess.CalledProcessError` if git returns a non-zero exit code.
        """
        if not os.path.ispath(path):
            raise self.DirectoryError("Argument `path` is invalid. Path not found.")
        if file_name is None and not recursive:
            raise TypeError("Neither `file_name` or `recursive` have been set.")
        if file_name is not None and recursive:
            raise TypeError("Both `recursive` and `file_name` have been used,")
        if file_name is not None and not os.path.isfile(path + '/' + file_name):
            raise self.FileError("Argument `file_name` is invalid. File not found.")
        # check if `file_name` is one of the ignored files in '.gitignore'
        # consider TODO: make it so the user can choose if they want to proceed
        if file_name in self.ignored_files:
            raise self.FileError("`file_name` found in '.gitignore'.")

        final_path = path if file_name is None else (path + '/' + file_name)
        shortlog = None

        if not recursive:
            try:
                shortlog = subprocess.check_output(['git', 'shortlog', '-s', final_path])
            except subprocess.CalledProcessError as err:
                print("Invalid path or file name. Printing stack trace...")
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
            # TODO: implement recursive option
            pass

    def add_license(self, follow_gitignore=True):
        """
        function add_license(follow_gitignore) -> None

        Parameters:
        'follow_gitignore' -> bool (optional), default == True:
            allows us to decide if we want to ignore the '.gitignore' file

        Summary:

        Throws:
        `TypeError` if `follow_gitignore` is not type 'bool'
        """
        if not isinstance(follow_gitignore, bool):
            raise TypeError("Parameter 'follow_gitignore' is not of type 'bool'")

        if not follow_gitignore:
            # implement situation where user wants to ignore '.gitignore'
            pass

if __name__ == '__main__':
    state = Inspector()

    print("Ignored Files: ", end='')
    print(state.ignored_files)

    print("Ignored Directories: ", end='')
    print(state.ignored_dir)
