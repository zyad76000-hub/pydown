import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
    CommandHandler
)

from downloader import download_video
from keyboards import quality_keyboard
import config

# حفظ روابط كل مستخدم مؤقتًا
user_links = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 مرحبًا! أرسل رابط الفيديو، وسأعطيك خيارات الجودة أو الصوت."
    )

# استقبال رابط الفيديو
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    user_links[update.message.from_user.id] = url
    await update.message.reply_text(
        "🎥 اختر الجودة أو تنزيل الصوت:",
        reply_markup=quality_keyboard()
    )

# التعامل مع اختيار الجودة أو الصوت
async def quality_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    quality = query.data
    user_id = query.from_user.id
    url = user_links.get(user_id)

    if not url:
        await query.edit_message_text("❌ لم يتم العثور على رابط الفيديو.")
        return

    await query.edit_message_text("📥 جاري تنزيل الفيديو...")

    try:
        file = download_video(url, quality, config.DOWNLOAD_FOLDER)
        size = os.path.getsize(file)

        if size < config.MAX_TELEGRAM_FILE:
            if quality == "audio":
                await context.bot.send_audio(
                    chat_id=query.message.chat.id,
                    audio=open(file, "rb")
                )
            else:
                await context.bot.send_document(
                    chat_id=query.message.chat.id,
                    document=open(file, "rb")
                )
        else:
            await context.bot.send_message(
                chat_id=query.message.chat.id,
                text="⚠️ الملف كبير جدًا، لا يمكن إرساله مباشرة."
            )

        os.remove(file)

    except Exception as e:
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=f"❌ حدث خطأ أثناء التنزيل.\n{e}"
        )

def main():
    app = ApplicationBuilder().token(config.TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.add_handler(CallbackQueryHandler(quality_select))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()