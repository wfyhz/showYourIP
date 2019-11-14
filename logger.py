# coding=utf-8
import logging


def init_logger(threshold=logging.INFO, log_file="all.log"):
    fmt = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
    filename = log_file
    handler = logging.FileHandler(filename=filename)
    log = logging.getLogger("zhou")
    # 以info为阈值,若想要debug信息,可以调整为DEBUG
    log.setLevel(threshold)
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.propagate = False
    return log


logger = init_logger()
