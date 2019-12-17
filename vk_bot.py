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

is_lottery_start = False
lottery_list = []

def tryToLottery(number):
    global lottery_list
    random.shuffle(lottery_list)
    res = []
    if len(lottery_list) < number:
        for i in lottery_list:
            res.append(i)
    else:
        for i in range(number):
            res.append(lottery_list[i])
    return res

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
    if a[0] in constant.DIV2 and len(a) == 2:
        return 1
    else:
        return 0

def isLottery(st):
    a = st.split()
    if a[0] in constant.LOTTERY_:
        return True
    else:
        return False

def listToStr(values):
    res = ''
    for i in range(0,len(values)):
        res += str(values[i])
        if i + 1 < len(values):
            res += ', '
    return res

def main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user:
            # print('abacaba', event.text.lower())
            command = event.text.lower()
            if command in constant.SYNC_:
                try_to_sync(event.user_id)
            elif command in constant.EXIT_COMMANDS_:
                exit()
            elif isLottery(command):
                if str(event.user_id) == '30806644':
                    global is_lottery_start
                    if (command == 'розыгрыш'):
                        if is_lottery_start:
                            write_message(event.user_id, 'Никита, ты уже начал розыгрыш! Не балуйся!')
                            continue
                        is_lottery_start = True
                        write_message(event.user_id, 'Да начнется розыгрыш!')
                    else:
                        a = command.split()
                        if len(a) != 2:
                            write_message(event.user_id, 'Никита, опять фигню какую-то ввел!')
                            continue
                        if a[1].isdigit() == 0:
                            write_message(event.user_id, 'второе значение должно быть числом')
                            continue
                        winners = tryToLottery(int(a[1]))
                        write_message(event.user_id, 'В розыгрыше выиграли:')
                        for winner in winners:
                            write_message(event.user_id, str(winner))
                        lottery_list.clear()
                        is_lottery_start = False
                else:
                    if is_lottery_start == 0:
                        write_message(event.user_id, 'Розыгрыш еще не начался!')
                        continue
                    user = vk_session.method("users.get", {"user_ids": event.user_id})
                    fullname = user[0]['first_name'] + ' ' + user[0]['last_name']
                    if fullname not in lottery_list:
                        lottery_list.append(fullname)
                        write_message(event.user_id, 'Ваш голос учтен!')
                    else:
                        write_message(event.user_id, 'Вы уже принимаете участие в розыгрыше!')

            elif command in constant.bad_words:
                write_message(event.user_id, 'Сейчас обидно было :-(')
            elif command in constant.balance:
                points = table.getPointsWithVkId(event.user_id)
                if points < 0:
                    write_message(event.user_id, 'Не удалось получить данные о вашем счете!')
                else:
                    write_message(event.user_id, 'У вас на счету: ' + str(points) + ' баллов.')
            elif command in constant.GOOD_WORDS_:
                write_message(event.user_id, 'Какой вы клевый! Уважаю!')
            elif command in constant.RESET_ONE_USER_POINTS_:
                table.resetPointsWithVkId(event.user_id)
                write_message(event.user_id, 'Данные успешно обновлены!')
            elif command in constant.RESET_ALL_USERS_POINTS_ and str(event.user_id) == '30806644':
                table.resetAllUsersInfo()
                write_message(event.user_id, 'Таблица полностью обновлена!')
            elif isDivTwo(command) > 0:
                a = command.split()
                if a[1].isdigit():
                    if table.isEnoughtForBet(event.user_id, a[1]) < 1:
                        write_message(event.user_id, 'У вас слишком мало баллов или '
                                                     'ваша ставка слишком маленькая (минимальная ставка 10 sp).')
                        continue
                    table.setSpentPointsWithVkId(event.user_id, a[1])
                    goods.tryToAddDivTwoBet(table.getHandleWithVkId(event.user_id), a[1])
                    write_message(event.user_id, 'Ваша ставка принята!')
                elif a[1].lower() == 'cancel':
                    goods.tryToCancelDivTwoBet(table.getHandleWithVkId(event.user_id))
                    write_message(event.user_id, 'Ваша ставка на проведение контеста '
                                                 'второго дивизиона успешно аннулирована.')
                else:
                    write_message(event.user_id, 'У команды div2 нет такого параметра!')
            elif command in constant.HELLO_:
                write_message(event.user_id, 'Добрый день! Рад тебя видеть, друг!')
            elif command in constant.WHO_RESPECT_THE_BEES:
                write_message(event.user_id, 'кто к ним не пристает,\n того они не жалят,\n тому приносят мёд!')
            elif str(event.user_id) == '30806644' and command in constant.CONDUCT_DIV2_:
                if goods.getSumOfDivTwoBets() >= goods.getDivTwoCost():
                    write_message(event.user_id, 'Контест готов к проведению.')
                    text = 'В следующем контесте принимают участие: ' + listToStr(goods.getDivTwoParty())
                    vk_api.VkApi(token=constant.accecc_token).method('board.addTopic', {
                        'group_id': '189233231',
                        'title': 'Проведение контеста div2',
                        'text': text,
                        'from_group': 1,
                        'attachments': []})
                else:
                    write_message(event.user_id, 'Собрано недостаточно средств.')

            else:
                if (event.user_id == '413059663'):
                    write_message(event.user_id, 'Хуй будешь?')
                else:
                    write_message(event.user_id, 'Я не понимаю вас :-(')
            continue

main()