from django.core.management.base import BaseCommand
from telegram import Bot
from django.conf import settings
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler
from telegram.ext import Filters, CommandHandler
from telegram.ext import Updater
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.request import Request
from telegram.ext import CallbackQueryHandler

import os

from polls.models import *

PORT = int(os.environ.get('PORT', 8000))

def start(update, context):
    chat_id = update.message.chat_id
    username = update.message.chat.username

    Profile.objects.update_or_create(
        external_id = chat_id,
        defaults ={
            'name': username,
        }
    )
    
    # cat_objs = Category.objects.order_by('id')[:4]
    # message = f''' '''


    # for cat_obj in cat_objs:
    #     message += f'''{cat_obj.category} \n'''

    if username != None:
        update.message.reply_text('Привет {}! Добро пожаловать в нашего бота с тестами '.format(username))
    elif username == None:
        update.message.reply_text('Привет друг без username! Добро пожаловать в нашего бота с тестами ')
    
    update.message.reply_text('Ваш ID {}!'.format(chat_id))
    # update.message.reply_text(f'''{message}''')
    update.message.reply_text(quest(), reply_markup=menu_keyboard())

########################################################################################

CALLBACK_BUTTON1_CATEGORY = "callback_button1_category"
CALLBACK_BUTTON2_RESULTS = "callback_button2_results"
CALLBACK_BUTTON_HIDE_KEYBOARD = "callback_button_hide"

CALLBACK_BUTTON3_CATEGORY1 = "callback_button_category_chosen_1"
CALLBACK_BUTTON4_CATEGORY2 = "callback_button_category_chosen_2"
CALLBACK_BUTTON5_CATEGORY3 = "callback_button_category_chosen_3"
CALLBACK_BUTTON6_CATEGORY4 = "callback_button_category_chosen_4"
CALLBACK_BUTTON7_CATEGORY_NEXT = "callback_button7_category_next"
CALLBACK_BUTTON7_CATEGORY_PREV = "callback_button7_category_prev"

CALLBACK_BUTTON_CATEGORY_MENU = "callback_button_category_menu"

# CALLBACK_BUTTON8_TEST1 = "callback_button8_test1"
# CALLBACK_BUTTON9_TEST2 = "callback_button9_test2"
# CALLBACK_BUTTON10_TEST3 = "callback_button10_test3"
# CALLBACK_BUTTON11_TEST4 = "callback_button11_test4"
# CALLBACK_BUTTON12_TEST_MORE = "callback_button12_test_more"


TITLES = {
    CALLBACK_BUTTON1_CATEGORY: "Категории",
    CALLBACK_BUTTON2_RESULTS: "Результаты",
    CALLBACK_BUTTON_HIDE_KEYBOARD: "Спрять клавиатуру",

    CALLBACK_BUTTON3_CATEGORY1: "null",
    CALLBACK_BUTTON4_CATEGORY2: "null",
    CALLBACK_BUTTON5_CATEGORY3: "null",
    CALLBACK_BUTTON6_CATEGORY4: "null",
    CALLBACK_BUTTON7_CATEGORY_NEXT: "Следующие 4 категории",
    CALLBACK_BUTTON7_CATEGORY_PREV: "Предыдущие 4 категории",

    CALLBACK_BUTTON_CATEGORY_MENU: "Вернуться в меню",

}

########################################################################################

def menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON1_CATEGORY], callback_data=CALLBACK_BUTTON1_CATEGORY),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON2_RESULTS], callback_data=CALLBACK_BUTTON2_RESULTS),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON_HIDE_KEYBOARD], callback_data=CALLBACK_BUTTON_HIDE_KEYBOARD),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def category_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON3_CATEGORY1], callback_data=CALLBACK_BUTTON3_CATEGORY1),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON4_CATEGORY2], callback_data=CALLBACK_BUTTON4_CATEGORY2),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON5_CATEGORY3], callback_data=CALLBACK_BUTTON5_CATEGORY3),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON6_CATEGORY4], callback_data=CALLBACK_BUTTON6_CATEGORY4),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON7_CATEGORY_NEXT], callback_data=CALLBACK_BUTTON7_CATEGORY_NEXT),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON7_CATEGORY_PREV], callback_data=CALLBACK_BUTTON7_CATEGORY_PREV),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON_CATEGORY_MENU], callback_data=CALLBACK_BUTTON_CATEGORY_MENU),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def keyboard_callback_handler(update, context):
    #обработчик кнопок
    query = update.callback_query
    data = query.data

    chat_id = update.effective_message.chat_id
    current_text = update.effective_message.text

    q = Category.objects.count()
    z = q//4+q%4
    i = 1

    if data == CALLBACK_BUTTON1_CATEGORY:
            # Показать следующий экран клавиатуры
            # (оставить тот же текст, но указать другой массив кнопок)
        # cat_objs = Category.objects.order_by('id')[:4]

        # for cat_obj in cat_objs:
        #     z.append(cat_obj)
        cat_objs = Category.objects.order_by('id')[((i-1)*4):4*i]

        TITLES[CALLBACK_BUTTON3_CATEGORY1] = cat_objs[0].category
        TITLES[CALLBACK_BUTTON4_CATEGORY2] = cat_objs[1].category
        TITLES[CALLBACK_BUTTON5_CATEGORY3] = cat_objs[2].category
        TITLES[CALLBACK_BUTTON6_CATEGORY4] = cat_objs[3].category

        query.edit_message_text(
            text = 'Выберите категорию, вы на странице номер' + ' ' + str(i) + ' из ' + str(z),
            reply_markup=category_keyboard(),
        )

    elif data == CALLBACK_BUTTON7_CATEGORY_NEXT:

        i += 1
        if q%4!=0:
            if int(z-i)>0:
                cat_objs = Category.objects.order_by('id')[((i-1)*4):4*i]
            else:
                cat_objs = Category.objects.order_by('id')[((i-1)*4):(((i-1)*4)+(q%4))]
        else:
            cat_objs = Category.objects.order_by('id')[((i-1)*4):4*i]

        TITLES[CALLBACK_BUTTON3_CATEGORY1] = cat_objs[0].category
        TITLES[CALLBACK_BUTTON4_CATEGORY2] = cat_objs[1].category
        TITLES[CALLBACK_BUTTON5_CATEGORY3] = cat_objs[2].category
        TITLES[CALLBACK_BUTTON6_CATEGORY4] = cat_objs[3].category

        query.edit_message_text(
            text = 'Выберите категорию, вы на странице номер' + ' ' + str(i) + ' из ' + str(z),
            reply_markup=category_keyboard(),
        )

    elif data == CALLBACK_BUTTON7_CATEGORY_NEXT:

        i -= 1 

        query.edit_message_text(
            text = 'Выберите категорию, вы на странице номер' + ' ' + str(i) + ' из ' + str(z),
            reply_markup=category_keyboard(),
        )

    elif data == CALLBACK_BUTTON_CATEGORY_MENU:
        query.edit_message_text(
            text = 'Вы вернулись обратно в меню. '+ quest(),
            reply_markup=menu_keyboard(),
        )


    elif i == 1:
            # Показать следующий экран клавиатуры
            # (оставить тот же текст, но указать другой массив кнопок)
        # cat_objs = Category.objects.order_by('id')[:4]

        # for cat_obj in cat_objs:
        #     z.append(cat_obj)

        cat_objs = Category.objects.order_by('id')[((i-1)*4):4*i]

        TITLES[CALLBACK_BUTTON3_CATEGORY1] = cat_objs[0].category
        TITLES[CALLBACK_BUTTON4_CATEGORY2] = cat_objs[1].category
        TITLES[CALLBACK_BUTTON5_CATEGORY3] = cat_objs[2].category
        TITLES[CALLBACK_BUTTON6_CATEGORY4] = cat_objs[3].category

        query.edit_message_text(
            text = 'Выберите категорию, вы на странице номер' + ' ' + str(i) + ' из ' + str(z),
            reply_markup=category_keyboard(),
        )



#----------------------------------------#
def quest():
    return 'Выберите дальнейшие действия, вы можете или найти тесты по категориям или посмотреть результаты своих пройденных тестов'

########################################################################################

class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
        )
        print(bot.get_me())

        updater = Updater(
            bot=bot,
            use_context=True,
        )
        
        start_command = CommandHandler('start', start)
        buttons_handler = CallbackQueryHandler(callback=keyboard_callback_handler)

        updater.dispatcher.add_handler(start_command)
        updater.dispatcher.add_handler(buttons_handler)

        updater.start_polling()



        # updater.start_webhook(
        #             listen='0.0.0.0',
        #             port=int(PORT),
        #             url_path=settings.TOKEN,
        #             webhook_url='https://1ca2-85-174-193-158.ngrok.io/' + settings.TOKEN,
        # )

        updater.idle()