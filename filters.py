from telegram.ext import BaseFilter


class FilterJoke(BaseFilter):
    def filter(self, message):
        return 'joke' in message.text.lower()


class FilterTranslate(BaseFilter):
    def filter(self, message):
        return 'translate' in message.text.lower()
