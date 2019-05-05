from r2s.extensions.proofpoint.pcasb.alerts_formatter import PCASBAlertFormatter
from infra.data import options,item_1, valid_msg, partial_item

def test_severity_calc():
    parser = PCASBAlertFormatter(options_parser)
    
    parser.setItem({'severity':'LOW'})
    assert parser.getSeverity() == 1
    
    parser.setItem({'severity':'MID'})
    assert parser.getSeverity() == 5

    parser.setItem({'severity':'HIGH'})
    assert parser.getSeverity() == 8
    
    parser.setItem({'severity':'CRITICAL'})
    assert parser.getSeverity() == 10
    
    parser.setItem({'severity':'INVALID'})
    assert parser.getSeverity() == 1
    
    parser.setItem({'mock':'INVALID'})
    assert parser.getSeverity() == 1

def test_message_header():
    parser = PCASBAlertFormatter(options)
    parser.setItem(item_1)
    msg = parser.buildMessage()
    assert msg == valid_msg

def test_missing_fields():
    parser = PCASBAlertFormatter(options)
    parser.setItem(partial_item)
    msg = parser.buildMessage()
    assert msg == valid_msg #even for a partial msg - the parser does not fail