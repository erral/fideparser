import argparse
from ratingperiod import RatingPeriod


def main():
    parser = argparse.ArgumentParser(description='Parse FIDE site to get tournament info')

    parser.add_argument('country',
                        type=str,
                        help='Enter the three letter country-code',
                        )
    parser.add_argument('period',
                        type=str,
                        help='''Enter the rating list period you want to process.
                        Take into account that this export method only works for
                        already computed rating periods and not for the future ones.
                        Period strings are like these: 2011-01-01, 2011-03-01, etc.
                        ''',
                        )

    parser.add_argument('output_file',
                        type=str,
                        help='''Filename where the data will be stored. If the
                        file exists, its contents will be overwritten, otherwise
                        a new file will be created'''
                        )

    parser.add_argument('export_format',
                        type=str,
                        help='Select the format of the exported data',
                        choices=['binary', 'json', 'csv'],
                        default='binary'
                        )

    parser.add_argument('--datafile',
                        type=str,
                        help='''Optional data file. If you have a previously created
                        file in 'binary' format, you can write the path to it.
                        All the data will be imported from there, and thus
                        period and country parameters will be ignored'''

    )

    arguments = parser.parse_args()

    rating_period = RatingPeriod(arguments.country,
                                 arguments.period)

    if arguments.datafile:
        rating_period.load_from_file(arguments.datafile)
    else:
        rating_period.save()

    rating_period.export(arguments.output_file,
                         arguments.export_format)
