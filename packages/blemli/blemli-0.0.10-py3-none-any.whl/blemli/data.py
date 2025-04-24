#!/usr/bin/env python

import re
def indic(file,key):
    try:
        with open(file, "r") as file:
            data=[line for line in file.readlines() if re.match(r'^\S+ \S+$',line)]
            dictionary=dict([line.strip().split() for line in data])
            try:
                return dictionary.get(key)
            except KeyError:
                logging.error(f"KeyError: '{key}' not found in dictionary '{file}'")
                return None
    except FileNotFoundError:
        logging.error("Dictionary file '{file}' not found")
        return None
