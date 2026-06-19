import logging

def get_logger(name: str, level: str | int = "INFO") -> logging.Logger:
    """
    Return a named logger, configuring the root logger on first call.

    Parameters
    name : str
        Logger name Always pass __name__ so log output shows the module it came from
    level : str or int
        minimum log level. Default to INFO

    Returns
    logging.Logger
        configured name logger

    """
    root_logger = logging.getLogger()

    if not root_logger.handlers:
        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            fmt="[%(asctime)s] %(filename)s %(lineno)d  %(levelname)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)

        root_logger.setLevel(level)

    return logging.getLogger(name)