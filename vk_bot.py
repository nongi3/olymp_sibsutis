# coding=utf-8
import json
import random
import urllib.request
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType

import cf_api
import constants
import dist_vic
import secret_constants
import table
import ddt

vk_session = vk_api.VkApi(token=secret_constants.token)
# vk_session = vk_api.VkApi(login='#', password='#', token=secret_constants.token, scope='wall, messages')

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


def writeMessage(user_id, msg):
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


def is_correct_rating(rating):
    return 500 <= rating <= 3000 and rating % 100 == 0


def isCompMath(event, command):
    a = command.split()
    if len(a) < 2 or a[0] != 'вычмат':
        return False
    if a[1] in constants.GET_EXEMPTED_:
        info = ddt.getExempted(table.getHandleWithVkId(event.user_id))
        if 'Error' in info:
            return True
        writeMessage(event.user_id, 'Задачи на динамику: ' + info['dinamic'] + '/6' +
                     (' - выполнено;' if int(info['dinamic']) >= 6 else ';'))
        writeMessage(event.user_id, 'Задачи на геометрию: ' + info['geometry'] + '/12' +
                     (' - выполнено;' if int(info['geometry']) >= 12 else ';'))
        writeMessage(event.user_id, 'Задачи на графы: ' + info['graph'] + '/3' +
                     (' - выполнено;' if int(info['graph']) >= 3 else ';'))
        writeMessage(event.user_id, 'Участий в контестах: ' + info['contests'] + '/13' +
                     (' - выполнено.' if int(info['contests']) >= 13 else '.'))
        if int(info['dinamic']) >= 6 and int(info['geometry']) >= 12 and int(info['graph']) >= 3 \
                and int(info['contests']) >= 13:
            writeMessage(event.user_id, 'Вы сделали достаточно для автомата!')
        return True
    return False


def help_text(event):
    writeMessage(event.user_id, 'Список доступных вам команд:\n' +
                 'лидеры - получение топ 10;\n' +
                 'пинг - позвать на помощь Бога;\n' +
                 'рейтинг - узнать текущую позицию в рейтинге;\n' +
                 'кто пчелок уважает - узнать истину;\n' +
                 'привет - чтобы быть вежливым;\n' +
                 'синхра - чтобы начать регистрацию;\n' +
                 'обнови меня - чтобы обновить свой рейтинг;\n' +
                 'баланс - текущее количество баллов;\n + '
                 'дай_задачу - самая сдаваемая задача среди участников программы...\n' +
                 'дай_задачу rating - для получения задачи определенного рейтинга,\n'
                 'количество_сданных_задач rating - получение количества уникальных верных решений для рейтинга,\n'
                 'количество_баллов_за_рейтинг rating - баллы за задачу с определенным рейтингом,\n'
                 'количество_сданных_задач_за number_of_days - количество задач за последние n дней,\n'
                 'ранг - указывает ваш текущий уровень доступа в боте,\n'
                 'повышение - требования для достижения следующего уровня')


def listToStr(values):
    res = ''
    for i in range(0, len(values)):
        res += str(values[i])
        if i + 1 < len(values):
            res += ', '
    return res


def printLeaders(event):
    leaders = table.getLeaders()
    writeMessage(event.user_id, 'Десятка лидеров:')
    for i in range(0, 10):
        writeMessage(event.user_id, str(i + 1) + ') ' + leaders[i][constants.TABLE_COLUMN_HANDLE_] + ' - ' +
                     leaders[i][constants.TABLE_COLUMN_PROBLEMSET_])


def printCompLeaders(event, leaders):
    writeMessage(event.user_id, 'Десятка лидеров соревнования:')
    for i in range(0, 10):
        writeMessage(event.user_id, str(i + 1) + ') ' + leaders[i][constants.TABLE_COLUMN_HANDLE_] + ' - ' +
                     leaders[i][constants.TABLE_COLUMN_COMP_])


def isBinding(event):
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user and \
            event.user_id in sync_list:
        handle = event.text.lower()
        try:
            request_url = 'http://codeforces.com/api/user.info?handles=' + handle
            response = urllib.request.urlopen(request_url)
            res = json.loads(response.read())
        except Exception:
            writeMessage(event.user_id, 'Что-то пошло не так... Возможно вы ввели неверный ник или ваш профиль на '
                                        'кодфорсе закрыт')
            return True
        if 'result' not in res:
            writeMessage(event.user_id, 'Возникла ошибка при получении данных от cf API')
            return True
        if len(res['result']) < 1:
            writeMessage(event.user_id, 'Возникла ошибка при получении данных от cf API')
            return True
        if 'vkId' not in res['result'][0]:
            writeMessage(event.user_id, 'Возникла ошибка при получении данных от cf API')
            return True
        vk_id_from_cf = cf_api.getVkIdFromCodeforces(handle)
        if vk_id_from_cf == 'Error':
            writeMessage(event.user_id, 'Возникла ошибка при обращении к cf api. Попробуйте позже!')
            return True
        if str(event.user_id) != str(vk_id_from_cf):
            writeMessage(event.user_id, 'Страница вк в профиле с указанным хэндлом отличается от вашей!')
            return True
        if table.isUserAlreadyExist(event.user_id):
            writeMessage(event.user_id, 'Вы уже зарегистрированы в системе! Повторное подтверрждение не требуется!')
            return True
        table.addNewUser(handle, event.user_id)
        writeMessage(event.user_id, 'Отлично, вы прошли проверку! Сейчас внесу вас в таблицу!')
        sync_list.remove(event.user_id)
        return True
    return False


def isSyncCommand(event, command):
    if command not in constants.SYNC_:
        return False
    if table.isUserAlreadyExist(event.user_id):
        writeMessage(event.user_id, 'Вы уже зарегистрированы в системе! Повторное подтверрждение не требуется!')
        return True
    if event.user_id in sync_list:
        writeMessage(event.user_id, 'Жду с нетерпением вашего хэндла, чтобы подтвердить вступление'
                                    ' в наши ряды')
        return True
    writeMessage(event.user_id, 'Введите ваш хэндл на codeforces для '
                                'добавления вас в таблицу и синхронизации с аккаунтом vk')
    sync_list.append(event.user_id)
    return True


def isUserLogin(user_id):
    if table.getHandleWithVkId(user_id) == 'None':
        writeMessage(user_id, 'Пройдите регистрацию, пожалуйста!\n Для начала введите "sync" (без ковычек)')
        return False
    return True


def isExit(event, command):
    if command in constants.EXIT_COMMANDS_:
        writeMessage(event.user_id, 'Пока :-D')
        exit()


def isGood(event, command):
    if command in constants.GOOD_WORDS_:
        writeMessage(event.user_id, 'Какой вы клевый! Уважаю!')
        return True
    return False


def isBad(event, command):
    if command in constants.bad_words:
        writeMessage(event.user_id, 'Сейчас обидно было :-(')
        return True
    return False


def isBalance(event, command):
    if command in constants.balance:
        points = table.getPointsWithVkId(event.user_id)
        if points < 0:
            writeMessage(event.user_id, 'Не удалось получить данные о вашем счете!')
        else:
            writeMessage(event.user_id, 'У вас на счету: ' + str(points) + ' баллов.')
        return True
    return False


def isPosition(event, command):
    if command in constants.POSITION_:
        position = table.getPositionWithVkId(event.user_id)
        if position < 0:
            writeMessage(event.user_id, 'Не удалось получить данные о вас!')
        else:
            writeMessage(event.user_id, 'Вы находитесь на ' + str(position) + ' месте.')
        return True
    return False


def isLeaders(event, command):
    if command in constants.LEADERS_:
        printLeaders(event)
        return True
    return False


def isReset(event, command):
    if command in constants.RESET_ONE_USER_POINTS_:
        if not table.resetPointsWithVkId(event.user_id):
            writeMessage(event.user_id, 'Данные о вас не найдены в таблице!')
            return True
        if not table.resetGymPointsWithVkId(event.user_id):
            writeMessage(event.user_id, 'Данные о вас не найдены в таблице!')
            return True
        writeMessage(event.user_id, 'Данные успешно обновлены!')
        points = table.getPointsWithVkId(event.user_id)
        writeMessage(event.user_id, 'У вас на счету: ' + str(points) + ' баллов.')
        position = table.getPositionWithVkId(event.user_id)
        writeMessage(event.user_id, 'Вы находитесь на ' + str(position) + ' месте.')
        return True
    elif command in constants.RESET_ALL_USERS_POINTS_:
        if str(event.user_id) not in constants.ADMIN_VK_ID_:
            writeMessage(event.user_id, 'Вам не доступна эта команда!')
            return True
        writeMessage(event.user_id, 'Обновление таблицы может занять некоторое время!')
        table.resetAllUsersInfo()
        writeMessage(event.user_id, 'Таблица полностью обновлена!')
        return True
    elif command in constants.RESET_LEADERS_:
        leaders = table.getLeaders()
        is_leader = False
        for leader in leaders:
            if leader[constants.TABLE_COLUMN_VK_ID_] == str(event.user_id):
                is_leader = True
                break
        if not is_leader:
            writeMessage(event.user_id, 'Эта команда доступна только действующим лидерам!')
            return True
        for leader in leaders:
            table.resetPointsWithVkId(leader[constants.TABLE_COLUMN_VK_ID_])
        writeMessage(event.user_id, 'Первая десятка успешно обновлена!')
        printLeaders(event)
        return True
    return False


def isGreeting(event, command):
    if command in constants.HELLO_:
        writeMessage(event.user_id, 'Добрый день! Рад тебя видеть, друг!')
        return True
    return False


def isRespect(event, command):
    if command in constants.WHO_RESPECT_THE_BEES:
        writeMessage(event.user_id, 'кто к ним не пристает,\n того они не жалят,\n тому приносят мёд!')
        return True
    return False


def isPing(event, command):
    if command in constants.PING_:
        writeMessage('30806644', 'Какой-то петуч нуждается в помощи. Ссылка: vk.com/id' + str(event.user_id))
        writeMessage(event.user_id, 'Ваша молитва услышана!')
        return True
    return False


def isHelp(event, command):
    if command in constants.HELP_:
        help_text(event)
        return True
    return False


def isCorrectEvent(event):
    return event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user


def isChangeHeader(event, command):
    if command in constants.RESET_TABLE_HEADER_:
        table.changeHeader()
        writeMessage(event.user_id, 'Заголовок таблицы обновлен')
        return True
    return False


def onDelete(event, command):
    if command == 'вот же петуч':
        tasks = ddt.specialForYou()
        if len(tasks) == 0:
            writeMessage(event.user_id, 'Все задачи петуча вами уже решены!')
            return True
        lst = []
        for rating in tasks:
            for name in tasks[rating]:
                lst.append("https://codeforces.com/problemset/problem/" +
                           str(tasks[rating][name]["contestId"]) + "/"
                           + str(tasks[rating][name]["index"]))
        if len(lst) == 0:
            writeMessage(event.user_id, 'Все задачи петуча вами уже решены!')
            return True
        ind = random.randint(0, len(lst) - 1)
        writeMessage(event.user_id, lst[ind])
        return True
    return False


def isFromAdmin(event):
    if str(event.user_id) in constants.ADMIN_VK_ID_:
        command = event.text.lower()
        isExit(event, command)
        if isChangeHeader(event, command):
            return True
        if onDelete(event, command):
            return True
        return False
    return False


def isTaskList(event, command):
    if command in constants.TRAINING_FIRST_FORMAT_:
        tasks = ddt.some_unsolved_tasks()
        for task in tasks:
            writeMessage(event.user_id, task)
        return True
    return False


def checkOnGiveTaskCommand(command):
    split_command = command.split()
    if len(split_command) < 1 or len(split_command) > 2 \
            or (str(split_command[0])) not in constants.GIVE_TASK_:
        return "Not give task command"
    if len(split_command) == 1:
        return "Correct 1"
    if split_command[1].isdigit() and 500 <= int(split_command[1]) <= 3000 and int(split_command[1]) % 100 == 0:
        return "Correct 2"
    return "Incorrect parameters"


def isGiveATask(event, command):
    check = checkOnGiveTaskCommand(command)
    if check == 'Not give task command':
        return False
    if check == 'Correct 1':
        writeMessage(event.user_id, "Ссылка на задачу: " +
                     ddt.theMostSolvedTaskFromUnsolved(table.getHandleWithVkId(event.user_id)))
    elif check == 'Correct 2':
        handle = table.getHandleWithVkId(event.user_id)
        rating = int(command.split()[1])
        if not cf_api.isStillRelevant(handle, rating):
            writeMessage(event.user_id, 'Задача с таким рейтингом больше не принесет вам баллов! B-)')
            return True
        url = cf_api.getTaskWithTagAndRating(handle, '', rating)
        if 'Error' in url:
            writeMessage(event.user_id, 'Не удалось получить задачу для вас, извините :-(')
            return True
        writeMessage(event.user_id, "Ссылка на задачу: " + url)
    else:
        writeMessage(event.user_id, 'Вы ввели неверные параметры!')
    return True


def isActiveUser(event):
    handle = table.getHandleWithVkId(event.user_id)
    cf_rating = cf_api.get_codeforces_rating(handle)
    table_rating = table.getPointsWithVkId(event.user_id)
    count_of_accept = cf_api.get_count_of_solved_tasks_for_some_days(handle, 30)
    return int(cf_rating) >= 1400 or int(table_rating) >= 1000 or int(count_of_accept) >= 60


def isExpert(event):
    handle = table.getHandleWithVkId(event.user_id)
    cf_rating = cf_api.get_codeforces_rating(handle)
    table_rating = table.getPointsWithVkId(event.user_id)
    count_of_accept = cf_api.get_count_of_solved_tasks_for_some_days(handle, 30)
    return int(cf_rating) >= 1600 or int(table_rating) >= 2000 or int(count_of_accept) >= 100


def isChampion(event):
    handle = table.getHandleWithVkId(event.user_id)
    cf_rating = cf_api.get_codeforces_rating(handle)
    table_rating = table.getPointsWithVkId(event.user_id)
    count_of_accept = cf_api.get_count_of_solved_tasks_for_some_days(handle, 30)
    return int(cf_rating) >= 1900 or int(table_rating) >= 5000 or int(count_of_accept) >= 150 or \
        handle in constants.VIP_USERS_


def isRank(event, command):
    if command in constants.RANK_:
        if isChampion(event):
            writeMessage(event.user_id, table.getHandleWithVkId(event.user_id) + ' находится в ранге чемпиона!')
        elif isExpert(event):
            writeMessage(event.user_id, table.getHandleWithVkId(event.user_id) + ' находится в ранге эксперта!')
        elif isActiveUser(event):
            writeMessage(event.user_id, table.getHandleWithVkId(event.user_id) + ' находится в ранге продвинутого!')
        elif isUserLogin(event.user_id):
            writeMessage(event.user_id, table.getHandleWithVkId(event.user_id) + ' находится в ранге новичка!')
        else:
            writeMessage(event.user_id, table.getHandleWithVkId(event.user_id) + ' находится в ранге гостя!')
        return True
    return False


def checkOnCountOfSolvedTasksCommand(command):
    words = command.split()
    if len(words) != 2:
        return False
    if not words[1].isdigit():
        return False
    rating = int(words[1])
    return words[0] in constants.COUNT_OF_SOLVED_TASKS_ and is_correct_rating(rating)


def isCountOfSolvedTasks(event, command):
    if checkOnCountOfSolvedTasksCommand(command):
        handle = table.getHandleWithVkId(event.user_id)
        rating = command.split()[1]
        count_of_solved_tasks = cf_api.countOfTasksWithRating(handle, rating)
        writeMessage(event.user_id, 'Вы решили ' + str(count_of_solved_tasks) + ' задач с рейтингом ' + str(rating))
        return True
    return False


def checkOnCountOfPointsWithRating(command):
    split_command = command.split()
    if len(split_command) != 2 or not split_command[1].isdigit():
        return False
    rating = int(split_command[1])
    return split_command[0] in constants.COUNT_OF_POINTS_FOR_SOME_RATING_ and is_correct_rating(rating)


def isCountOfPointsWithRating(event, command):
    if checkOnCountOfPointsWithRating(command):
        handle = table.getHandleWithVkId(event.user_id)
        rating = int(command.split()[1])
        count_of_points = cf_api.countOfPointsForATaskWithRating(handle, rating)
        writeMessage(event.user_id, handle + ' получит ' + str(count_of_points) + ' баллов за задачу с рейтингом '
                     + str(rating))
        return True
    return False


def checkOnCountOfSolvedTasksFor(command):
    split_command = command.split()
    if len(split_command) != 2 or not split_command[1].isdigit():
        return False
    return split_command[0] in constants.COUNT_OF_SOLVED_TASKS_FOR_


def isCountOfSolvedTasksFor(event, command):
    if checkOnCountOfSolvedTasksFor(command):
        handle = table.getHandleWithVkId(event.user_id)
        count_of_days = int(command.split()[1])
        count_of_solved_tasks = cf_api.get_count_of_solved_tasks_for_some_days(handle, count_of_days)
        writeMessage(event.user_id, handle + ' решил ' + str(count_of_solved_tasks) + ' задач за последние ' +
                     str(count_of_days) + ' дней.')
        return True
    return False


def isUpgrade(event, command):
    if command in constants.UPGRADE_:
        handle = table.getHandleWithVkId(event.user_id)
        cf_rating = int(cf_api.get_codeforces_rating(handle))
        table_rating = table.getPointsWithVkId(event.user_id)
        count_of_accept = cf_api.get_count_of_solved_tasks_for_some_days(handle, 30)
        if isChampion(event):
            writeMessage(event.user_id, 'Вы на вершине и расти больше некуда!')
        elif isExpert(event):
            writeMessage(event.user_id, 'До ранга чемпион вам осталось:\n' +
                         str(1900 - cf_rating) + ' рейтинга на кодфорсе\n' +
                         str(5000 - table_rating) + ' рейтинга в таблице\n' +
                         'или ' + str(150 - count_of_accept) + ' задач')
            writeMessage(event.user_id, 'Обращаю ваше внимание, что количество задач рассматривается '
                                        'за последние 30 дней. Это значит, что это число может уменьшаться.')
        elif isActiveUser(event):
            writeMessage(event.user_id, 'До ранга эксперт вам осталось:\n' +
                         str(1600 - cf_rating) + ' рейтинга на кодфорсе\n' +
                         str(2000 - table_rating) + ' рейтинга в таблице\n' +
                         'или ' + str(100 - count_of_accept) + ' задач')
            writeMessage(event.user_id, 'Обращаю ваше внимание, что количество задач рассматривается '
                                        'за последние 30 дней. Это значит, что это число может уменьшаться.')
        else:
            writeMessage(event.user_id, 'До ранга продвинутый вам осталось:\n' +
                         str(1400 - cf_rating) + ' рейтинга на кодфорсе\n' +
                         str(1000 - table_rating) + ' рейтинга в таблице\n' +
                         'или ' + str(60 - count_of_accept) + ' задач')
            writeMessage(event.user_id, 'Обращаю ваше внимание, что количество задач рассматривается '
                                        'за последние 30 дней. Это значит, что это число может уменьшаться.')
        return True
    return False


def isDist(event, command):
    split_command = command.split()
    if len(split_command) != 5:
        return False
    if split_command[0] not in constants.DIST_:
        return False
    for i in range(1, 3):
        if not split_command[i].isdigit():
            return False
    dist_vic.setLab(int(split_command[2]), int(split_command[3]), split_command[1], split_command[4])
    writeMessage(event.user_id, 'Данные успешно записаны в таблицу!')
    return True


def isFromUser(event):
    command = event.text.lower()
    if isDist(event, event.text):
        return True
    if isGood(event, command):
        return True
    if isBad(event, command):
        return True
    if isGreeting(event, command):
        return True
    if isRespect(event, command):
        return True
    if isHelp(event, command):
        return True
    if isCompMath(event, command):
        return True
    if isSyncCommand(event, command):
        return True
    if not isUserLogin(event.user_id):
        return True
    if isRank(event, command):
        return True
    # выше функции для гостя
    if isBalance(event, command):
        return True
    if isPosition(event, command):
        return True
    if isLeaders(event, command):
        return True
    if isCountOfSolvedTasksFor(event, command):
        return True
    if isUpgrade(event, command):
        return True
    # выше функции новичка
    if not isActiveUser(event):
        writeMessage(event.user_id, 'Сдавайте больше задач, чтобы попасть в ряды тру кодеров!')
        return False
    if isCountOfPointsWithRating(event, command):
        return True
    if isCountOfSolvedTasks(event, command):
        return True
    if isGiveATask(event, command):
        return True
    if isReset(event, command):
        return True
    # выше функции продвинутого
    if not isExpert(event):
        return False
    if isPing(event, command):
        return True
    if isTaskList(event, command):
        return True
    # выше функции эксперта
    if not isChampion(event):
        return False
    return False


def main():
    for event in longpoll.listen():
        if not isCorrectEvent(event):
            continue
        if isBinding(event):
            continue
        if isFromAdmin(event):
            continue
        if isFromUser(event):
            continue
        help_text(event)


main()

# vk_session.auth()
# vk_session.method('messages.send', {'user_id': 30806644, 'message': 'msg', 'random_id': 12415215})
# print(vk_session.method('wall.get', {'owner_id': -189233231, 'count': 1}))
