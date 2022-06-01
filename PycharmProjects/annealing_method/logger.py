import logging
import traceback


CHECKPOINT_FILE = "logs/checkpoint.txt"


class CustomLogger:

    def __init__(self, log_name: str, log_file: str):
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.INFO)
        self.file_handler = logging.FileHandler(log_file, encoding='utf-8')

        self.formater = logging.Formatter('%(asctime)s : [%(levelname)s] : %(message)s')
        self.file_handler.setFormatter(self.formater)
        self.logger.addHandler(self.file_handler)
        self.checkpoint_file = CHECKPOINT_FILE

    def error_mess(self, message: str = "", line_number: int = 0):
        err_formater = logging.Formatter('%(asctime)s : [%(levelname)s][LINE ' + str(line_number) + '] : %(message)s')
        self.file_handler.setFormatter(err_formater)
        if message:
            self.logger.error(message)
        self.logger.error(traceback.format_exc())
        self.logger.addHandler(self.file_handler)
        self.file_handler.setFormatter(self.formater)
        self.logger.addHandler(self.file_handler)
        raise RuntimeError

    def info_mess(self, message: str):
        self.logger.info(message)

    def warning_mes(self, message: str):
        self.logger.warning(message)

    def multiple_info(self, lines: list):
        for line in lines:
            self.logger.info(line)

    # def make_checkpoint(self):
    #     with open(self.checkpoint_file, "w"):
    #         pass
    #
    # def load_from_checkpoint(self) -> list:
    #     with open(self.checkpoint_file, "r"):
    #         pass

