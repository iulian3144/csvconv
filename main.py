#!/usr/bin/python
import sys
import csv
import argparse
from CSVFormatter import CSVtoHTMLFormatter



def log_error(*args):
    print("ERROR:", *args, file=sys.stderr)



def log_warning(*args):
    print("WARNING:", *args, file=sys.stderr)



def parse_csv_line(header, row=None):
    """Custom CSV line parser.

    Parse a CSV row (based on header) according to the following rules:
    - if the last character of the header's item is a '>', the next item will
      be merged with it
    - if the column is empty and it is to be merged, nothing will be appended
      to the header item
    :return: A dictionary containing the parsed header and the parsed row
    """
    merge = False
    parsed_header = []
    parsed_row = []
    if row is None or len(row) == 0:
        row = header
    for header_col, row_col in zip(header, row):
        header_col_stripped = header_col.rstrip(">")
        # merge last field with the current one
        if merge:
            # do not append empty field
            if len(header_col_stripped) > 0:
                parsed_header[-1] += f":{header_col_stripped}"
            parsed_row[-1] += f":{row_col}"
        else:
            # skip column if it's empty
            if len(header_col_stripped) > 0:
                parsed_header.append(header_col_stripped)
                parsed_row.append(row_col)

        merge = False
        if len(header_col) > 0 and header_col[-1] == '>':
            merge = True
    return {"header": parsed_header, "row": parsed_row}



parser = argparse.ArgumentParser(description='Convert a CSV file to a specified format.', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('infile', metavar='INFILE',
        const=None, default=sys.stdin,
        help='Input file (default: STDIN). First row will be used as the table header.')
parser.add_argument('-d', '--delimiter', metavar='DELIM', dest='delimiter',
        const=None, default=";", help="Character used to separate fields.")
parser.add_argument('-o', '--output', metavar='OUTFILE', dest='outfile',
        const=None, default=sys.stdout, help="File to write output to (default: STDOUT).")
parser.add_argument('-f', '--format', metavar='FORMAT', dest='format',
        const=None, default="html", help="Specify output format (default: html).\n"\
            "Supported formats:\n"\
            "  html: output data as a HTML formatted table")

SUPPORTED_FORMATS = {
    "html": CSVtoHTMLFormatter
}

def main():
    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    delimiter = args.delimiter
    format = args.format
    if format not in SUPPORTED_FORMATS:
        log_error("Specified output format (`{}`) is not supported.".format(format))
        return 1

    csvformatter = SUPPORTED_FORMATS[format]
    if infile is not sys.stdin:
        infile = open(infile, 'r')
    if outfile is not sys.stdout:
        print(f"Data will be written to {outfile}")
        outfile = open(outfile, 'w')


    parsed_rows = []
    csvreader = csv.reader(infile, delimiter=delimiter)
    # first row is the header
    header = next(csvreader, None)
    if not header:
        log_warning("Empty file!")
        return(1)
    parsed_header = parse_csv_line(header)["header"]

    for row in csvreader:
        parsed_row = parse_csv_line(header, row)['row']
        parsed_rows.append(parsed_row)


    data = csvformatter(parsed_header, parsed_rows)

    data.print(file=outfile)

    if args.infile is not sys.stdin:
        infile.close()
    if args.outfile is not sys.stdout:
        outfile.close()


if __name__ == '__main__':
    main()