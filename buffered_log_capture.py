import logging
from six import StringIO


class NotCapturing(RuntimeError):
    """Raised when attempting to call BufferedLogCapture.stop() before start()."""


class BufferedLogCapture(object):
    """Context manager to buffer logging messages to an internal buffer. Logging to the buffer can be achieved
    either by calling start() and stop(), or using an instances as a context manager.
    If `new_log_level` is passed to __init__, the root logger will be updated to that level while the buffer
    log is active. Please note that this may result in unwanted messages being logged to other handlers while active.
    This buffers data in memory, please be cognizant of logging output volume."""

    capturing = False
    new_log_level = None
    old_log_level = None
    log_handler = None
    buffer = None
    _context_nesting = 0

    def __init__(self,
                 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                 new_log_level=None):
        self.new_log_level = new_log_level
        self.format = format
        self.reset()

    def reset(self):
        """Empty the internal log buffer"""
        self.buffer = StringIO()

    def start(self):
        if self.capturing:
            return

        self.capturing = True
        root_logger = logging.getLogger()
        if self.new_log_level is not None:
            self.old_log_level = root_logger.getEffectiveLevel()
            root_logger.setLevel(self.new_log_level)

        self.log_handler = logging.StreamHandler(self.buffer)
        formatter = logging.Formatter(self.format)
        self.log_handler.setFormatter(formatter)
        root_logger.addHandler(self.log_handler)

    def stop(self):
        if not self.capturing:
            raise NotCapturing()

        self.capturing = False
        root_logger = logging.getLogger()
        if self.old_log_level is not None:
            root_logger.setLevel(self.old_log_level)
            self.old_log_level = None

        root_logger.removeHandler(self.log_handler)
        self.log_handler.flush()
        self.buffer.flush()

    def __enter__(self):
        self.start()
        self._context_nesting += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._context_nesting -= 1
        if self._context_nesting == 0:
            self.stop()

    def getvalue(self):
        return self.buffer.getvalue()
