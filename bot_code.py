from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import InputFile



BOT_TOKEN = '7023769811:AAFGbBOopl1nkcZ2CkHXOomccDQ51eEeOsU'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Данные о пользователе и флаги для их изменения
user = {'writename': False,
        'writephone': False,
        'anymessage': False,
        'endregistration': False,
        'fullname': '',
        'phonenumber': ''}



# Срабатывает на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    username = message.from_user.username
    await message.answer(F'Привет, {username}!\nДобро пожаловать в компанию DamnIT')
    await message.answer('Напишите своё ФИО')
    user['writename'] = True


button_accept = KeyboardButton(text='Ознакомился')

accept_kb =  ReplyKeyboardMarkup(keyboard=[[button_accept]], resize_keyboard=True, one_time_keyboard=True)

        


# Принимает любое сообщение. Сначала запрашивет ФИО, затем номер телефона, затем скидывает общие положения. Последующие сообщения передают списибо за регистрацию
@dp.message()
async def send_echo(message: Message):
    if user['writename']:
        catch_number = False
        for i in message.text:
            if not( ord('я')>=ord(i)>=ord('а')  or ord('Я')>=ord(i)>=ord('А') or i==' '):
                catch_number = True
        if (catch_number and len(str(message.text)))>0:
            await message.answer("Неверно написано ФИО. Напишите ещё раз")
        else:
            user['writename'] = False
            user['writephone'] = True
            user['fullname'] = str(message.text)
            await message.answer('Укажите ваш номер телефона')


    elif user['writephone']:
        catch_letter = False
        if message.text[0] != '7':
            catch_letter = True
        for i in message.text:
            if not( ord('9')>=ord(i)>=ord('0') or i==' '):
                catch_letter = True
        if (catch_letter or len(str(message.text)) != 11):
            await message.answer("Неверно написан номер телефона. Напишите ещё раз")
        else:
            user['writephone'] = False
            user['anymessage'] = True
            user['phonenumber'] = str(message.text)
            await message.answer('Напишите любой комментарий')


    elif user['anymessage']:
        await message.answer(

            reply_markup=accept_kb
        )
        await message.answer_photo(InputFile('Rules.pdf'))
    else:
        await message.answer('Спасибо за успешную регистрацию')
    
        

# Сраабатывает на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    fullname = user['fullname']
    phonenumber = user['phonenumber']
    await message.answer(
        'Этот бот создан для регистрации в компании DamnIT\n'
        'Ваши введённые данные:\n'
        F'ФИО: {fullname}\n'
        F'Номер телефона: {phonenumber}'
    )


if __name__ == '__main__':
    dp.run_polling(bot)