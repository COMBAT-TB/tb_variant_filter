#!/usr/bin/env python

import argparse
import pprint
from io import StringIO

import requests

from .region_list import bed_to_regions

def main():
    parser = argparse.ArgumentParser(description='Print a list of Location objects from a BED file input')
    parser.add_argument('bed_location', help='Path or URL to BED locations')
    args = parser.parse_args()

    if '://' in args.bed_location:
        response = requests.get(args.bed_location)
        if response.status_code != 200:
            response.raise_for_status()
        bed_file = StringIO(response.text)
    else:
        bed_file = open(args.bed_location)
    
    pp = pprint.PrettyPrinter(indent=8)
    pp.pprint(bed_to_regions(bed_file))

if __name__ == '__main__':
    main()