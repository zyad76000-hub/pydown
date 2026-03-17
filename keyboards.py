from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def quality_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("360p", callback_data="360"),
            InlineKeyboardButton("720p", callback_data="720"),
            InlineKeyboardButton("1080p", callback_data="1080")
        ],
        [
            InlineKeyboardButton("🎵 Audio Only", callback_data="audio")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)