from logging import INFO, Formatter, StreamHandler, getLogger

# Logger setting
handler = StreamHandler()
handler.setLevel(INFO)
fmt = '[%(levelname)s] %(message)s'
formatter = Formatter(fmt)
handler.setFormatter(formatter)
logger = getLogger()
logger.setLevel(INFO)
logger.addHandler(handler)
