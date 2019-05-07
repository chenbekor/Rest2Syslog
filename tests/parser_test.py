from r2s.extensions.abstract import R2SItemFormatter
from r2s.extensions.proofpoint.pcasb.alerts_formatter import PCASBAlertsFormatter
from infra.data import options,item_1, valid_msg, valid_header, partial_item

def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    R2SItemFormatter.options = options

def test_severity_calc():
    
    assert PCASBAlertsFormatter({'severity':'LOW'}).getSeverity() == '1'
    
    assert PCASBAlertsFormatter({'severity':'MID'}).getSeverity() == '5'

    assert PCASBAlertsFormatter({'severity':'HIGH'}).getSeverity() == '8'
    
    assert PCASBAlertsFormatter({'severity':'CRITICAL'}).getSeverity() == '10'
    
    assert PCASBAlertsFormatter({'severity':'INVALID'}).getSeverity() == '1'
    
    assert PCASBAlertsFormatter({'mock':'INVALID'}).getSeverity() == '1'

def test_message_header():
    formatter = PCASBAlertsFormatter(item_1)
    header = formatter.buildHeader()
    assert header == valid_header

def test_missing_fields():
    formatter = PCASBAlertsFormatter(partial_item)
    msg = formatter.buildMessage()
    assert  msg == valid_msg #even for a partial msg - the parser does not fail