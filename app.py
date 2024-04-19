import telebot
from config import currencies,TOKEN
from extentions import APIException,Convertor

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = ('Для начала работы с ботом введите команду в следующем формате:\n'
            '<ИМЯ ВАЛЮТЫ> <ИМЯ ВАЛЮТЫ В КОТОРУЮ СОВЕРШАЕТСЯ ПЕРЕВОД> <КОЛИЧЕСТВО ПЕРЕВОДИМОЙ ВАЛЮТЫ>\n'
            'Увидеть список всех доступных валют: /values')
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currencies.keys():
        text = '\n'.join((text,key,))
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Количество параметров не равно 3.')
        quote, base, amount = values
        conversion_rate = Convertor.get_price(quote,base,amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n'
                              f'{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n'
                              f'{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {round((conversion_rate * float(amount)), 5)}'
        bot.reply_to(message, text)


bot.infinity_polling()