import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("8405278693:AAFISKWFDXnF9GrGm5PFBRQqFU1jmkTo4f0")  # Токен хранится в переменных Railway
ADMIN_CHAT_ID = int(os.getenv("6054782646"))  # Твой chat_id для уведомлений

# Приветственное сообщение
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Здесь можно сообщить о громких звуках, пролётах БПЛА или ракет.\n"
        "✍️ Просто напиши, что ты слышал или видел."
    )

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text or ""
    caption = update.message.caption or ""
    message_text = text if text else caption

    # Пересылаем сообщение админу
    if update.message.photo:
        await context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=update.message.photo[-1].file_id, caption=f"📩 От {user.first_name} (@{user.username}):\n{message_text}")
    else:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"📩 От {user.first_name} (@{user.username}):\n{message_text}")

    # Подтверждаем пользователю
    await update.message.reply_text("✅ Сообщение получено! Спасибо за информацию.")

# Запуск бота
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, handle_message))

app.run_polling()