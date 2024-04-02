# temporary solution pending translation customization

def translate(context, text):
    return text


def tr_(text):
    return translate("cadbaselibrary", text)

translations_dict = {
    'ru_RU': {
        ('Operator', 'Open'): 'Открыть',
        ('Operator', 'Go back'): 'Назад',
        ('Operator', 'Authorization'): 'Авторизация',
        ('Operator', 'Pull data'): 'Получить данные',
        ('Operator', 'Link file'): 'Прилинковать файл',
        ('Operator', 'Push changes'): 'Отправить изменения',
        ('Operator', 'Settings'): 'Настройки',
        ('Operator', 'Settings'): 'Настройки'
    }
}