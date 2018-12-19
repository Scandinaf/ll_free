import sys
from getopt import GetoptError

from bootstrapper import io_loop, db_layer
from model.word import Word
from service.command_line_arg_parser import CommandLineArgParser
from service.word_service import WordService


async def main(argv):
    try:
        cmd_parser = CommandLineArgParser(argv)
    except GetoptError as exp:
        print(exp.msg)
    else:
        await command_line_arg_handler(cmd_parser)


async def command_line_arg_handler(cmd_parser):
    word_service = WordService(db_layer)
    arg_dict = cmd_parser.arg_dict
    if '-a' in arg_dict or '--add' in arg_dict:
        print(await word_service
              .save_word(cmd_parser
                         .arg_dict_to_json(Word)))
    else:
        print(CommandLineArgParser.get_help_information())


if __name__ == "__main__":
    io_loop.run_until_complete(main(sys.argv[1:]))
    io_loop.close()
