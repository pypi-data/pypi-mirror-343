import logging
import os
from datetime import datetime
from colorlog import ColoredFormatter


class DailyFileHandler(logging.FileHandler):
    """一个日志处理程序，它每天创建一个新的日志文件。"""

    def __init__(self, dir_name, mode='a', encoding=None, delay=False):
        self.dir_name = dir_name
        self.mode = mode
        self.encoding = encoding
        self.delay = delay
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        filename = self.get_filename()
        super().__init__(filename, mode, encoding, delay)

    def get_filename(self):
        """根据当前日期生成日志文件名。"""
        date_str = datetime.now().strftime("%Y/%m/%d")
        log_dir = os.path.join(self.dir_name, date_str)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return os.path.join(log_dir, "log.log")

    def emit(self, record):
        """在写入日志记录之前，检查是否需要滚动文件。"""
        new_date = datetime.now().strftime("%Y-%m-%d")
        if new_date != self.current_date:
            self.current_date = new_date
            self.baseFilename = self.get_filename()
            self.stream = self._open()
        super().emit(record)


# def setup_logger():
#     """
#     设置日志记录器并返回它。日志文件按年/月/日的层级结构保存。
#     :return: 日志记录器。
#     """
#     logger = logging.getLogger('my_logger')
#     logger.setLevel(logging.INFO)
#
#     # 避免重复添加处理程序
#     if not logger.hasHandlers():
#         # 创建自定义的日志处理程序（写入文件）
#         file_handler = DailyFileHandler("./logfile", encoding="utf-8")
#         file_handler.setLevel(logging.INFO)
#
#         # 创建控制台处理程序
#         console_handler = logging.StreamHandler()
#         console_handler.setLevel(logging.INFO)
#
#         # 设置统一的日志格式
#         formatter = logging.Formatter(
#             '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - line %(lineno)d - %(message)s'
#         )
#         file_handler.setFormatter(formatter)
#         console_handler.setFormatter(formatter)
#
#         # 将处理程序添加到日志记录器
#         logger.addHandler(file_handler)
#         logger.addHandler(console_handler)
#
#         # 避免日志重复打印到根日志器
#         logger.propagate = False
#
#     return logger
def setup_logger():
    """
    设置日志记录器并返回它。日志文件按年/月/日的层级结构保存。
    :return:
    """
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():
        file_handler = DailyFileHandler("./logfile", encoding="utf-8")
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 普通格式，用于写入文件
        file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - line %(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)

        # 彩色格式，用于控制台
        color_formatter = ColoredFormatter(
            "%(log_color)s%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - line %(lineno)d - %(message)s",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
        console_handler.setFormatter(color_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        logger.propagate = False

    return logger
