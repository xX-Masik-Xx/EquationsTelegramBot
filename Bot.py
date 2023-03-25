import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def solve_equation_str(equation: str) -> str:
    lines = [equation]
    lines.append(normalize_answer(solve_quadratic_equation(equation)))
    return "\n".join(lines)

def normalize_answer(answers: tuple[float]) -> str:
    res = f"±{answers[0]}" if len(answers) >= 2 and answers[0] == -answers[1] and len(answers) == 2 else '; '.join(list(map(str, answers)))
    res = f"Ответ: {res};"
    return res

def solve_quadratic_equation(equation: str) -> tuple[int] | bool:
    from math import sqrt
    a,b,c = tuple(list(map(int,equation.replace("x^2", "").replace("x", "").replace(" + ", ";").split(";"))))
    discriminant = b**2 - 4*a*c
    x1, x2 = (-b + sqrt(discriminant))/(2*a), (-b - sqrt(discriminant))/(2*a)
    return (x1, x2) if x1 != x2 else tuple([x1])

with open("token.txt", "r") as token:
    bot = telebot.TeleBot(token.read())
    
#bot setup
keyboard = ReplyKeyboardMarkup(resize_keyboard=True,)
keyboard.add(KeyboardButton("Реши уравнение"))

@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Нажмите на кнопку \"Реши уравнение\"", reply_markup=keyboard)
    
@bot.message_handler(func=lambda s: 'Решить' in s.text)
def solve_equation(message):
    bot.send_message(message.chat.id, solve_equation_str(message.text))
    
@bot.message_handler(func=lambda s: 'Реши: ' in s.text)
def solve_equation(message):
    bot.send_message(message.chat.id, solve_equation_str(message.text.replace("Реши:", "")))
    
bot.infinity_polling()