import logging
import telegram


class TgLogsHandler(logging.Handler):

    def __init__(self, token, chat_id):
        super().__init__()
        self.bot = telegram.Bot(token=token)
        self.admin_chat_id = chat_id

    def emit(self, record):
        self.bot.send_message(
                         chat_id=self.admin_chat_id,
                         text=self.format(record)
		)