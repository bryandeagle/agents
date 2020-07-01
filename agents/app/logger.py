from logging import handlers, Formatter, getLogger, INFO


_log_level = INFO
_formatter = Formatter(fmt='[%(levelname)s] %(message)s')
_file_handler = handlers.RotatingFileHandler(filename='app.log',
                                             maxBytes=5*1024*1024,
                                             encoding='utf-8')
_file_handler.setFormatter(_formatter)
_file_handler.setLevel(_log_level)

# Creat log object
log = getLogger(__name__)
log.addHandler(_file_handler)
log.setLevel(_log_level)
