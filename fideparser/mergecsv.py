import argparse
import csv
import sys

def merge(outfile,  infiles):
    data = []
    for filename in infiles:
        try:
            fp = open(filename, 'r')
        except IOError:
            print('File %s does not exists. Nothing done.' % filename)
            sys.exit(1)

        reader = csv.DictReader(fp)
        data.extend([i for i in reader])
        fp.close()

    try:
        f = open(outfile, 'w')
        writer = csv.DictWriter(f, set(reader.fieldnames))
        writer.writeheader()
        writer.writerows(data)
    except IOError:
        print('An error occured writing %s. Nothing done.' % outfile)
        sys.exit(1)

def main():

    parser = argparse.ArgumentParser(description="""Merge CSV files created with fideparser.
    Sometimes the order of the columns in the generated files is not correct, and you
    need to merge the files. This scripts does it for you in an easy way.

    If the output file exists, it will be overwritten.

    """)

    parser.add_argument('outfile',
                        type=str,
                        help='The name of the file that will save the merged data',
                        )

    parser.add_argument('infiles',
                        type=str,
                        nargs='+',
                        help='CSV filenames to be merged')

    arguments = parser.parse_args()
    merge(arguments.outfile, arguments.infiles)
    print('%s file was generated, after merging %s' % (arguments.outfile,
                                                    ' '.join(arguments.infiles)
        ))


