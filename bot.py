import telebot
import robot

TOKEN = '1346716396:AAGuyz5kFdw62HlmuzeXP7vuAo34vbNkcbA'
bot = telebot.TeleBot(TOKEN)

# Цифровые выходы
keys = [telebot.types.InlineKeyboardButton('', callback_data='')]*8
# Выходы инструмента
buttons = [telebot.types.InlineKeyboardButton('', callback_data='')]*2
condition = robot.get_now_state()

# Функция генерирует клавиатуру, в зависимости от нужд:
def generateKeyboard(act, i = 0):
    newKeyboard = telebot.types.InlineKeyboardMarkup()
    # Clear - чистая клавитура
    if act == 'Clear':
        for i in range(8):
            keys[i] = telebot.types.InlineKeyboardButton(str(i + 1)+')⚪', callback_data=str(i))
            condition[i] = False
    # On/Off - включение/выключение iй кнопки
    if act == 'On':
        keys[i] = telebot.types.InlineKeyboardButton(str(i + 1)+')🔵', callback_data=str(i)+str(i))
        condition[i] = True
    if act == 'Off':
        keys[i] = telebot.types.InlineKeyboardButton(str(i + 1)+')⚪', callback_data=str(i))
        condition[i] = False
    # Now - текущее состояние кнопок
    if act == 'Now':
        value = robot.get_now_state()
        for i in range(8):
            if not value[i]:
                keys[i] = telebot.types.InlineKeyboardButton(str(i + 1) + ')⚪', callback_data=str(i))
                keys[i] = telebot.types.InlineKeyboardButton(str(i + 1) + ')🔵', callback_data=str(i) + str(i))
        pass
    # Back - возвращение в меню
    if act == 'Back':
        newKeyboard.row(
            telebot.types.InlineKeyboardButton('Состояния', callback_data='get-input'),
            telebot.types.InlineKeyboardButton('Задать выходы', callback_data='set-output'),
            telebot.types.InlineKeyboardButton('Инструмент', callback_data='set-tool-outputs')
        )
        return newKeyboard

    if act == 'Tool':
        value = robot.get_tool_outputs()
        for i in range(2):
            if value[i]:
                buttons[i] = telebot.types.InlineKeyboardButton(str(i + 1) + ')🔵', callback_data='t' + str(i) + str(i))
            else:
                buttons[i] = telebot.types.InlineKeyboardButton(str(i + 1) + ')⚪', callback_data='t' + str(i))
        newKeyboard.row(buttons[0], buttons[1])
        return newKeyboard

    if act == 'ToolOn':
        buttons[i] = telebot.types.InlineKeyboardButton(str(i + 1) + ')🔵', callback_data='t' + str(i) + str(i))
        robot.set_tool_output(i)
        newKeyboard.row(buttons[0], buttons[1])
        return newKeyboard

    if act == 'ToolOff':
        buttons[i] = telebot.types.InlineKeyboardButton(str(i + 1) + ')⚪', callback_data='t' + str(i))
        robot.set_tool_output(i)
        newKeyboard.row(buttons[0], buttons[1])
        return newKeyboard

    newKeyboard = telebot.types.InlineKeyboardMarkup()
    newKeyboard.row(
        keys[0], keys[1], keys[2], keys[3]
    )
    newKeyboard.row(
        keys[4], keys[5], keys[6], keys[7]
    )
    newKeyboard.row(
        telebot.types.InlineKeyboardButton('Очистить', callback_data='Clear'),
        telebot.types.InlineKeyboardButton('Обновить', callback_data='Update'),
        telebot.types.InlineKeyboardButton('Назад', callback_data='Back')
    )
    return newKeyboard


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Запустились', reply_markup=generateKeyboard('Back'))

@bot.callback_query_handler(func=lambda call: True)
def ans(call):
    # Состояния входов
    if call.data == 'get-input':
        ansver = bin(robot.get_input())
        bulb = ['0', '0', '0', '0', '0', '0', '0', '0', '0']

        i = len(ansver) - 1
        j = 8
        while ansver[i] != 'b':
            bulb[j] = ansver[i]
            j -= 1
            i -= 1

        for i in range(1, 9):
            send = str(i) + ') '
            if bulb[i] == '1':
                send += '🔵'
            elif bulb[i] == '0':
                send += '⚪'
            bot.send_message(call.message.chat.id, send)
    # Состояния выходов
    if call.data == 'set-output':
        bot.send_message(call.message.chat.id, 'Состояния: ', reply_markup=generateKeyboard('Now'))
    # Обработчик кнопки Назад
    if call.data == 'Back':
        bot.edit_message_text(text='Меню',chat_id=call.from_user.id, message_id=call.message.message_id)
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id,
                                      reply_markup=generateKeyboard('Back'))
    # Обновление клавиатуры
    if call.data == 'Update':
        try:
            bot.edit_message_reply_markup(call.from_user.id, call.message.message_id,
                                            reply_markup=generateKeyboard('Now'))
        except:
            bot.send_message(call.from_user.id, 'Состояния свежие')

    if call.data == 'set-tool-outputs':
        bot.send_message(call.from_user.id, 'Выходы инструмента', reply_markup=generateKeyboard('Tool'))

    for i in range(2):
        if call.data == 't' + str(i):
            bot.edit_message_reply_markup(call.from_user.id, call.message.message_id,
                                          reply_markup=generateKeyboard('ToolOff'))
        if call.data == 't' + str(i) + str(i):
            bot.edit_message_reply_markup(call.from_user.id, call.message.message_id,
                                          reply_markup=generateKeyboard('OnOff'))

    # Вся логика для кнопок цифровых выходов
    for i in range(8):
        if call.data == str(i):
            bot.edit_message_reply_markup(call.from_user.id, call.message.message_id,
                                          reply_markup=generateKeyboard('On',i))
            robot.set_output(i)
        if call.data == str(i)+str(i):
            bot.edit_message_reply_markup(call.from_user.id, call.message.message_id,
                                          reply_markup=generateKeyboard('Off', i))
            robot.set_output(i)
    # Обработчик конпки Очистить
    if call.data == 'Clear':
        try:
            bot.edit_message_reply_markup(call.from_user.id, call.message.message_id,
                                          reply_markup=generateKeyboard('Clear'))
            robot.set_output(-1)
        except:
            bot.send_message(call.from_user.id, 'Ничего не горит')

@bot.message_handler(content_types=['text'])
def send(message):
    bot.send_message(message.chat.id, 'Включён')

bot.polling(none_stop=True)
