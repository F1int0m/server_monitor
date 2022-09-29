from telegram.ext import Application, CommandHandler

import config
from core import telegram_handlers


def main():
    print('Start init')
    application = Application.builder().token(config.BOT_TOKEN).build()

    welcome_handler = CommandHandler(command=['start', 'help'], callback=telegram_handlers.start)
    monitoring_start_handler = CommandHandler(command='start_monitoring', callback=telegram_handlers.start_monitoring)
    monitoring_stop_handler = CommandHandler(command='stop_monitoring', callback=telegram_handlers.stop_monitoring)
    total_data_handler = CommandHandler(command='total', callback=telegram_handlers.total_network_load)

    application.add_handler(handler=welcome_handler)
    application.add_handler(handler=monitoring_start_handler)
    application.add_handler(handler=monitoring_stop_handler)
    application.add_handler(handler=total_data_handler)

    print('Init done')
    application.run_polling()


if __name__ == '__main__':
    main()
