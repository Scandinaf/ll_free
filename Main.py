import logging
import sys
from getopt import GetoptError

import kafka

from bootstrapper import __init_logger__, __init_io_loop__, __init_db_layer__, __init_producer__
from model.word import Word
from service.command_line_arg_parser import CommandLineArgParser
from service.word_service import WordService


async def main(argv):
    try:
        cmd_parser = CommandLineArgParser(argv)
    except GetoptError as exp:
        print(exp.msg)
        print(CommandLineArgParser.get_help_information())
    else:
        await command_line_arg_handler(cmd_parser)


async def command_line_arg_handler(cmd_parser):
    word_service = WordService(db_layer, producer)
    arg_dict = cmd_parser.arg_dict
    if '-a' in arg_dict or '--add' in arg_dict:
        print(await word_service
              .save_word(cmd_parser
                         .arg_dict_to_json(Word)))
    elif '-u' in arg_dict or '--update' in arg_dict:
        print(await word_service
              .update_word(cmd_parser
                           .arg_dict_to_json(Word)))
    elif '-g' in arg_dict or '--get' in arg_dict:
        print(await word_service
              .get_word(arg_dict['-w']))
    elif '-d' in arg_dict or '--delete' in arg_dict:
        print(await word_service
              .delete_word(arg_dict['-w']))
    elif '--reload_translation' in arg_dict:
        print(await word_service
              .reload_translation(arg_dict['-w']))
    else:
        print(CommandLineArgParser.get_help_information())


if __name__ == "__main__":
    __init_logger__()
    module_logger = logging.getLogger()
    loop = __init_io_loop__()
    db_layer = __init_db_layer__(loop)
    try:
        producer = __init_producer__(loop)
    except kafka.errors.ConnectionError as kafka_exp:
        module_logger.error("Exception : {}".format(kafka_exp))
        print("Could you please check the connection to Kafka.")
    else:
        loop.run_until_complete(main(sys.argv[1:]))
    loop.close()
