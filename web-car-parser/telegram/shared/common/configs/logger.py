import logging
from datetime import datetime, timedelta


class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = datetime.fromtimestamp(record.created)
        ct += timedelta(hours=0)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s,%03d" % (t, record.msecs)
        return s

    def apply_config(self, configs: list) -> list:
        processed_handlers = []
        for item in configs:
            item[0].setLevel(item[1])
            item[0].setFormatter(self)
            processed_handlers.append(item[0])
        return processed_handlers


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

formatter_obj = CustomFormatter(
    fmt='[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
)

warning_handler, critical_handler, general_handler = \
    logging.StreamHandler(), logging.StreamHandler(), logging.StreamHandler()

handlers_config = [
    [warning_handler, logging.WARNING], [critical_handler, logging.CRITICAL], [general_handler, logging.INFO]
]

logging.basicConfig(level=logging.DEBUG, handlers=formatter_obj.apply_config(configs=handlers_config))
