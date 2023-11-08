import logging
import sys
import datetime as dt

from collections.abc import Callable

try:
    import curses
except ImportError:
    curses = None


class LogFormatter(logging.Formatter):
    DEFAULT_FORMAT: str = (
        "%(color)s"
        "[%(module_name)s-%(task_id)d/%(name)s %(levelname)1.1s "
        "%(asctime)s %(module)s:%(lineno)d]"
        "%(end_color)s %(message)s"
    )

    DEFAULT_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S.%f%Z"

    DEFAULT_COLORS: dict = {
        logging.DEBUG: 4,  # Blue
        logging.INFO: 2,  # Green
        logging.WARNING: 3,  # Yellow
        logging.ERROR: 1,  # Red
    }

    converter: Callable[..., dt.datetime] = dt.datetime.fromtimestamp

    def __init__(
        self,
        module=None,
        task_id=0,
        color=True,
        fmt=DEFAULT_FORMAT,
        datefmt=DEFAULT_DATE_FORMAT,
        colors=None,
    ):
        super(LogFormatter, self).__init__(datefmt=datefmt)

        if colors is None:
            colors = self.DEFAULT_COLORS

        self._module_name = module
        self._task_id = task_id
        self._fmt = fmt
        self._colors = {}
        self._color = color and self._stderr_supports_color()

    def _stderr_supports_color(self) -> bool:
        color = False
        if curses and sys.stderr.isatty():
            try:
                curses.setupterm()
                if curses.tigetnum("colors") > 0:
                    color = True
            except Exception:
                pass
        return color

    def formatTime(self, record, datefmt=None) -> str:
        ct = self.converter(record.created)
        if datefmt:
            return ct.strftime(datefmt)
        else:
            return ct.strftime(self.DEFAULT_DATE_FORMAT)

    def format(self, record) -> str:
        try:
            record.message = record.getMessage()
        except Exception as e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)

        record.module_name = self._module_name
        record.task_id = self._task_id
        record.asctime = self.formatTime(record, self.datefmt)

        prefix = (
            "[%(task_id)d %(levelname)s " + "%(asctime)s %(module)s:%(lineno)d]"
        ) % record.__dict__

        formatted = prefix + " " + record.message
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            lines = [formatted.rstrip()]
            lines.extend(ln.strip() for ln in record.exc_text.split("\n"))
            formatted = " ".join(lines)
        return formatted.replace("\n", " ")
