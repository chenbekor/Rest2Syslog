from r2s.extensions.abstract import R2SItemFormatter
from r2s.extensions.proofpoint.pcasb.events_formatter import PCASBEventsFormatter
from infra.events_data import options,item_1, valid_msg, valid_partial_msg, valid_header, partial_item
from r2s.utils import _print_debug

def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    R2SItemFormatter.options = options



def test_message_header():
    formatter = PCASBEventsFormatter(item_1)
    header = formatter.buildHeader()
    assert header == valid_header

def test_message():
    formatter = PCASBEventsFormatter(item_1)
    leef_msg = formatter.buildMessage()
    _print_debug(leef_msg)
    _print_debug(valid_msg)
    assert leef_msg == valid_msg

def test_missing_fields():
    formatter = PCASBEventsFormatter(partial_item)
    msg = formatter.buildMessage()
    _print_debug(msg)
    _print_debug(valid_partial_msg)
    assert  msg == valid_partial_msg #even for a partial msg - the parser does not fail