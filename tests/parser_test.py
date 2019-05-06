from r2s.extensions.abstract import R2SItemFormatter
from r2s.extensions.proofpoint.pcasb.alerts_formatter import PCASBAlertFormatter
from infra.data import options,item_1, valid_msg, valid_header, partial_item

def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    R2SItemFormatter.options = options

def test_severity_calc():
    
    assert PCASBAlertFormatter({'severity':'LOW'}).getSeverity() == '1'
    
    assert PCASBAlertFormatter({'severity':'MID'}).getSeverity() == '5'

    assert PCASBAlertFormatter({'severity':'HIGH'}).getSeverity() == '8'
    
    assert PCASBAlertFormatter({'severity':'CRITICAL'}).getSeverity() == '10'
    
    assert PCASBAlertFormatter({'severity':'INVALID'}).getSeverity() == '1'
    
    assert PCASBAlertFormatter({'mock':'INVALID'}).getSeverity() == '1'

def test_message_header():
    formatter = PCASBAlertFormatter(item_1)
    header = formatter.buildHeader()
    assert header == valid_header

def test_missing_fields():
    formatter = PCASBAlertFormatter(partial_item)
    msg = formatter.buildMessage()
    assert  msg == valid_msg #even for a partial msg - the parser does not fail