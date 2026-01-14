# В Colab в отдельной ячейке: !pip install pyTelegramBotAPI

from telebot import TeleBot, types
import json
import os
import html

bot = TeleBot(token='Вставить_свой_токен', parse_mode='html')  # создание бота

@bot.message_handler(commands=['start'])
def start_command_handler(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Привет! Я умею проверять JSON и форматировать его в красивый текст\nВведи JSON в виде строки:',
    )


@bot.message_handler()
def message_handler(message: types.Message):
    try:
        payload = json.loads(message.text)
    except json.JSONDecodeError as ex:
        bot.send_message(
            chat_id=message.chat.id,
            text=f'При обработке произошла ошибка:\n<code>{html.escape(str(ex))}</code>'
        )
        return

    pretty = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)

    # сохраняем JSON в файл
    filename = 'pretty_json.json'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(pretty)

    # создаем кнопку "Преобразовать в файл"
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Преобразовать в файл", callback_data='send_file')
    markup.add(button)

    # ОДИН вызов — отправляем отформатированный JSON и добавляем кнопку
    bot.send_message(
        chat_id=message.chat.id,
        text=f'JSON:\n<pre>{html.escape(pretty)}</pre>',
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == 'send_file')
def callback_send_file(call: types.CallbackQuery):
    filename = 'formatted_json.json'
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            bot.send_document(chat_id=call.message.chat.id, document=f)
        try:
            os.remove(filename)
        except OSError:
            pass
    else:
        bot.answer_callback_query(call.id, "Файл не найден")


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()
