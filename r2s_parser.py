from syslogng import LogMessage
from r2s_utils import _print


class Parser:
    def __init__(self,options):
        self.company_name = options['company_name']
        self.product_name = options['product_name']
        self.product_version = options['product_version']

    def calculateSeverity(self,alert):
        alert_severity_text = alert['severity']
        if alert_severity_text == 'LOW':
            return 1
        elif alert_severity_text == 'MID':
            return 5
        elif alert_severity_text == 'HIGH':
            return 8
        elif alert_severity_text == 'CRITICAL':
            return 10
        else:
            return 1

    def buildMessage(self,alert):
        leef_header = 'LEEF:1.0|' + self.company_name + '|' + self.product_name + '|' + self.product_version + '|' + alert['type'] + '|'
        leef_attributes = {}
        leef_attributes['cat'] = alert['sub_type']
        leef_attributes['devTime'] = str(alert['timestamp'])
        leef_attributes['devTimeFormat'] = 'Milliseconds'
        leef_attributes['sev'] = str(self.calculateSeverity(alert))
        leef_attributes['alertID'] = alert['id']
        leef_attributes['description'] = alert['description'].replace('\n',' ')
        leef_attributes['title'] = alert['title']
        try:
            leef_attributes['usrName'] = alert['related_events'][0]['user_email']
        except:
            _print('could not extract user email from alert id: ' + alert['id'])
        try:
            leef_attributes['cloudService'] = alert['related_events'][0]['cloud_service']
        except:
            _print('could not extract cloud service name from alert ' + alert['id'])
        try:
            leef_attributes['eventCategory'] = alert['related_events'][0]['event_classification']['category']
        except:
            _print("could not extract the related event's category from alert " + alert['id'])
        try:
            leef_attributes['eventSubCategory'] = alert['related_events'][0]['event_classification']['sub_category']
        except:
            _print("could not extract the related event's sub category from alert " + alert['id'])
        try:
            leef_attributes['threat'] = alert['related_events'][0]['event_classification']['threat']
        except:
            _print("could not extract the related event's threat from alert " + alert['id'])

        leef_body = ''
        for (key,val) in leef_attributes.items(): leef_body += (key + '=' + val + '\t')
        leef_msg = leef_header + leef_body
        return LogMessage(leef_msg)
