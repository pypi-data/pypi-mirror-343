import queue
import atexit
import logging.config
import logging.handlers
from logging.handlers import QueueListener
from .config import dictConfig
from ..utils.python_version import PythonVersion


def setup_root_logger():
    """ Setup root logger with filters, formatters, handlers and loggers """
    # Get python version info minor detail
    python_version_info_minor = PythonVersion.get_minor()
    # For python versions >= 3.12
    if python_version_info_minor >= 12:
        # Configure root logger using dictConfig
        logging.config.dictConfig(dictConfig)
        # Returns queue_handler handler which is defined in config
        queue_handler = logging.getHandlerByName("queue_handler")
        # Check if queue handler exists
        if queue_handler is not None:
            # Start listener for queue handler
            queue_handler.listener.start()
            # Register queue handler cleanup method to perform clean up upon interpreter termination
            atexit.register(queue_handler.listener.stop)
    # For older python versions < 3.12
    else:
        # Remove the handlers key, as it's not supported for lower versions
        dictConfig['handlers']['queue_handler'].pop('handlers')
        # Remove the respect_handler_level key, as it's not supported for lower versions
        dictConfig['handlers']['queue_handler'].pop('respect_handler_level')
        # Add the custom handlers to root logger handlers
        # This will bring the handlers in configuration dictionary to runtime object
        dictConfig['loggers']['root']['handlers'] = ['queue_handler',
                                                     'test_rest_api_console_handler',
                                                     'test_rest_api_report_handler']
        # Create the log queue
        log_queue = queue.Queue()
        # Update the configuration dictionary
        # Add queue object to queue_handler using the key "queue"
        dictConfig['handlers']['queue_handler']['queue'] = log_queue
        # After updating the configuration dictionary to support older versions, Now we can configure root logger using dictConfig
        logging.config.dictConfig(dictConfig)
        # Get the custom handlers to add them in the QueueListener
        test_rest_api_console_handler, test_rest_api_report_handler = logging.getLogger().handlers[1:]
        # Create the QueueListener with the configured handlers
        # Explicitly pass the handlers to the QueueListener
        listener = QueueListener(log_queue, test_rest_api_console_handler, test_rest_api_report_handler)
        # After adding them to the QueueListener, we can remove them from the logger
        # This is to avoid duplicate logging
        # This makes the root logger to only have the queue handler, and queue handler will process custom handlers
        logging.getLogger().handlers = logging.getLogger().handlers[:-2]
        # Start listener for queue handler
        listener.start()
        # Register listener cleanup method to perform clean up upon interpreter termination
        atexit.register(listener.stop)
