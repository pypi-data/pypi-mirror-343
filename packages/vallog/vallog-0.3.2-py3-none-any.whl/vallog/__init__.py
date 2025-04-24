"""
importing Logger module
make variables accessible to the user
"""

from vallog.logger import Logger
from vallog.timer import Timer


default = Logger.default
info = Logger.info
warning = Logger.warning
error = Logger.error
debug = Logger.debug
header = Logger.header
