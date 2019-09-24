import getopt
import sys

from RaplaExtractor import RaplaExtractor


def main(argv):
    key = ''
    year = ''
    try:
        opts, args = getopt.getopt(argv, "k:y", ["key=", "year="])
    except getopt.GetoptError:
        print('main.py -k <key> -y <year>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-k':
            print('main.py -k <key> -y <year>')
            sys.exit()
        elif opt in ("-k", "--key"):
            key = arg
        elif opt in ("-y", "--year"):
            year = arg

    x = RaplaExtractor(key=key, year=year)


if __name__ == '__main__':
    main(sys.argv[1:])
