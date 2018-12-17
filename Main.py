import sys, getopt
from service.word_service import save_word


def main(argv):
    optlist, _ = getopt.getopt(argv, "a:", ["add="])

    if len(optlist) == 0:
        show_help_information()
        sys.exit(2)

    for opt, arg_json in optlist:
        if opt == '-a' or opt == '--add':
            print(save_word(arg_json))
        else:
            show_help_information()
            sys.exit(2)


def show_help_information():
    print('Usage: Main.py [options]')
    print('Options:')
    print('-a, --add OBJECT     Add new word in the vocabulary')


if __name__ == "__main__":
   main(sys.argv[1:])