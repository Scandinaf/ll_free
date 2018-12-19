import asyncio
import logging
import sys
from getopt import GetoptError
from logging.config import fileConfig

from model.word import Word
from service.command_line_arg_parser import CommandLineArgParser
from service.word_service import WordService


async def main(argv, loop):
    try:
        cmd_parser = CommandLineArgParser(argv)
    except GetoptError as exp:
        print(exp.msg)
    else:
        await command_line_arg_handler(cmd_parser, loop)


async def command_line_arg_handler(cmd_parser, loop):
    word_service = WordService(loop)
    arg_dict = cmd_parser.arg_dict
    if '-a' in arg_dict or '--add' in arg_dict:
        print(await word_service
              .save_word(cmd_parser
                         .arg_dict_to_json(Word)))
    else:
        print(CommandLineArgParser.get_help_information())


def init_logger():
    fileConfig('logging.conf')
    logger = logging.getLogger()
    logger.info("Logger was initialized.")


if __name__ == "__main__":
    init_logger()
    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(main(sys.argv[1:], ioloop))
    ioloop.close()
