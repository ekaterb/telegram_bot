import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes, CallbackQueryHandler

from users import UserHandler
from forecast_requester import WeaterHandler, get_forecast


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    # TODO button insted of /start
    # TODO create meny with choose_city, subscr/unsubs buttons
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"Hi {update.message.chat.first_name}! I'm ForeCat, nice to meet you!\n"
                                        "Please choose your city that I could sent you the data"
                                        "use /choose_city command")


async def choose_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton('Barcelona', callback_data='Barcelona')],  #  TODO get cities from config
                [InlineKeyboardButton('Amsterdam', callback_data='Amsterdam')]]
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Please choose your city",
                                   reply_markup=InlineKeyboardMarkup(keyboard))


async def handle_callback_query(update, context):
    # TODO add functional
    await context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Great! Let me a sec to check the weather in ' + update.callback_query.data)


# TODO add subscribtion functional
# async def callback_auto_message(context, chat_id, forecast):
#     await context.bot.send_message(chat_id=chat_id, text=forecast)
#
#
# async def start_auto_messaging(update, context, forecast):
#     chat_id = update.message.chat_id
#     await context.job_queue.run_repeating(callback_auto_message(chat_id, forecast), 10, context=chat_id, name=str(chat_id))
#     # await context.job_queue.run_once(callback_auto_message, 3600, context=chat_id)
#     # await context.job_queue.run_daily(callback_auto_message, time=datetime.time(hour=9, minute=22), days=(0, 1, 2, 3, 4, 5, 6), context=chat_id)
#
#
#await def stop_notify(update, context):
#     chat_id = update.message.chat_id
#     await context.bot.send_message(chat_id=chat_id, text='Stopping automatic messages!')
#     job = context.job_queue.get_jobs_by_name(str(chat_id))
#     job[0].schedule_removal()


if __name__ == '__main__':
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    bot = ApplicationBuilder().token(BOT_TOKEN).build()
    bot.add_handler(CommandHandler('start', start))
    bot.add_handler(CommandHandler('choose_city', choose_city))
    bot.add_handler(CallbackQueryHandler(handle_callback_query, pattern='.*'))

    user = UserHandler(Update.message.chat_id)
    if not user.check_for_user():
        user.add_user()  # why I store all users who clicked /start b?
    city = user.get_users_city()
    subscription = user.get_users_subscription()

    bot.run_polling()
