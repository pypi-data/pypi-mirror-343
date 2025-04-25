from logging import DEBUG, Formatter, getLogger, LogRecord, Logger, StreamHandler

from .constants import LOG_PREFIX


# Create a custom formatter that adds a prefix to each log message
class _Formatter(Formatter):
    def format(self, record: LogRecord) -> str:
        return f"{LOG_PREFIX} {super().format(record=record)}"


# Create and configure the logger
_logger: Logger = getLogger(name="logger")
_logger.setLevel(level=DEBUG)  # Handle everything from DEBUG and above (DEBUG, INFO, WARNING, ERROR, CRITICAL)

# Avoid adding multiple handlers if the logger is imported multiple times
if not _logger.hasHandlers():
    # Create console handler and set level
    _console_handler: StreamHandler = StreamHandler()
    _console_handler.setLevel(level=DEBUG)

    # Create formatter and add it to the handler
    _formatter: _Formatter = _Formatter("%(asctime)s - %(levelname)s - %(message)s")
    _console_handler.setFormatter(fmt=_formatter)

    _logger.addHandler(hdlr=_console_handler)  # Add the handler to the logger
