from telegram.ext import BaseFilter


class FilterJoke(BaseFilter):
    def filter(self, message):
        return 'joke' in message.text.lower()
