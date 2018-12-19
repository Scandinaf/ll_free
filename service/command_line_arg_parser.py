import getopt


class CommandLineArgParser:
    shortopts = "agdw:t:p:s:"
    lognopts = ["add","get","delete"]

    def __init__(self, argv):
        optlist, _ = getopt.getopt(argv,
                                   CommandLineArgParser.shortopts,
                                   CommandLineArgParser.lognopts)
        self.arg_dict = dict(optlist)
        self.__validate_arg_dict__()

    def __validate_arg_dict__(self):
        if '-w' not in self.arg_dict:
            raise getopt.GetoptError(msg="The parameter -w is required", opt="-w")

    def arg_dict_to_json(self, cls):
        return cls.arg_dict_to_json(self.arg_dict)

    @staticmethod
    def get_help_information():
        return 'Usage: Main.py [operation] [options]\n' \
               + 'Options:\n' \
               + '-w [Required]    A word that will be saved in the dictionary\n' \
               + '-t               A translation that will be saved in the dictionary\n' \
               + '-p               A phrase with the specified word\n' \
               + '-s               A synonyms for the specified word\n' \
               + 'Operations:\n' \
               + '-a, --add        Add new word in the dictionary\n' \
               + '-d, --delete     Delete word from the dictionary\n' \
               + '-g, --get        Get word from the dictionary\n'
