from telebot import types


markup_next_question = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton('Показать вопрос')
# btn2 = types.KeyboardButton('Сколько вопросов осталось?')
# btn3 = types.KeyboardButton('Завершить игру')
markup_next_question.add(btn1)

markup_hideBoard = types.ReplyKeyboardRemove()

# markup1 = types.InlineKeyboardMarkup()
# markup1.add(types.InlineKeyboardButton("Да", callback_data='yes'))
# markup1.add(types.InlineKeyboardButton("Нет", callback_data='no'))
