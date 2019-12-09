import vk_api
import json
from vk_api.longpoll import VkLongPoll, VkEventType
import random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import urllib.request

import cf_api
import constant
import table
import goods

vk_session = vk_api.VkApi(token=constant.token)

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

def write_message(user_id, msg):
    random_id = random.randint(1, 1234567898765)
    vk_session.method('messages.send', {'user_id': user_id, 'message': msg, 'random_id': random_id})

def try_to_sync(user_id):
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
                table.addNewUser(handle, user_id)
                write_message(user_id, 'Отлично, вы прошли проверку! Сейчас внесу вас в таблицу!')
            else:
                write_message(user_id, 'Что-то пошло не так... Возможно вы ввели неверный ник или ваш профиль на '
                                             'кодфорсе закрыт')
            return 0
    return 1

def isDivTwo(st):
    a = st.split()
    if a[0] == 'div2' and len(a) == 2:
        return 1
    else:
        return 0

def main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user:
            # print('abacaba', event.text.lower())
            command = event.text.lower()
            if command in constant.SYNC_:
                try_to_sync(event.user_id)
            elif command in constant.EXIT_COMMANDS_:
                exit()
            elif command in constant.bad_words:
                write_message(event.user_id, 'Сам такой!!!')
            elif command in constant.balance:
                points = table.getPointsWithVkId(event.user_id)
                if points < 0:
                    write_message(event.user_id, 'Не удалось получить данные о вашем счете!')
                else:
                    write_message(event.user_id, 'У вас на счету: ' + str(points) + ' баллов.')
            elif command in constant.GOOD_WORDS_:
                write_message(event.user_id, 'Какой вы клевый! Уважаю!')
            elif command in constant.RESET_POINTS_:
                table.resetPointsWithVkId(event.user_id)
            elif isDivTwo(command) > 0:
                a = command.split()
                if a[1].isdigit():
                    if table.isEnoughtForBet(event.user_id, a[1]) < 1:
                        write_message(event.user_id, 'У вас слишком мало баллов или '
                                                     'ваша ставка слишком маленькая (минимальная ставка 10 sp).')
                        continue
                    write_message(event.user_id, 'Ваша ставка принята!')
                    table.setSpentPointsWithVkId(event.user_id, a[1])
                    goods.tryToAddDivTwoBet(table.getHandleWithVkId(event.user_id), a[1])
                elif a[1].lower() == 'cancel':
                    goods.tryToCancelDivTwoBet(table.getHandleWithVkId(event.user_id))
                    write_message(event.user_id, 'Ваша ставка на проведение контеста '
                                                 'второго дивизиона успешно аннулирована.')
                else:
                    write_message(event.user_id, 'У команды div2 нет такого параметра!')
            elif command in constant.HELLO_:
                write_message(event.user_id, 'Добрый день! Рад тебя видеть, друг!')
            else:
                if (event.user_id == '413059663'):
                    write_message(event.user_id, 'Хуй будешь?')
                else:
                    write_message(event.user_id, 'Я не понимаю вас :-(')
            continue

main()