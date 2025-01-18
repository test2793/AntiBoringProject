import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters

# Ваш токен бота
TOKEN = "токен бота"
# ID канала или группы (например, @username или ID)
CHANNEL_ID = "канал для подписки перед использованием бота"  # Или используйте ID канала, например, -1001234567890

# Список сайтов, которые бот будет открывать
WEBSITES = [
    "https://www.crazygames.com",
    "https://www.kongregate.com",
    "https://imgflip.com/memegenerator",
    "https://experiments.withgoogle.com",
    "https://www.soundtrap.com",
    "https://www.autodraw.com",
    "https://www.boredpanda.com",
    "https://www.thisissand.com",
    "https://www.xkcd.com",
    "https://www.randvid.com",
    "https://www.boredbutton.com",
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
        await update.message.reply_text("Привет! Используй команду /random_site, чтобы открыть случайный сайт.")
    else:
        await update.message.reply_text(
            "Пожалуйста, подпишитесь на наш канал, чтобы использовать бота:\n"
            f"{CHANNEL_ID}"
        )

# Команда /random_site
async def random_site(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
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

    # Регистрация команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("random_site", random_site))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()