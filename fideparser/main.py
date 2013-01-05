import argparse

def main():
    parser = argparse.ArgumentParser(description='Parse FIDE site to get tournament info')

    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                    help='an integer for the accumulator')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                    const=sum, default=max,
    #                    help='sum the integers (default: find the max)')
    parser.add_argument('country',
                        type=str,
                        help='Enter the three letter country-code',
                        )
    parser.add_argument('period',
                        type=str,
                        help='''Enter the rating list period you want to process.
                        Take into account that this export method only works for
                        already computed rating periods and not for the future ones.
                        ''',
                        )

    arguments = parser.parse_args()
    rating_period = RatingPeriod(country, period)
    rating_period.save()
    rating_period.export()
