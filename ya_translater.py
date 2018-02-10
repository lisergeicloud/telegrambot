from yandex_translate import YandexTranslate
from mytokens import ya_translate_token

translate = YandexTranslate(ya_translate_token)


def translate_this(text, direction='en-ru'):
    response = translate.translate(text, direction)
    response = '{} - {}'.format(text, response['text'][0])
    return response


if __name__ == '__main__':
    print('Languages:', translate.langs)
    print('Translate directions:', translate.directions)
    print('Detect language:', translate.detect('Привет, мир!'))
    print('Translate:', )  # or just 'en'
