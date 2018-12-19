import getopt


class CommandLineArgParser:
    shortopts = "aw:t:p:s:"
    lognopts = ["add="]

    def __init__(self, argv):
        optlist, _ = getopt.getopt(argv,
                                   CommandLineArgParser.shortopts,
                                   CommandLineArgParser.lognopts)
        self.arg_dict = dict(optlist)

    def arg_dict_to_json(self, cls):
        return cls.arg_dict_to_json(self.arg_dict)

    @staticmethod
    def get_help_information():
        return 'Usage: Main.py [options]\n' \
               + 'Options:\n' \
               + '-a, --add OBJECT     Add new word in the vocabulary\n'
