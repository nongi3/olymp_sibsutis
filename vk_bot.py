import vk_api
import json
from vk_api.longpoll import VkLongPoll, VkEventType
import random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import urllib.request

import cf_api
import constant
import table

# API-ключ созданный ранее


vk_session = vk_api.VkApi(token=constant.token)

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

sinc_ = []
exit_commands_ = []

def write_message(user_id, msg):
    random_id = random.randint(1, 1234567898765)
    vk_session.method('messages.send', {'user_id': user_id, 'message': msg, 'random_id': random_id})

def init():
    global sync_
    global exit_commands_
    sinc_.append('синхра')
    sinc_.append('sync')
    sinc_.append('add')
    exit_commands_.append('exit')

def try_to_sinc(user_id):
    write_message(user_id, 'Введите ваш хэндл на codeforces для '
                           'добавления вас в таблицу и синхронизации с аккаунтом vk')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user:
            handle = event.text.lower()
            try:
                request_url = 'http://codeforces.com/api/user.info?handles=' + handle
                response = urllib.request.urlopen(request_url)
                res = json.loads(response.read())
            except Exception:
                write_message(user_id, 'Что-то пошло не так... Возможно вы ввели неверный ник или ваш профиль на '
                                       'кодфорсе закрыт')
                return 1
            if 'result' not in res:
                write_message(user_id, 'Что-то пошло не так... Возможно вы ввели неверный ник или ваш профиль на '
                                       'кодфорсе закрыт')
                return 1
            if 'vkId' not in res['result'][0]:
                write_message(user_id, 'Что-то пошло не так... Возможно вы ввели неверный ник или ваш профиль на '
                                       'кодфорсе закрыт')
                return 1
            vk_id_from_cf = res['result'][0]['vkId']
            if str(user_id) == str(vk_id_from_cf):
                cf_api.add_new_handle(handle)
                write_message(user_id, 'Отлично, вы прошли проверку! Сейчас внесу вас в таблицу!')
            else:
                write_message(user_id, 'Что-то пошло не так... Возможно вы ввели неверный ник или ваш профиль на '
                                             'кодфорсе закрыт')
            return 0
    return 1

def main():
    init()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user:
            print('abacaba', event.text.lower())
            command = event.text.lower()
            if command in sinc_:
                try_to_sinc(event.user_id)
            elif command in exit_commands_:
                exit()
            elif command in constant.bad_words:
                write_message(event.user_id, 'Сам такой!!!')
            elif command in constant.balance:
                table.getPointsWithVkId(event.user_id)
            else:
                write_message(event.user_id, 'Я не понимаю вас :-(');
            continue

main()