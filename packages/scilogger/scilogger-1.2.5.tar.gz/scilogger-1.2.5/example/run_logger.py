"""
Simple script demonstrating the SciLogger capabilities.
"""

__author__ = "Thomas Guillod"
__copyright__ = "Thomas Guillod - Dartmouth College"
__license__ = "BSD License"

import sys
import time
import scilogger
import mod_a
import mod_b

# create the logger
LOGGER = scilogger.get_logger(__name__, "main")


if __name__ == "__main__":
    # start timer
    timestamp = scilogger.get_timestamp()

    # normal messages
    LOGGER.debug("debug level log")
    time.sleep(0.1)
    LOGGER.info("info level log")
    time.sleep(0.1)
    LOGGER.error("error level log")

    # log inside a timed block
    with LOGGER.BlockTimer("example for the timed blocks", level="INFO"):
        LOGGER.info("info level log")
        time.sleep(0.1)
        LOGGER.info("info level log")

    # log inside an indented block
    with LOGGER.BlockDisplay("example for the indented blocks", level="INFO"):
        LOGGER.info("info level log")
        time.sleep(0.1)
        LOGGER.info("info level log")

    # log an exception
    try:
        raise ValueError("example for the exceptions")
    except ValueError as ex:
        LOGGER.log_exception(ex=ex, level="ERROR")

    # call another module
    mod_a.display()
    mod_b.display()

    # get total time
    (seconds, duration, date) = scilogger.get_duration(timestamp)
    LOGGER.info("timing data")
    with LOGGER.BlockIndent():
        LOGGER.info("date = %s" % date)
        LOGGER.info("duration = %s" % duration)
        LOGGER.info("seconds = %.3f" % seconds)

    sys.exit(0)
