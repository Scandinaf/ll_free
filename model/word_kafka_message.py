class WordKafkaMessage:
    def __init__(self, word):
        self.word = word

    def build_kafka_message(self):
        return {'word' : self.word}