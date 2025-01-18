import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Ваш токен бота
TOKEN = "8114342844:AAFPrriZHADGQxhAt-G4Khaur0131IejkNY"
# ID канала или группы (например, @username или ID)
CHANNEL_ID = "@AntiBoringProject"  # Или используйте ID канала, например, -1001234567890

# Список сайтов, которые бот будет открывать
WEBSITES = [
    "https://www.crazygames.com",
    "https://imgflip.com/memegenerator",
    "https://www.soundtrap.com",
    "https://www.autodraw.com",
    "https://www.xkcd.com",
    "https://www.boredbutton.com",
    "https://picrew.me/en/image_maker/644129",
    "https://www.playphrase.me",
    "https://slowroads.io",
    "https://emulatoronline.com/",
    "https://playback.fm/birthday-song",
    "https://checkboxrace.com",
    "https://thezen.zone",
    "https://ubg100.github.io/games.html",
    "https://jspaint.app",
    "https://mecabricks.com",
    "https://flashmuseum.org",
    "https://playcanv.as",
]

# Проверка, подписан ли пользователь на канал
async def is_user_subscribed(user_id: int) -> bool:
    try:
        # Используем метод getChatMember для проверки статуса пользователя
        chat_member = await application.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        # Если статус "left", пользователь не подписан
        return chat_member.status != "left"
    except Exception as e:
        print(f"Ошибка при проверке подписки: {e}")
        return False

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if await is_user_subscribed(user_id):
        # Создаем клавиатуру с кнопкой
        keyboard = [["🎲Открыть случайный сайт"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "Привет! Нажми кнопку ниже, чтобы открыть случайный сайт.",
            reply_markup=reply_markup,
        )
    else:
        await update.message.reply_text(
            "Пожалуйста, подпишитесь на наш канал, чтобы использовать бота:\n"
            f"{CHANNEL_ID}"
        )

# Обработка нажатия кнопки
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    text = update.message.text

    if text == "🎲 Открыть случайный сайт":
        if await is_user_subscribed(user_id):
            site = random.choice(WEBSITES)
            await update.message.reply_text(f"Вот случайный сайт: {site}")
        else:
            await update.message.reply_text(
                "Пожалуйста, подпишитесь на наш канал, чтобы использовать бота:\n"
                f"{CHANNEL_ID}"
            )

def main() -> None:
    global application
    # Создаем экземпляр бота
    application = Application.builder().token(TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
