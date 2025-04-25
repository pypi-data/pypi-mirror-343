# some logging to stdout
"""
old_factory = logging.getLogRecordFactory()

def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.custom_attribute = 0xdecafbad
    return record

logging.setLogRecordFactory(record_factory)
"""
import logging
from .defs import read_vach_cfg

logging.basicConfig(level=logging.INFO, format="%(levelname)s [%(module)s %(funcName)s] %(message)s") 
read_vach_cfg()
