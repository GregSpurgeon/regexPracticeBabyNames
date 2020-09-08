#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BabyNames python coding exercise.

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

"""
Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration. Here's what the HTML looks like in the
baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 - Extract all the text from the file and print it
 - Find and extract the year and print it
 - Extract the names and rank numbers and print them
 - Get the names data into a dict and print it
 - Build the [year, 'name rank', ... ] list and print it
 - Fix main() to use the extracted_names list
"""

__author__ = """Greg Spurgeon with help from study group D"""

import sys
import re
import argparse


def extract_names(filename):
    """
    Given a single file name for babyXXXX.html, returns a
    single list starting with the year string followed by
    the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', 'Aaron 57', 'Abagail 895', ...]
    """
    names = []
    # open file and read its contents
    with open(filename, "r") as file:
        content = file.read()

    # use regex to search for a pattern to determine the year
    # use group method to get just the year from the match
    match = re.search(r"Popularity\sin\s(\d\d\d\d)", content)
    year = match.group(1)
    names.append(year)

    # use regex to search for all the boynames girlnames and rank
    re_names_and_rank = r'<td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>'
    name_tuples = re.findall(re_names_and_rank, content)

    # loop through name tuples to assign name and rank to dict
    # the name will be the key and the rank is the value
    ranked_names = {}
    for rank, boyname, girlname in name_tuples:
        if boyname not in ranked_names:
            ranked_names[boyname] = rank
        if girlname not in ranked_names:
            ranked_names[girlname] = rank

    # sort names by their key
    sort_names = sorted(ranked_names.keys())

    # add results to names list
    for name in sort_names:
        names.append(name + " " + ranked_names[name])
    return names


def create_parser():
    """Create a command line parser object with 2 argument definitions."""
    parser = argparse.ArgumentParser(
        description="Extracts and alphabetizes baby names from html.")
    parser.add_argument(
        '--summaryfile', help='creates a summary file', action='store_true')
    # The nargs option instructs the parser to expect 1 or more
    # filenames. It will also expand wildcards just like the shell.
    # e.g. 'baby*.html' will work.
    parser.add_argument('files', help='filename(s) to parse', nargs='+')
    return parser


def main(args):
    # Create a command line parser object with parsing rules
    parser = create_parser()
    # Run the parser to collect command line arguments into a
    # NAMESPACE called 'ns'
    ns = parser.parse_args(args)

    if not ns:
        parser.print_usage()
        sys.exit(1)

    file_list = ns.files

    # option flag
    create_summary = ns.summaryfile

    # For each filename, call `extract_names()` with that single file.
    # Format the resulting list as a vertical list (separated by newline \n).
    # Use the create_summary flag to decide whether to print the list
    # or to write the list to a summary file (e.g. `baby1990.html.summary`).

    for filename in file_list:
        names = extract_names(filename)
        file_content = '\n'.join(names)
        if create_summary:
            with open(filename + '.summary', 'w') as output:
                output.write(file_content + '\n')
        else:
            print(file_content)


if __name__ == '__main__':
    main(sys.argv[1:])
