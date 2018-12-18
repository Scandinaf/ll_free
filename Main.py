import asyncio
import getopt
import logging
import sys
from logging.config import fileConfig

from service.word_service import WordService


async def main(argv, loop):
    optlist, _ = getopt.getopt(argv, "a:", ["add="])

    if len(optlist) == 0:
        show_help_information()
        sys.exit(2)

    for opt, arg_json in optlist:
        word_service = WordService(loop)
        if opt == '-a' or opt == '--add':
            print(await word_service.save_word(arg_json))
        else:
            show_help_information()
            sys.exit(2)


def show_help_information():
    print('Usage: Main.py [options]')
    print('Options:')
    print('-a, --add OBJECT     Add new word in the vocabulary')


def init_logger():
    fileConfig('logging.conf')
    logger = logging.getLogger()
    logger.info("Logger was initialized.")


if __name__ == "__main__":
    init_logger()
    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(main(sys.argv[1:], ioloop))
    ioloop.close()
