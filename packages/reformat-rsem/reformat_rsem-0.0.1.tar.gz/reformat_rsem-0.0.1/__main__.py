import sys

if __package__:
    from .reformat_rsem import main
else:
    from reformat_rsem import main


main(sys.argv[1:])
