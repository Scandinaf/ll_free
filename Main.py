import sys, getopt


def main(argv):
    optlist, _ = getopt.getopt(argv, "a:", ["add="])

    if len(optlist) == 0:
        show_help_information()
        sys.exit(2)

    for opt, arg in optlist:
        if opt == '-a' or opt == '--add':
            print("Record was added!!!")
        else:
            show_help_information()
            sys.exit(2)


def show_help_information():
    print('Usage: Main.py [options]')
    print('Options:')
    print('-a, --add OBJECT     Add new word in the vocabulary')


if __name__ == "__main__":
   main(sys.argv[1:])