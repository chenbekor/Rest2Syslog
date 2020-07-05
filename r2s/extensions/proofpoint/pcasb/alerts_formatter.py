from r2s.utils import _print, _print_debug,_print_error
from r2s.extensions.abstract import R2SItemFormatter
from datetime import datetime
from datetime import timezone

class PCASBAlertsFormatter(R2SItemFormatter):
    def __init__(self, item):
        _print_debug("About to initialize PCASBAlertsFormatter...")
        self.company_name = self.options['company_name']
        self.product_name = self.options['product_name']
        self.product_version = self.options['product_version']
        super().__init__(item)
    
    @staticmethod
    def wrapItems(items_as_json_array):
        formatters = []
        for item in items_as_json_array:
            formatters.append(PCASBAlertsFormatter(item))
        if len(formatters) > 0:
            return formatters
        else:
            return None

    def buildHeader(self):
        return 'LEEF:1.0|' + self.company_name + '|' + self.product_name + '|' + self.product_version + '|' + self.item['type'] + '|'
    
    def buildBody(self, leef_attributes):
        try:
            leef_body = ''
            for (key,val) in leef_attributes.items(): leef_body += (key + '=' + val + '\t')
            return leef_body
        except Exception as ex:
            _print_error(ex)
            return ''
            

    def getCategory(self): 
        return self.item['sub_type']

    def getTime(self):
        return str(self.item['timestamp'])
    
    def getDateTimeAsString(self):
        try:
            _t = self.item['timestamp']
            _print('about to parse this epoch: {}'.format(_t))
            return datetime.fromtimestamp(_t/1000.0,timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        except Exception as e: 
            _print('Error occured while trying to parse DateTimeAsString:{}'.format(e))
            return 'N/A'
    
    def getTimeFormat(self):
        return 'Milliseconds'

    def getSeverity(self):
        try:
            item_severity_text = self.item['severity']
        except: return '1'

        if item_severity_text == 'LOW':
            return '1'
        elif item_severity_text == 'MID':
            return '5'
        elif item_severity_text == 'HIGH':
            return '8'
        elif item_severity_text == 'CRITICAL':
            return '10'
        else:
            return '1'
    
    def getID(self):
        return self.item['id']
    
    def getDescription(self):
        return self.item['description'].replace('\n',' ')
    
    def getTitle(self):
        return self.item['title']
    
    def getUserName(self):
        try:
            return self.item['related_events'][0]['user_email']
        except:
            _print_error('could not extract user email from item id: ' + self.item['id'])
            return 'USER_NAME_EXTRACT_FAIL'
    
    def getCloudServiceName(self):
        try:
            return self.item['related_events'][0]['cloud_service']
        except:
            _print_error('could not extract cloud service name from item ' + self.item['id'])
            return 'CLOUD_SERVICE_EXTRACT_FAIL'
    
    def getClassification(self):
        try:
            return self.item['related_events'][0]['event_classification']['category']
        except:
            _print_error("could not extract the related event's category from item " + self.item['id'])
            return 'CLASSIFICATION_EXTRACT_FAIL'
    
    def getSubClassification(self):
        try:
            return self.item['related_events'][0]['event_classification']['sub_category']
        except:
            _print_error("could not extract the related event's sub category from item " + self.item['id'])
            return 'SUB_CLASSIFICATION_EXTRACT_FAIL'

    def getThreat(self):
        try:
            return self.item['related_events'][0]['event_classification']['threat']
        except:
            _print_error("could not extract the related event's threat from item " + self.item['id'])
            return 'THREAT_EXTRACT_FAIL'
    
    def buildMessage(self):
        leef_header = self.buildHeader()
        
        #standard LEEF Attributes
        leef_attributes = {}
        leef_attributes['cat'] = self.getCategory()
        leef_attributes['devTime'] = self.getTime()
        leef_attributes['devTimeFormat'] = self.getTimeFormat()
        leef_attributes['sev'] = self.getSeverity()
        leef_attributes['usrName'] = self.getUserName()
        
        #extended LEEF Attributes
        leef_attributes['alertID'] = self.getID()
        leef_attributes['description'] = self.getDescription()
        leef_attributes['title'] = self.getTitle()
        leef_attributes['cloudService'] = self.getCloudServiceName()
        leef_attributes['alertClassification'] = self.getClassification()
        leef_attributes['alertSubClassification'] = self.getSubClassification()
        leef_attributes['threat'] = self.getThreat()
        leef_attributes['dateTimeString'] = self.getDateTimeAsString()

        leef_body = self.buildBody(leef_attributes)
        
        leef_msg = leef_header + leef_body
        return leef_msg
