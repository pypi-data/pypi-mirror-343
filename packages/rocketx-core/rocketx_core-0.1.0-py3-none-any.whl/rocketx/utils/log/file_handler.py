# encoding: utf8
import logging

class FileHandler(logging.Handler):
    """
    FileHandler is python log handler that handles writing logs into specified file.

    It creates and delgates log handling to `logging.FileHandler` after receiving task
    instance context.

    :param base_log_folder: Base log folder to place logs.
    :param max_bytes: max bytes for each log file.
    :param backup_count: backup file count for each log file.
    :param delay: default False -> StreamHandler, True -> FileHandler
    """
    def __init__(
        self, 
        base_log_folder: str, 
        max_bytes: int = 0, 
        backup_count: int = 0, 
        delay: bool = False
    ):
        super().__init__()
        self.handler: logging.FileHandler | None = None
        self.local_base = base_log_folder
        self.maintain_propagate: bool = False
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.delay = delay  # If true, overrides default behavior of setting `propagate=False`


    def set_context(self):
        ...
    