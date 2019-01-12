import logging

from pygame import mixer

from model.error import Error
from model.word import Word
from utils.helper import check_index_valid, file_exists


class GameService:
    def __init__(self, db_layer):
        self.db_layer = db_layer
        self.module_logger = logging.getLogger()
        self.mixer = mixer.init()

    async def start_game(self):
        self.module_logger.info("Game started!!!")
        try:
            word_list_json = await self.db_layer.word.get_list_to_study()
            if not word_list_json:
                return "Add new words to the dictionary and come back!!!"
            await self.__game__(self.__convert_to_inst__(word_list_json))
            return "Bye Bye!!!"
        except Exception as exp:
            return self.__unexpected_exception__(exp)

    async def __game__(self, word_list):
        bulk_update_dict = {}
        index = -1
        print(self.__get_rules__())
        while True:
            print("current index - {0}, total words - {1}".format(index + 1, len(word_list)))
            command = input("Please enter command: ")
            if command == 'next':
                new_index, result = self.__game_iter__(index,
                                                       1,
                                                       word_list,
                                                       bulk_update_dict)
                index = new_index
                self.__handle_command_result__(result)
            elif command == 'previous':
                new_index, result = self.__game_iter__(index,
                                                       -1,
                                                       word_list,
                                                       bulk_update_dict)
                index = new_index
                self.__handle_command_result__(result)
            elif command == 'play':
                self.__handle_command_result__(
                    self.__game_play_audio__(word_list, index))
            elif command == 'exit':
                if bulk_update_dict:
                    await self.db_layer.word.update_study_status(
                        list(bulk_update_dict.values()))
                break
            else:
                print(self.__get_rules__())

    def __game_iter__(self, index, value, word_list, bulk_update_dict):
        new_index = index + value
        if check_index_valid(new_index, len(word_list)):
            entity = word_list[new_index]
            if entity.word not in bulk_update_dict:
                bulk_update_dict[entity.word] = entity
            return new_index, entity.get_pretty_view()
        else:
            return index, "You are trying to go beyond the index."

    def __game_play_audio__(self, word_list, index):
        path = word_list[index].sound_record_path
        if path is not None and file_exists(path):
            mixer.music.load(path)
            mixer.music.play()
        else:
            self.module_logger.warning("File not found. Path - {}".format(path))
            return "File not found"

    def __unexpected_exception__(self, exp):
        self.module_logger.error("Exception : {}".format(exp))
        return Error("Something was wrong")

    def __handle_command_result__(self, result):
        if result is not None:
            print(result)

    @staticmethod
    def __get_rules__():
        return 'Commands:\n' \
               + 'next                      Show next word\n' \
               + 'previous                  Show previous word\n' \
               + 'play                      Play audio record\n' \
               + 'exit                      Exit the program\n'

    @staticmethod
    def __convert_to_inst__(word_list_json):
        return list(map(lambda word_json: Word.init_form_json(word_json),
                        word_list_json))
