import getopt

from service.command_line_arg_validator import validate_arg_dict
from service.decorator import validate_wrapper


class CommandLineArgParser:
    shortopts = "agduw:t:p:s:"
    lognopts = ["add", "get", "delete", "update"]

    def __init__(self, argv):
        optlist, _ = getopt.getopt(argv,
                                   CommandLineArgParser.shortopts,
                                   CommandLineArgParser.lognopts)
        self.__set_atg_dict__(arg_dict=dict(optlist))

    @validate_wrapper(validation_func=validate_arg_dict)
    def __set_atg_dict__(self, arg_dict):
        self.arg_dict = arg_dict

    def arg_dict_to_json(self, cls):
        return cls.arg_dict_to_json(self.arg_dict)

    @staticmethod
    def get_help_information():
        return 'Usage: Main.py [operation] [options]\n' \
               + 'Options:\n' \
               + '-w [Required]    A word that will be saved in the dictionary\n' \
               + '-t               A translation that will be saved in the dictionary\n' \
               + '-p               A phrase with the specified word\n' \
               + '-s               A synonyms for the specified word\n\n' \
               + 'Operations:\n' \
               + '-a, --add        Add new word in the dictionary\n' \
               + '-d, --delete     Delete word from the dictionary\n' \
               + '-g, --get        Get word from the dictionary\n' \
               + '-u, --update     Update word from the dictionary\n\n' \
               + 'Example:\n' \
               + 'Main.py -add -w bad -t плохой\n' \
