# coding=utf-8
import vk_api
import json
from vk_api.longpoll import VkLongPoll, VkEventType
import random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import urllib.request

import cf_api
import secret_constants
import constants
import table
import goods
import price

vk_session = vk_api.VkApi(token=secret_constants.token)

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


def write_message(user_id, msg):
    random_id = random.randint(1, 1234567898765)
    vk_session.method('messages.send', {'user_id': user_id, 'message': msg, 'random_id': random_id})

sync_list = []


def makeTopic(name):
    text = 'В следующем лоте - ' + name + ' - принимают участие: ' + listToStr(goods.getParty(name))
    vk_api.VkApi(token=secret_constants.accecc_token).method('board.addTopic', {
        'group_id': '189233231',
        'title': 'Проведение лота: ' + name,
        'text': text,
        'from_group': 1,
        'attachments': []})


def listToStr(values):
    res = ''
    for i in range(0, len(values)):
        res += str(values[i])
        if i + 1 < len(values):
            res += ', '
    return res


def isBinding(event):
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user and \
            event.user_id in sync_list:
        handle = event.text.lower()
        try:
            request_url = 'http://codeforces.com/api/user.info?handles=' + handle
            response = urllib.request.urlopen(request_url)
            res = json.loads(response.read())
        except Exception:
            write_message(event.user_id, 'Что-то пошло не так... Возможно вы ввели неверный ник или ваш профиль на '
                                         'кодфорсе закрыт')
            return True
        if 'result' not in res:
            write_message(event.user_id, 'Возникла ошибка при получении данных от cf API')
            return True
        if len(res['result']) < 1:
            write_message(event.user_id, 'Возникла ошибка при получении данных от cf API')
            return True
        if 'vkId' not in res['result'][0]:
            write_message(event.user_id, 'Возникла ошибка при получении данных от cf API')
            return True
        vk_id_from_cf = res['result'][0]['vkId']
        if str(event.user_id) != str(vk_id_from_cf):
            write_message(event.user_id, 'Страница вк в профиле с указанным хэндлом отличается от вашей!')
            return True
        if table.isUserAlreadyExist(event.user_id):
            write_message(event.user_id, 'Вы уже зарегистрированы в системе! Повторное подтверрждение не требуется!')
            return True
        table.addNewUser(handle, event.user_id)
        write_message(event.user_id, 'Отлично, вы прошли проверку! Сейчас внесу вас в таблицу!')
        return True
    return False


def isSyncCommand(command):
    if command not in constants.SYNC_:
        return False
    if event.user_id in sync_list:
        write_message(event.user_id, 'Жду с нетерпением вашего хэндла, чтобы подтвердить вступление'
                                     ' в наши ряды')
        return True
    write_message(event.user_id, 'Введите ваш хэндл на codeforces для '
                                 'добавления вас в таблицу и синхронизации с аккаунтом vk')
    sync_list.append(event.user_id)
    return True


def isUserLogin(user_id):
    if table.getHandleWithVkId(user_id) == 'None':
        write_message(user_id, 'Пройдите регистрацию, пожалуйста!')
        return False
    return True


def isExit(command):
    if command in constants.EXIT_COMMANDS_:
        write_message(event.user_id, 'Пока :-D')
        exit()


def isGood(command):
    if command in constants.GOOD_WORDS_:
        write_message(event.user_id, 'Какой вы клевый! Уважаю!')
        return True
    return False


def isBad(command):
    if command in constants.bad_words:
        write_message(event.user_id, 'Сейчас обидно было :-(')
        return True
    return False


def isBalance(command):
    if command in constants.balance:
        points = table.getPointsWithVkId(event.user_id)
        if points < 0:
            write_message(event.user_id, 'Не удалось получить данные о вашем счете!')
        else:
            write_message(event.user_id, 'У вас на счету: ' + str(points) + ' баллов.')
        return True
    return False


def isReset(command):
    if command in constants.RESET_ONE_USER_POINTS_:
        table.resetPointsWithVkId(event.user_id)
        write_message(event.user_id, 'Данные успешно обновлены!')
        points = table.getPointsWithVkId(event.user_id)
        write_message(event.user_id, 'У вас на счету: ' + str(points) + ' баллов.')
        return True
    elif command in constants.RESET_ALL_USERS_POINTS_:
        write_message(event.user_id, 'Обновление таблицы может занять некоторое время!')
        table.resetAllUsersInfo()
        write_message(event.user_id, 'Таблица полностью обновлена!')
        return True
    return False


def isGreeting(command):
    if command in constants.HELLO_:
        write_message(event.user_id, 'Добрый день! Рад тебя видеть, друг!')
        return True
    return False


def isRespect(command):
    if command in constants.WHO_RESPECT_THE_BEES:
        write_message(event.user_id, 'кто к ним не пристает,\n того они не жалят,\n тому приносят мёд!')
        return True
    return False


def isPing(command):
    if command in constants.PING_:
        write_message('30806644', 'Какой-то петуч нуждается в помощи.')
        write_message(event.user_id, 'Ваша молитва услышана!')
        return True
    return False


def isHelp(command):
    if command in constants.HELP_:
        write_message(event.user_id, 'Список доступных вам команд:')
        return True
    return False


def isCorrectEvent(event):
    return event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user


def isFromAdmin(event):
    if event.user_id in constants.ADMIN_VK_ID_:
        command = event.text.lower()
        isExit(command)
        return True
    return False


def isFromUser(event):
    command = event.text.lower()
    if isSyncCommand(command):
        return True
    if isGood(command):
        return True
    if isBad(command):
        return True
    if isBalance(command):
        return True
    if isReset(command):
        return True
    if isGreeting(command):
        return True
    if isRespect(command):
        return True
    if isPing(command):
        return True
    if isHelp(command):
        return True


def main():
    for event in longpoll.listen():
        if not isCorrectEvent(event):
            continue
        if not isUserLogin(event.user_id):
            continue
        if isBinding(event):
            continue
        if isFromAdmin(event):
            continue
        if isFromUser(event):
            continue
        write_message(event.user_id, 'Я не понимаю вас :-(')


main()
