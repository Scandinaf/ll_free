class Error:
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "An error has occurred. Description - {}".format(self.message)
