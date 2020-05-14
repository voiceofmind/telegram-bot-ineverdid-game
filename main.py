import telebot
import csv
from random import choice
from time import time
from keyboard_markup import *
import logging
from config import *


bot = telebot.TeleBot(TOKEN)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

users = {}


# Prepare questions list from CSV:
with open('questions_base.csv', mode='r') as file:
    reader = csv.reader(file, delimiter=';')
    questions_dict = {}
    for row in reader:
        questions_dict[row[0]] = row[1]


def authorize_new_user(current_user):
    users[current_user.id] = ({'username': current_user.username,
                               'first_name': current_user.first_name,
                               'last_name': current_user.last_name,
                               'language_code': current_user.language_code,
                               'questions_ids': [],
                               'has_active_game': False,
                               'last_access': int(time())
                               })
    logging.info(f'New user started the bot: {current_user.username} ({current_user.id}). '
                 f'Users in database: {len(users)}')


def is_new_user(user_id):
    for _ in users:
        if _ == user_id:
            return False  # user already exists
    return True


def user_start_game(user_id):
    users[user_id]['questions_ids'] = list(questions_dict.keys())
    users[user_id]['has_active_game'] = True


def user_finish_game(user_id, requested_by_user=False):
    users[user_id]['questions_ids'] = []
    users[user_id]['has_active_game'] = False
    if requested_by_user:
        logging.info(f'Existing user restarted the bot: {users[user_id]["username"]} ({user_id}). '
                     f'His game is reset (if any).')


def user_has_active_game(user_id):
    return users[user_id]['has_active_game']


def user_update_last_access(user_id):
    users[user_id]['last_access'] = int(time())


@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user

    if is_new_user(user.id):
        authorize_new_user(user)
    else:
        user_finish_game(user.id, requested_by_user=True)

    welcome_message = 'Что ж, играем! Я буду показывать случайные вопросы из своего списка. ' \
                      'Чтобы начать игру сначала, отправь команду /start'
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup_next_question)


@bot.message_handler(content_types=['text'])
def mess(message):
    current_user = message.from_user
    get_message_bot = message.text.strip().lower()

    if get_message_bot == 'показать вопрос':
        if is_new_user(current_user.id):
            authorize_new_user(current_user)
        show_next_question(message)


def show_next_question(message):
    user_id = message.from_user.id

    if not user_has_active_game(user_id):
        user_start_game(user_id)

    user_questions_ids = users[user_id]['questions_ids']

    if len(user_questions_ids) == 0:
        bot.send_message(message.chat.id, "Вопросы закончились... Команда /start начнет игру сначала.",
                         reply_markup=markup_hideBoard)
    else:
        current_question_number = choice(user_questions_ids)
        current_question = questions_dict[current_question_number]
        bot.send_message(message.chat.id, current_question)
        users[user_id]['questions_ids'].remove(current_question_number)
        user_update_last_access(user_id)
        logging.info(f'Question for {message.from_user.username} ({message.from_user.id}): "{current_question}" '
                     f'({len(user_questions_ids)} left)')


bot.polling(none_stop=True)
