"""
.. module:: fmt
    :platform: Unix, Windows
    :synopsis: Base module for formatting log output
        Best practices retrieved from
        https://docs.python.org/3/howto/logging-cookbook.html
"""

# Python Standard Libraries
import datetime
import logging
import re
import uuid

# 3rd Party Libraries
from dateutil import tz  # pylint: disable=import-error

# Project Specific Libraries
from elevaso_spine.fmt.sub import sub_value

# These are reserved attribute names for logging
# http://docs.python.org/library/logging.html#logrecord-attributes
RESERVED_ATTRS = (
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "message",
    "module",
    "msecs",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "taskName",
    "thread",
    "threadName",
)

# These are the only keyword arguments allowed to be passed
# down to the logging.Formatter during __init__
LOGGING_KWARGS = ["fmt", "datefmt", "style", "validate"]

DEFAULT_PATTERN = re.compile(
    r"%\((?P<var>\w+)\)[#0+ -]*(\*|\d+)?(\.(\*|\d+))?[diouxefgcrsa%]",
    re.IGNORECASE,
)

LOGGER = logging.getLogger(__name__)


class BaseFormatter(logging.Formatter):
    """Custom base formatting class

    Attributes:
        default_dtm_format: Default date/time format, defaults to
        %Y-%m-%d %H:%M:%S.%f %z

        default_time_zone: The default time zone to output timestamps in,
        defaults to UTC
    """

    # These are the default settings for this class
    default_dtm_format = "%Y-%m-%d %H:%M:%S.%f %z"
    default_timezone = "UTC"
    output_func = None

    def __init__(self, **kwargs):
        """Initialize instance of the class

        Kwargs:
            include_keys (list): List of reserved keys to include in all json
            logging, defaults to RESERVED_ATTRS

            timestamp_key (str): Name of the timestamp json key (either
            provided in log message extra or automatically added), defaults
            to None

            session_key (str): Name of the session json key (either provided
            in log message extra or automatically added as uuid4), defaults to
            None

            dtm_format (str): Date/time format for asctime and/or
            timestamp_key, defaults to `self.default_dtm_format`

            timezone (str): String representing the time zone, defaults to
            `self.default_timezone`

            extra (dict): Dictionary of key/value data to provide on all
            log messages

        Raises:
            ValueError if timezone is invalid
        """
        # Saving the original kwargs so we can reference in other
        # classes using this as the base
        self.kwargs = kwargs

        self.__include_keys = kwargs.pop("include_keys", RESERVED_ATTRS)
        self.__timestamp_key = kwargs.pop("timestamp_key", None)
        self.__session_key = kwargs.pop("session_key", None)
        self.__dtm_format = kwargs.pop("dtm_format", self.default_dtm_format)
        self.__timezone = kwargs.pop("timezone", self.default_timezone)
        self.__extra = kwargs.pop("extra", {})
        self.fmt = kwargs.pop("format", None) or kwargs.get("fmt", None)

        if self.__timezone != self.default_timezone and not tz.gettz(
            self.__timezone
        ):
            raise ValueError(f"Timezone {self.__timezone} is invalid")

        # This is only used if the session_key does not exist in the log
        # message
        if self.__session_key:
            self.__session_id = uuid.uuid4()

        logging.Formatter.__init__(
            self, **{k: v for k, v in kwargs.items() if k in LOGGING_KWARGS}
        )

    def __create_output(self, record: logging.LogRecord) -> dict:
        """Updates the record based on various checks

        Args:
            record (logging.LogRecord): log record

        Returns:
            dict: Dictionary format of the record
        """
        output = self.__extra

        if isinstance(record.msg, dict):
            # It's already a dictionary, so add to output as-is
            output.update(record.msg)
        else:
            record.message = record.getMessage()

        if "asctime" in self.__include_keys:
            record.asctime = self.formatTime(record, self.datefmt)

        if "exc_info" in self.__include_keys and (
            record.exc_info or record.exc_text
        ):
            output.update(
                {
                    "exc_info": self.formatException(record.exc_info)
                    or record.exc_text
                }
            )

        return output

    def __append_output(self, record: logging.LogRecord, output: dict) -> dict:
        """Append fields/values to the output

        Args:
            record (logging.LogRecord): log record

            val (dict): Dictionary of values to append to

        Returns:
            dict: Dictionary of values with updated values
        """
        output.update(
            {
                key: value
                for key, value in record.__dict__.items()
                if key in self.__include_keys
            }
        )

        if (
            self.__session_key
            and self.__session_key not in record.__dict__.keys()
        ):
            output[self.__session_key] = self.__session_id
        if (
            self.__timestamp_key
            and self.__timestamp_key not in record.__dict__.keys()
        ):
            output[self.__timestamp_key] = self.formatTime(record, self.datefmt
                                                           )

        output.update(
            {
                key: value
                for key, value in record.__dict__.items()
                if key not in RESERVED_ATTRS
            }
        )

        return output

    def format(self, record: logging.LogRecord) -> str:
        """Formats the log record

        Args:
            record (logging.LogRecord): log record to format

        Returns:
            object: Formatted log output
        """
        output = self.__create_output(record)

        output = self.__append_output(record, output)

        extra_keys = {
            **{
                key: value
                for key, value in record.__dict__.items()
                if key not in RESERVED_ATTRS
            }
        }

        if self.output_func:
            # pylint: disable=not-callable
            return self.output_func(output, extra_keys=extra_keys)

        if self.fmt:
            return sub_value(self.fmt, output, pattern=DEFAULT_PATTERN)

        return output["msg"]

    def formatTime(self, record: logging.LogRecord, datefmt: str = None) -> \
                                                                        str:
        """Format the time and converts to desired timezone

        Args:
            record (logging.LogRecord): log record to format

            datefmt (str, optional): Format of the date/time, defaults to None

        Returns:
            str: String of the date/time value
        """
        date_time = datetime.datetime.fromtimestamp(
            record.created, tz=datetime.timezone.utc
        )

        if self.__timezone != "UTC":
            date_time = date_time.astimezone(tz=tz.gettz(self.__timezone))

        return date_time.strftime(self.__dtm_format)
